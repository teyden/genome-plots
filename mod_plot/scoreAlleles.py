import os
import parser
from db_model import ChromosomeCollection

DEFAULT_OUTPUT_FILEPATH = '../../BIO_DATA/alleleScores.txt'
DEFAULT_REF_FILEPATH = '../../BIO_DATA/23andme_v4_hg19_ref.txt'
DEFAULT_USER_FILEPATH = '../../BIO_DATA/raw23andme_SNPs_teyden.txt'

# Value... (fieldnames)
RSID = 'RSID'
DESCRIPTION = 'DESCRIPTION'
CHROMOSOME = 'CHROMOSOME'
POSITION = 'POSITION'
GENOTYPE = 'GENOTYPE'
DATE = 'DATE'

def isIndel(genotype):
	if len(genotype) > 1 and any([genotype == x for x in ['DD', 'DI', 'ID', 'II']]):
		return True
	elif len(genotype) == 1 and any([genotype == x for x in ['D', 'I']]):
		return True
	else:
		return False 

def scoreAlleles(RefSNPFile, UserSNPFile):
	"""
	Structure of RefSNPdict and UserSNPdict:
		key = chromosome string as '1', '2', ..., '23' (X), '24' (Y), '25', (MT/M)

	(*) Reference allele is only ONE letter. 

	- Genotype is a string of len=2, the original allele representations from the 23andme file

	- Variant(s) represents any letters different from the Reference, if none then given '-'

	- Match Score (0,1,2): the SNP is given a score of ...
			- 2 (homozygous) if both letters are the same as the Reference
			- 1 (heterozygous) if one letter is the same as the Reference
			- 0 (recessive) if neither match the reference 

	(*) Variants given a match score of 0 may need to be switched to the 
	opposite letters (A to T, C to G and vice versa); must check to 
	confirm which are minus vs. plus strands)

	### BASIC FORMAT:
	#chrNum 	position 	Ref 	Genotype	Variant 	Matches(0,1,2)
	1			1000		A 		AA 			-			

	RETURNS: none, streams to file... 
	"""
	RefSNPdict = parser._referenceObject(RefSNPFile, 'CHROMOSOME')
	UserSNPdict = parser._23andmeObject(UserSNPFile, 'CHROMOSOME')

	nonMatchedRSIDs = []
	numMatchedRSIDs = 0
	indel = {}

	F = open(DEFAULT_OUTPUT_FILEPATH, 'w')
	F.write('#Chrom\tRSID\tPos\tRef\tGenotype\tVariant(s)\tMatch Score\n')
	for chr in parser.CHROMOSOME_LIST:
		positions = RefSNPdict[chr].keys()
		positions.sort()
		indel[chr] = {}
		for pos in positions:
			refAllele = RefSNPdict[chr][pos][GENOTYPE].upper()
			rsid = RefSNPdict[chr][pos][RSID]

			# Check allele cases for ref in the user's snps
			if pos in UserSNPdict[chr]:
				if rsid != UserSNPdict[chr][pos][RSID]:
					nonMatchedRSIDs += [(rsid, UserSNPdict[chr][pos][RSID])]

				if isIndel(UserSNPdict[chr][pos][GENOTYPE]):
					indel[chr][pos] = {
						RSID: UserSNPdict[chr][pos][RSID], 
						GENOTYPE: UserSNPdict[chr][pos][GENOTYPE]
						}

				else:
					numMatchedRSIDs += 1
					sampleAllele = UserSNPdict[chr][pos][GENOTYPE]		# 3

					# Chromosomes 1-22 will have an allele pair, hence str len of 2
					if len(sampleAllele) == 2:
						if sampleAllele[0] == '-' and sampleAllele[1] == '-':
							variant = '-'
							score = '-'
						elif sampleAllele[0].lower() == refAllele.lower() and sampleAllele[1].lower() == refAllele.lower():
							variant = '-'
							score = 2
						elif sampleAllele[0].lower() == refAllele.lower():
							variant = sampleAllele[1]
							score = 1
						elif sampleAllele[1].lower() == refAllele.lower():
							variant = sampleAllele[0]
							score = 1
						else:
							variant = sampleAllele
							score = 0

					# Mitochondria, X, and Y chromosome alleles are of length 1
					elif len(sampleAllele) == 1:
						if sampleAllele == '-':
							variant = '-'
							score = '-'
						elif sampleAllele.lower() == refAllele.lower():
							variant = '-'
							score = 1
						else:
							variant = sampleAllele
							score = 0

					F.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\n' % (chr, rsid, pos, refAllele, sampleAllele, variant, score))

	F.close()
	parser.printMsg("Completed scoring user SNPs to REF SNPs. Streamed to a .teyden (LOL) file format (path=%s)" % DEFAULT_OUTPUT_FILEPATH)
	parser.printMsg('Number of matched rsid values: %s' % numMatchedRSIDs)
	parser.printMsg('Number of unmatched rsid values: %s' % len(nonMatchedRSIDs))
	return indel 

indel = scoreAlleles(DEFAULT_REF_FILEPATH, DEFAULT_USER_FILEPATH)
print len(indel)

for chr in indel:
	totalIndels = len(indel[chr].keys())
	numInsertions = 0
	numDeletions = 0
	numIDDI = 0
	for pos in indel[chr].keys():
		if any([indel[chr][pos][GENOTYPE] == x for x in ['I', 'II']]):
			numInsertions += 1
		elif any([indel[chr][pos][GENOTYPE] == x for x in ['D', 'DD']]):
			numDeletions += 1
		elif any([indel[chr][pos][GENOTYPE] == x for x in ['ID', 'DI']]):
			numIDDI += 1

	if chr == '23':
		chrom = 'X'
	elif chr == '24':
		chrom = 'Y'
	elif chr == '25':
		chrom = 'MT'
	else:
		chrom = chr
	ChromosomeCollection.update_one(
		{'_id': chr},
		{'$set':
			{
				# 'totalIndels': totalIndels,
				# 'numIDDI': numIDDI,
				# 'numInsertions': numInsertions,
				# 'numDeletions': numDeletions
				'value': chrom
			}
		}
	)
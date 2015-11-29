from parser import _referenceObject, parse_reference, printMsg


def scoreAlleles(RefSNPdict, UserSNPdict, filename):
	"""
	Makes simple SNP file for analysis by SNPhylo tree maker

	** 
	- SNPhylo is case-sensitive
	- Also requires single genotype mutation, represent single alleles different from the ref only

	### BASIC FORMAT:
	#chrNum 	position 	Ref 	SampleID1	... 
	1		1000		A 		A 		T 
	"""
	F = open('../../BIO_DATA/simplesnp/%s.txt' % filename, 'w')
	F.write('#Chrom\tPos\tRef\tSampleID1\n')
	for chr in CHROMOSOME_LIST:
		positions = RefSNPdict[chr].keys()
		positions.sort()
		for pos in positions:
			chrNum = chr								# 1
			position = pos 		 						# 2
			ref = RefSNPdict[chr][pos][GENOTYPE].upper()
			if pos in UserSNPdict[chr]:
				sample_genotype = UserSNPdict[chr][pos][GENOTYPE]		# 3
				sample = sample_genotype
				if len(sample_genotype) > 1:
					if ref.lower() == sample_genotype[0].lower():
						sample = sample_genotype[1]
					else:
						sample = sample_genotype[0]
				F.write('%s\t%s\t%s\t%s\n' % (chrNum, position, ref, sample))

	F.close()
	printMsg("Completed streaming to Simple SNP file format (path=simplesnp/%s)" % filename)


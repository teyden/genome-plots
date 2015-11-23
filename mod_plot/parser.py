
import json
import os

CHROMOSOME_LIST = [ '%s' % i for i in range(1,26)] # + ['X', 'Y', 'MT']
FILETYPES = ['vcf', '23andme', 'hapmap', 'bed']

RSID = 'RSID'
# Value... (fieldnames)
DESCRIPTION = 'DESCRIPTION'
CHROMOSOME = 'CHROMOSOME'
POSITION = 'POSITION'
GENOTYPE = 'GENOTYPE'
DATE = 'DATE'


def printMsg(string):
	"""
	Looks like this:
	__________

	SNP Values
	__________

	"""
	length = len(string)
	dashes = ""
	for i in range(0,length+2):
		dashes += "-"
	final = "\n" + dashes + "\n " + string + " \n" + dashes 
	print final 


def add_rsidValues(chromosome="", position=0, genotype=""):
	new_snp = {}
	new_snp[CHROMOSOME] = chromosome
	new_snp[POSITION] = position
	new_snp[GENOTYPE] = genotype
	return new_snp


sortOptions = [RSID, CHROMOSOME, POSITION]
def parse_23andmeFile(user_snp_file="", sortOption=""):
	"""
	Parses SNPs of user from locally saved file (.txt format) 
	that was downloaded through user upload or 23andme access. 

	Returns one of ...
	- Dictionary of all 23andme SNPs with RSID key
	- Dictionary of all 23andme SNPs with CHROMSOME key to a 
	dictionary of each SNP in a chromosome with POSITION key
	- Dictionary of all 23andme SNPs with POSITION key

	"""
	if os.path.exists(user_snp_file):
		f = open(user_snp_file, 'r')
		
		output = {}
		if sortOption == CHROMOSOME:			
			for chr in CHROMOSOME_LIST:
				output[chr] = {} 
		
		numSNPs = 0
		for line in f:
			line = line.strip()
			if line[0] != "#":
				rsid, chromosome, position, genotype = line.split()
				numSNPs += 1

				if sortOption == RSID: 
					output[rsid] = {
						CHROMOSOME: chromosome, 
						GENOTYPE: genotype, 
						POSITION: position
						} 

				elif sortOption == POSITION:
					output[position] = {
						CHROMOSOME: chromosome, 
						GENOTYPE: genotype, 
						RSID: rsid
						}

				elif sortOption == CHROMOSOME:
					output[chromosome][position] = {
						RSID: rsid, 
						GENOTYPE: genotype
						}	

		print "Total: %d" % numSNPs
		f.close()
		return output 
	else:
		print "Path <%s> not found" % user_snp_file
		return {}


def _23andmeObject(SNPfile, sortOption):
	"""
	Returns a SNP dictionary in the specified sorting format.
	Options are: [RSID, CHROMOSOME, POSITION]
	"""
	if not any([sortOption != option for option in sortOptions]):
		raise ValueError, "Please select a valid sortOption: RSID, CHROMOSOME, or POSITION"

	output = parse_23andmeFile(SNPfile, sortOption)
	if output == {}:
		printMsg("Error: verify inputs")
		return {}
	else:
		all = [len(output[chr]) for chr in output]
		numSNPs = sum(all)
		printMsg("Success! SNP dictionary obtained by %s (%s SNPs)" % (sortOption, numSNPs))
		return output 


FILETYPES = ['vcf', '23andme', 'hapmap', 'bed']
def grabData(filetype, filepath):
	"""
	~/Projects/snphylo/snphylo.sh -v genetic_data/snps/snps_teyden.vcf
	Grabs data from any of the filetypes specified below and
	returns a JSON for each value
	"""
	if filetype == FILETYPES[1]:
		pass


def printDataLines(SNPdict):
	pass


def stream2BEDfile(SNPdict, filename):
	"""
	Makes simple BED file 

	### BASIC FORMAT:
	#chrNum 	start_pos	end_pos		rsID 	... 
	chr1	23098138	23098139	rs21398723

	"""
	F = open('bed/%s.txt' % filename, 'w')
	for chr in CHROMOSOME_LIST:
		positions = SNPdict[chr].keys()
		positions.sort()
		for pos in positions:
			chrNum = 'chr%s' % chr 							# 1
			start_pos = int(pos)							# 2
			end_pos = int(pos)+1							# 3
			rsID = SNPdict[chr][pos][RSID]					# 4
			F.write('%s\t%d\t%d\t%s\n' % (chrNum, start_pos, end_pos, rsID))
	F.close()
	printMsg("Completed streaming to BED file format (path=bed/%s)" % filename)


def stream2SSfile(SNPdict, filename):
	"""
	Makes simple SNP file for analysis by SNPhylo tree maker

	### BASIC FORMAT:
	#chrNum 	position 	SampleID1	SampleID2	... 
	1		1000		A 		A 		T 
	"""
	F = open('simplesnp/%s.txt' % filename, 'w')
	F.write('#Chrom\tPos\tSampleID1\t\n')
	for chr in CHROMOSOME_LIST:
		positions = SNPdict[chr].keys()
		positions.sort()
		for pos in positions:
			chrNum = chr								# 1
			position = pos 		 						# 2
			sample = SNPdict[chr][pos][GENOTYPE]		# 3
			F.write('%s\t%s\t%s\t\n' % (chrNum, position, sample))
	F.close()
	printMsg("Completed streaming to Simple SNP file format (path=simplesnp/%s)" % filename)


def stream2HapMapfile(SNPdict, filename):
	"""
	** NOT READY FOR USE **
	- Needs to add columns for all Samples > 1
	- Need to add reference alleles for 'alleles' column

	Makes .hapmap for analysis by SNPhylo tree maker

	### BASIC FORMAT:
	rs#		alleles		chrom 		pos 	strand	assembly#	protLSID	assayLSID	panelLSID	QCCODE		W01		W02 ... 
	rs90823		A/C 	1 		  23112		   .       NA		   NA		   NA  		    NA		   NA   	 AC  	 CC
	"""
	F = open('hapmap/%s.hapmap' % filename, 'w')
	F.write('rs#\talleles\tchrom\tpos\tstrand\tassembly#\tprotLSID\tassayLSID\tpanelLSID\tQCCODE\t\n')
	for chr in CHROMOSOME_LIST:
		positions = SNPdict[chr].keys()
		positions.sort()
		for pos in positions:
			rsNum = SNPdict[chr][pos][RSID]				# 1
			chrNum = chr								# 2
			position = pos								# 3
			sample = SNPdict[chr][pos][GENOTYPE]		# 4
			F.write('%s\t%s\t%s\t%s\n.\tNA\tNA\tNA\tNA\tNA\tNA\t' % (rsNum, REF_RSID[rsNum]['alleles'], chrNum, position))
	F.close()
	printMsg("Completed streaming to hapmap file format (path=hapmap/%s)" % filename)
import json
import os
import datetime
import db_model

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


def swapChrom(x):
	if x == 'X':
		return '23'
 	elif x == 'Y':
		return '24'
	elif x == 'MT' or x == 'M':
		return '25'
	else:
		return x


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
					chromosome = swapChrom(chromosome)
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
		if sortOption == 'CHROMOSOME':
			all = [len(output[x]) for x in output]
			numSNPs = sum(all)
		if sortOption == 'RSID' or sortOption == 'POSITION':
			numSNPs = len(output)
		printMsg("Success! SNP dictionary obtained by %s (%s SNPs)" % (sortOption, numSNPs))
		return output 


def parse_reference(file="", sortOption=""):
	"""
	Parses SNPs of user from locally saved file (.txt format) 
	that was downloaded through user upload or 23andme access. 

	Returns one of ...
	- Dictionary of all 23andme SNPs with RSID key
	- Dictionary of all 23andme SNPs with CHROMSOME key to a 
	dictionary of each SNP in a chromosome with POSITION key
	- Dictionary of all 23andme SNPs with POSITION key

	"""
	if os.path.exists(file):
		f = open(file, 'r')
		
		output = {}
		if sortOption == CHROMOSOME:			
			for chr in CHROMOSOME_LIST:
				output[chr] = {} 
		
		numSNPs = 0
		for line in f:
			line = line.strip()
			if line[0] != "#":
				chromosome, position, rsid, genotype = line.split()
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
					chromosome = chromosome[3:]
					chromosome = swapChrom(chromosome)
					output[chromosome][position] = {
						RSID: rsid,
						GENOTYPE: genotype
						}

		print "Total SNPs: %d" % numSNPs
		f.close()
		return output 
	else:
		print "Path <%s> not found" % file
		return {}


def _referenceObject(SNPfile, sortOption):
	"""
	Returns a SNP dictionary in the specified sorting format.
	Options are: [RSID, CHROMOSOME, POSITION]
	"""
	if not any([sortOption != option for option in sortOptions]):
		raise ValueError, "Please select a valid sortOption: RSID, CHROMOSOME, or POSITION"

	output = parse_reference(SNPfile, sortOption)
	if output == {}:
		printMsg("Error: verify inputs")
		return {}
	else:
		all = [len(output[chr]) for chr in output]
		numSNPs = sum(all)
		printMsg("Success! SNP dictionary obtained by %s (%s SNPs)" % (sortOption, numSNPs))
		return output 

def parse_scoredAlleles_file(file="", userObjID=""):
	"""
	Parses SNPs of user from locally saved file (.txt format) 
	that was downloaded through user upload or 23andme access. 

	Returns one of ...
	- Dictionary of all 23andme SNPs with RSID key
	- Dictionary of all 23andme SNPs with CHROMSOME key to a 
	dictionary of each SNP in a chromosome with POSITION key
	- Dictionary of all 23andme SNPs with POSITION key

	"""
	k = 0
	if os.path.exists(file):
		f = open(file, 'r')
		
		output = {}

		blue = '<span class="label label-primary">'
		orange = '<span class="label label-warning">'
		gray = '<span class="label label-default">'
		green = '<span class="label label-success">'
		DB_SNP = 'http://www.ncbi.nlm.nih.gov/SNP/snp_ref.cgi?rs='
		SNPEDIA = 'http://www.snpedia.com/index.php/'
		
		for chr in CHROMOSOME_LIST:
			output[chr] = {} 
		
		numSNPs = 0
		i = 0 
		for line in f:
			line = line.strip()
			if line[0] != "#":
				chr, rsid, pos, refAllele, genotype, variant, score = line.split()
				if genotype == 'II' or genotype == 'I':
					tag = 'insertion'
					html_tag = blue
				elif genotype == 'DD' or genotype == 'D':
					tag = 'deletion'
					html_tag = blue
				elif genotype == 'DI' or genotype == 'ID':
					tag = 'indel'
					html_tag = blue
				else:
					tag = 'normal'
					if variant == score:  # '-', '-'
						html_tag = ''
					elif any(score == x for x in [1, 2]) and variant == '-':
						html_tag = gray
					elif score == 1:
						html_tag = green
					elif score == 0:
						html_tag = orange
					else:
						html_tag = ''

				# if not db_model.UsersSNPCollection.find({'_id': rsid}).count():
				if userObjID != '':
					numSNPs += 1
					chr = swapChrom(chr)		## Swaps from 'X' to '23', etc.
					data = {
						'_id': rsid,
						CHROMOSOME: chr,
						POSITION: pos,
						GENOTYPE: genotype,
						RSID: rsid,
						'REF': refAllele,
						'VARIANT': variant,
						'GENOTYPE_TAG': tag,
						'MATCH_SCORE': score,
						'SNPEDIA_LINK': SNPEDIA+rsid,
						'DB_SNP_LINK': DB_SNP+rsid,
						'DATE': datetime.datetime.now().ctime(),
						'USER_ID': userObjID,
						'HTML': html_tag
					}
					output[chr][pos] = data

				if numSNPs == db_model.CHECKLIST[k]:
					print "[x] Check %s-th complete. %s SNPs parsed so far. %s SNPs added to ScoredAllelesObject." % (k+1, db_model.CHECKLIST[k], numSNPs)
					k += 1 

		print "Total SNPs: %d" % numSNPs
		f.close()
		return output 
	else:
		print "Path <%s> not found" % file
		return {}


def _scoredAllelesObject(file, userObjID):
	"""
	data is a dictionary to be inserted to make a new mongodb document for an rsid

	Returns a SNP dictionary of format dict[chr][pos] = data 
	"""
	sortOption = 'CHROMOSOME'

	if not any([sortOption != option for option in sortOptions]):
		raise ValueError, "Please select a valid sortOption: RSID, CHROMOSOME, or POSITION"

	output = parse_scoredAlleles_file(file=file, userObjID=userObjID)
	if output == {}:
		printMsg("Error: verify inputs")
		return {}
	else:
		all = [len(output[chr]) for chr in output]
		numSNPs = sum(all)
		printMsg("_scoredAllelesObject: SNP dictionary obtained by %s (%s SNPs) \n\t from file=%s for mongoDB userID=%s" % (sortOption, numSNPs, file, userObjID))
		return output 


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


def stream2SSfile(RefSNPdict, UserSNPdict, filename):
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


def stream2SRSIDfile(input, filename):
	"""
	Streams input data containing SNP rsid's to an output (filename) file
	containing just the RSID values in each line. 
	"""
	pass


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
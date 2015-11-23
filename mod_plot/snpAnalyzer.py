import json

RSID = 'RSID'
# Value... (fieldnames)
DESCRIPTION = 'DESCRIPTION'
CHROMOSOME = 'CHROMOSOME'
POSITION = 'POSITION'
GENOTYPE = 'GENOTYPE'
DATE = 'DATE'


def add_rsidValues(chromosome="", position=0, genotype=""):
	''' 
	
	''' 
	new_snp = {}
	new_snp[CHROMOSOME] = chromosome
	new_snp[POSITION] = position
	new_snp[GENOTYPE] = genotype
	return new_snp


def parse_23andmeFile(username="", user_snp_file=''):
	"""
	Parses SNPs of user from locally saved file (.txt format) 
	that was downloaded through user upload or 23andme access. 

	"""
	print "in"

	if "" != user_snp_file:
		f = open(user_snp_file, 'r')
		
		user_rsIDs = {}
		user_rsIDs_byChromosome = {}
		for i in range(1,23):
			user_rsIDs_byChromosome[str(i)] = {}
		user_rsIDs_byChromosome['X'] = {}
		user_rsIDs_byChromosome['Y'] = {}
		user_rsIDs_byChromosome['MT'] = {}

		numSNPs = 0
		for line in f:
			line = line.strip()
			if line[0] != "#":
				line_data = line.split()
				rsid = line_data[0]
				chromosome = line_data[1]
				position = line_data[2]
				genotype = line_data[3]

				numSNPs += 1
				user_rsIDs[rsid] = add_rsidValues(chromosome=chromosome, \
					position=position, genotype=genotype)
				
				user_rsIDs_byChromosome[chromosome][position] = {RSID: rsid, GENOTYPE: genotype}

		print "Total: %d" % numSNPs
		f.close()

		chr_num = range(1,23) + ['X'] + ['Y'] + ['MT']

		### MAKE BED FILE
		outfile = open('bed/%s_snps_bed.txt' % (username), 'w')
		for chr in chr_num:
			positions = user_rsIDs_byChromosome[str(chr)].keys()
			positions.sort()
			for pos in positions:
				start = int(pos)
				end = int(pos)+1
				rsid = user_rsIDs_byChromosome[str(chr)][pos][RSID]
				outfile.write('chr%s\t%d\t%d\t%s\n' % (str(chr), start, end, rsid))
		outfile.close()

	else:
		print "Path <%s> not found" % user_snp_file

parse_23andmeFile('teyden', 'data/snps/snps_teyden.txt')
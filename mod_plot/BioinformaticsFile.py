import parseNstream
import os

##############
RSID = 'RSID'
# Value... (fieldnames)
DESCRIPTION = 'DESCRIPTION'
CHROMOSOME = 'CHROMOSOME'
POSITION = 'POSITION'
GENOTYPE = 'GENOTYPE'
DATE = 'DATE'


class BioinformaticsFile:
	"""
	The object for a bioinformatics file format. 

	Allows instant manipulation...
	- parsing
	- print out a single line in a file via
		- search by position
		- search by rsID


	FOR NOW: The only format it takes is the 23andme file. Output format options
	are SS, VCF, HapMap and RSIDs (1 rsid per line), and eventually BED.
	
	"""

	def __init__(self, format, inputPath):
		"""
		Constructs the bioinformatics file using the inputPath

		The input file will have these minimum requirements:
		- rsID
		- chromosome
		- position
		- sample genotype

		If input filetype is not specified, then send through parseNstream to predict filetype? 
		"""
		if os.path.exists(inputPath):
			self.inputPath = inputPath
			self.referencePath = '/Volumes/teyden/BIOINFORMATICS/23andme2vcf/23andme_v4_hg19_ref.txt'
			self.genome = parseNstream._23andmeObject(self.inputPath, sortOption='CHROMOSOME')  ## 
			self.chrList = [ '%s' % i for i in range(1,26)] # + ['X', 'Y', 'MT']

	def _getEndpoint(self, format=''):
		# assert() to make sure nothing invalid passes through
		if format.upper() == 'VCF':
			return '.vcf'
		elif format.upper() == 'BED':
			return '.bed'
		elif format.upper() == 'SS':
			return '.txt'
		elif format.upper() == 'RSID':
			return '.txt'
		else:
			print "Please enter a valid format"

	def _stream2SSfile(self, RefSNPdict):
		"""
		Makes simple SNP file for analysis by SNPhylo tree maker

		** 
		- SNPhylo is case-sensitive
		- Also requires single genotype mutation, represent single alleles different from the ref only

		### BASIC FORMAT:
		#chrNum 	position 	Ref 	SampleID1	... 
		1		1000		A 		A 		T 
		"""
		F = open(self.outputPath, 'w')
		F.write('#Chrom\tPos\tRef\tSampleID1\n')
		for chr in self.chrList:
			positions = RefSNPdict[chr].keys()
			positions.sort()
			for pos in positions:
				refGenotype = RefSNPdict[chr][pos][GENOTYPE].upper()
				if pos in self.genome[chr]:
					if len(self.genome[chr][refPos][GENOTYPE]) > 1:
						if refGenotype.lower() == self.genome[chr][refPos][GENOTYPE][0].lower():
							sample = self.genome[chr][refPos][GENOTYPE][1]
						else:
							sample = self.genome[chr][refPos][GENOTYPE][0]
					else:
						sample = self.genome[chr][refPos][GENOTYPE]
					F.write('%s\t%s\t%s\t%s\n' % (chr, pos, refGenotype, sample))
		F.close()
		parseNstream.printMsg("Completed streaming to Simple SNP file format (path=%s)" % self.outputPath)


	def _stream2SRSIDfile(self):
		"""
		Streams input data containing SNP rsid's to an output (filename) file
		containing just the RSID values in each line. 
		"""
		F = open(self.outputPath, 'w')
		for chr in self.genome:
			
			for pos in self.genome[chr]:
				F.write('%s\n' % self.genome[chr][pos][RSID])

		F.close()
		parseNstream.printMsg("Completed streaming to simple RSID file format (path=%s)" % self.outputPath)


	def _stream2VCFfile(self):
		pass

	def _stream2HapMapfile(self):
		pass

	def _stream2BEDfile(self):
		pass

	def convertTo(self, format=''):
		"""
		Takes a string indiciating file format and creates a file of that file format
		from the conversion of the original file format

		Returns none
		"""
		fileEndpoint = self._getEndpoint(format)
		self.outputPath = 'output/conversionTo_'+format+fileEndpoint

		if format.upper() == 'VCF':
			self._stream2VCFfile()
		elif format.upper() == 'BED':
			self._stream2BEDfile()
		elif format.upper() == 'SS':
			# Input and output of files should also be via the DB
			ref_snps = parseNstream._referenceObject(self.referencePath, 'CHROMOSOME')  ## parseNstream functions to be added as methods to a Genome object
			self._stream2SSfile(ref_snps)
		elif format.upper() == 'RSID':
			self._stream2SRSIDfile()
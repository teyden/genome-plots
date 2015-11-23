# Key...
RSID = 'RSID'
# Value... (fieldnames)
DESCRIPTION = 'DESCRIPTION'
CHROMOSOME = 'CHROMOSOME'
GENE = 'GENE'
ALLELES = 'ALLELES'
DATE = 'DATE'

class SNP:

	def __init__(self, rsid="", description="", chromosome=0, gene="", alleles=[]):
		self.rsid = rsid
		self.description = description
		self.chromosome = chromosome
		self.gene = gene
		self.alleles = alleles
		
		self._snp = {}
		self._snp[RSID] = rsid
		self._snp[DESCRIPTION] = description
		self._snp[CHROMOSOME] = chromosome
		self._snp[GENE] = gene
		self._snp[ALLELES] = alleles

	def __repr__(self):
		pass

	def __str__(self):
		return 'SNP(%s, %s, %d, %s, [%s, %s, %s])' % \
		(self.rsid, self.description, self.chromosome, self.gene, \
			self.alleles[0], self.alleles[1], self.alleles[2])

	def __cmp__(self, x):
		"""
		cmp(snp1, snp2)
		"""
		return type(self) == type(x)

	def json_without_RSID(self):
		"""
		In cases where a SNP needs to be inserted into a DB, the RSID
		is used as the KEY, and this resulting dictionary is the value. Hence,
		removing RSID from the original self._snp will avoid having any
		repetitive instances of RSID. 
		"""
		mod_json = {}
		for key in self._snp:
			if key != RSID:
				mod_json[key] = self._snp[key]
		return mod_json

	def json(self):
		"""
		Returns json form of the SNP object. 
		"""
		return self._snp

	def changeData(self, rsid="", description="", chromosome=0, gene="", alleles=[]):
		"""
		Change data members to an SNP object. All are set to default. 
		Can change any number of data members at once. If no input is
		given then nothing is changed in the SNP object.
		"""
		if rsid != "":
			self.rsid = rsid
		if description != "":
			self.description = description
		if chromosome != 0:
			self.chromosome = chromosome
		if gene != "":
			self.gene = gene
		if alleles != []:
			self.alleles = alleles
		else:
			return


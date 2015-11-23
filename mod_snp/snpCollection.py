import os
import os.path
import csv
import datetime

from app.mod_site.models import *

# Set global default CSV path 
DEFAULT_CSV_PATH = 'data/snpCollection.csv'
DATE = 'date'

# Global constants for CSV and SNP fieldnames 

# Key...
RSID = 'RSID'
# Value... (fieldnames)
DESCRIPTION = 'DESCRIPTION'
CHROMOSOME = 'CHROMOSOME'
GENE = 'GENE'
ALLELES = 'ALLELES'
DATE = 'DATE'


class snpCollection: 
	'''
	a snpCollection object is for storing SNPs for piping 
	to a CSV which can be transferred to the db. 

	call save_toCSV at the end of a session to add all SNPs
	added to the snpCollection object to a local CSV file

	#######
	Usage is shown in test_snpCollection.py, however
	short outline here:
		
		# JSON of rsIDs
		D = {'rs1799990': {'ALLELES': ['AA', 'AG', 'GG'], 
			'GENE': 'PRNP', 'DESCRIPTION': 'memory (long-term; logical)', 
			'CHROMOSOME': 22},  'rs1800497': {'ALLELES': 
			['AA', 'AG', 'GG'], 'GENE': 'ANKK1', 'DESCRIPTION': 
			'Addictive behaviours (gambling, alcoholism, smoking...)', 
			'CHROMOSOME': 11}
			}  

		new_snps = snpCollection()
		new_snps.insertBulk(D)  # Can add one by one (.add(), or .insertRaw())
		new_snps.setCSVpath("new_snps.csv")
		new_snps.save_toCSV()
	'''

	def __init__(self, path=DEFAULT_CSV_PATH):
		'''
		Each RSID is a unique key to an SNP object value
		'''
		# A single SNP object format. 
		self._snp = {
			DESCRIPTION: '',
			CHROMOSOME: 0,
			GENE: '',
			ALLELES: []
		}

		# Collection of { uniq_rsid ==> { ._snp } }
		# self._storage[uniq_rsid] = self._snp
		self._storage = {}

		# Set any additional variables
		self._current_CSVpath = self.setCSVpath()
		self._date = datetime.datetime.now().ctime()
		self._writer = ''


	def printCurrentSession(self):
		''' printCurrentSession() prints out each snp in ._storage
		'''
		for rsid in self._storage:
			print "\n   " + rsid + ""
			print "\t %s: %s" % (DESCRIPTION, self._storage[rsid][DESCRIPTION])
			print "\t %s: %s" % (CHROMOSOME, self._storage[rsid][CHROMOSOME])
			print "\t %s: %s" % (GENE, self._storage[rsid][GENE])
			print "\t %s: %s" % (ALLELES, self._storage[rsid][ALLELES])


	def size(self):
		count = 0
		with open(self._current_CSVpath) as csvfile:
			reader = csv.DictReader(csvfile)
			for row in reader:
				count += 1
		return count + len(self._storage)


	def _anyEmptyFields(self, snp):
		''' _anyEmptyFields() outputs True if any snp field input is empty,
		else, False. An snp added to the collection cannot 
		have any missing field values. 
		'''
		if snp[DESCRIPTION] == "" or snp[CHROMOSOME] == "" or snp[GENE] == "" or snp[ALLELES] == "":
			return True 
		else:
			return False	


	def isValid(self, snp, uniq_rsid="rsid"):
		''' isValid() ensures that every snp added to self._storage has valid structure
		'''
		if type(uniq_rsid) != type('') or type(snp[DESCRIPTION]) != type('') or type(snp[GENE]) != type(''):
			raise TypeError, "'RSID', 'DESCRIPTION', and 'GENE' must be StringType"

		if type(snp[CHROMOSOME]) != type(1):
			raise TypeError, "'CHROMOSOME' must be IntType"

		if type(snp[ALLELES]) != type([]): 
			raise TypeError, "'ALLELES' must be ListType"

		if uniq_rsid == "" or self._anyEmptyFields(snp) == True:
			raise ValueError, "Cannot have empty input values"		
		else:
			print "isValid():  PASS - valid SNP structure"
			return True


	def make_snp(self, description, chromosome, gene, alleles):
		''' make_snp() creates a new snp, checks structure validity,
		and returns it if isValid is True
		''' 
		new_snp = {}
		new_snp[DESCRIPTION] = description
		new_snp[CHROMOSOME] = chromosome
		new_snp[GENE] = gene
		new_snp[ALLELES] = alleles
		if self.isValid(new_snp):
			return new_snp


	def make_dict_ofSNPs(self, opt_dict={}):
		'''
		Can add to existing dictionary (opt_dict != {}) or start a new one.
		'''
		N = int(raw_input("Total SNP's to add: "))
		for x in range(N):
			try:
				_rsid = raw_input("RSID: ")
				_description = raw_input("DESCRIPTION: ")
				_chromosome = int(raw_input("CHROMOSOME: "))
				_gene = raw_input("GENE: ")
				_alleles = range(3)
				print "ALLELES: "
				for i in range(3):
					_alleles[i] = raw_input("(%d): " % (i+1))
			except (ValueError, TypeError):
				print "You put in the wrong type."
			else:
				opt_dict[_rsid] = self.make_snp(_description, _chromosome, _gene, _alleles)
		return opt_dict
		

	def _add(self, uniq_rsid, description, chromosome, gene, alleles):
		'''_add() adds new snp to ._storage if _add paramaters are valid
		- Use when adding snp's in same session. Does not save beyond session end; 
		call save_toCSV() before you end the session to save.
		'''	
		try: 
			# First make a new snp structure (which checks SNP validity too)
			snp = self.make_snp(description, chromosome, gene, alleles)
		except (ValueError, TypeError):
			print "Cannot make or add snp - invalid field input"
		else:
			# If it is, and doesn't exist in the collection, then add it.
			if uniq_rsid not in self._storage: 
				# Store in local variable; call to ._snp gives last snp added
				self._snp = snp
				# Store in ._storage collector
				self._storage[uniq_rsid] = snp
				print "%s ==> %s" % (uniq_rsid, str(snp))
			else:
				print "SNP already exists: " + str(self._storage[uniq_rsid])


	def _pop(self, uniq_rsid):
		''' _pop() removes snp with rsid (uniq_rsid) from collection
		and returns list of format [rsid, snp]. If rsid DNE in collection,
		then returns empty list.
		'''
		if uniq_rsid in self._storage:
			return [uniq_rsid, self._storage.pop(uniq_rsid)]
		else:
			print "SNP does not exist in dictionary"
			return []


	def setCSVpath(self, path=DEFAULT_CSV_PATH):
		''' _setCSVpath() sets ._current_CSVpath to 
		path (optional) parameter. If not given, then ._current_CSVpath 
		is set to default_CSVpath.
		''' 
		self._current_CSVpath = path
		''' Sets new CSV path; redirects 'w' and 'r' to new file
		'''
		if os.path.isfile(path):
			print "CSV file path is set."
		else:
			print "File path doesn't exist."
			answer = raw_input("Make file path (%s)? y/n: " % path)
			if answer == "y":
				os.system("touch %s" % path)
				print "File path redirected to new path variable."
			else:
				self._current_CSVpath = DEFAULT_CSV_PATH
				print "File path set to default."


	def save_toCSV(self):
		''' save_toCSV() inserts every element in ._storage to 
		locally stored CSV file in data/
		'''
		with open(self._current_CSVpath, 'w') as csvfile:
			fieldnames = [RSID, DESCRIPTION, CHROMOSOME, GENE, ALLELES, DATE]
			self._writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

			# Sets CSV headers with fieldnames
			self._writer.writeheader()
			# Sets CSV headers with fieldnames
			for key in self._storage:
				self._writer.writerow({
					RSID: key, 
					DESCRIPTION: self._storage[key][DESCRIPTION], 
					CHROMOSOME: self._storage[key][CHROMOSOME], 
					GENE: self._storage[key][GENE], 
					ALLELES: self._storage[key][ALLELES], 
					DATE: self._date})
				print "save_toCSV() Status ||| %s added to CSV." % key

				#for el in self._storage[key]:
					#self._writer.writerows(el)

	def printFromCSV(self):
		""" printFromCSV() prints each row in the CSV 
		"""
		with open(self._current_CSVpath) as csvfile:
			reader = csv.DictReader(csvfile)
			print reader
			for row in reader:
				print "%s, %s, %s, %s, %s, %s" % (row[RSID], row[DESCRIPTION], row[CHROMOSOME], row[GENE], str(row[ALLELES]), row[DATE])


	def insertRaw(self): 
		# Starts rsid stream session through user input 
		N = int(raw_input("Total SNP's to add: "))

		for x in range(N):
			try:
				_rsid = raw_input("RSID: ")
				_description = raw_input("DESCRIPTION: ")
				_chromosome = int(raw_input("CHROMOSOME: "))
				_gene = raw_input("GENE: ")
				_alleles = range(3)
				print "ALLELES: "
				for i in range(3):
					_alleles[i] = raw_input("(%d): " % (i+1))
			except (ValueError, TypeError):
				print "You put in the wrong type."
			else:
				self._storage[_rsid] = self.make_snp(_description, _chromosome, _gene, _alleles)
				print self._storage
		self.save_toCSV()


	def insertBulk(self, dict_SNPs={}):
		''' insertBulk() adds all valid snp's from dict_SNPs.
		Skips over invalid ones and prints out error statement.

		- Ensures no overwriting any snp's 
		- Ensures 
		'''
		count = 0
		if {} == dict_SNPs:
			insertRaw(self._storage)
		for key in dict_SNPs:
			if key not in self._storage:
				# Make sure each new SNP entry is of proper structure
				try: 
					self.isValid(dict_SNPs[key], key)
				except (TypeError, ValueError): 
					print "insertBulk():  ERROR - SNP field TypeError. Please check SNP field values. " + \
					"%s: " % key + str(dict_SNPs[key])
					# print "%s: %s" % (key, str(self.dict_SNPs[key]))
				else:
					count += 1 
					self._storage[key] = dict_SNPs[key]
		print "insertBulk():  Added %d new SNP entries." % count





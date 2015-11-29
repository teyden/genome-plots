from parser import _23andmeObject
from scoreAlleles import scoreAlleles

import os
from flask import request 
from pymongo import MongoClient

# Need to hide these.
CLIENT_ID = 'e1c168d2cbd3383adeab1705880617b0'
CLIENT_SECRET = '17dfae96a04efe3f534202037784526a'

# mongo_uri = os.environ['MONGOLAB_URI']
MONGOLAB_URI = 'mongodb://heroku_app36742821:t5n5280bq0afndja4psmb7kbap@ds061288.mongolab.com:61288/heroku_app36742821'
MONGO_DATABASE_STR = MONGOLAB_URI.split('/')[-1] 

# Print client ==> 'MongoClient('heroku_app36742821', 27017) or MongoClient('ds061288.mongolab.com', 61288)'
# Print db ==> 'Database(MongoClient('ds061288.mongolab.com', 61288), u'heroku_app36742821')'

client = MongoClient(MONGOLAB_URI) 
mongo_db = client[MONGO_DATABASE_STR] 

ReferenceSNPCollection = mongo_db.ReferenceSNPCollection
# ID's are mapped to users_collection id's. Contains the SNPs of a user from user_collection
UsersSNPCollection = mongo_db.UsersSNPCollection
# Collection of all users registered (through /signup)
users_collection = mongo_db.users_collection
# Collection of rsIDs inputted by owner
rsIDs_collection = mongo_db.rsIDs_collection
# Collection of messages sent from user / visitor
suggestMsgs_collection = mongo_db.suggestMsgs_collection
# Collection of popover data
PopoverData = mongo_db.PopoverData
AccessCodes = mongo_db.AccessCodes

# Distinction between using blah_collection vs. blah ?  [*][*][*]
users = users_collection.users
rsIDs = rsIDs_collection.rsIDs 
suggestMsgs = suggestMsgs_collection.suggestMsgs


# UserChromosomeDict = _23andmeObject('../../BIO_DATA/raw23andme_SNPs_teyden.txt', 'RSID')

# for item in rsIDs.find():
# 	if item['RSID'] not in UserChromosomeDict:
# 		print item['RSID']


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

def addRefRSIDs_toDB(file):
	"""
	file is the reference HG file used for 23andme genotyping

	adds every reference snp to the db 
	"""
	if os.path.exists(file):
		f = open(file, 'r')

		numSNPs = 0
		for line in f:
			line = line.strip()
			if line[0] != "#":
				chromosome, position, rsid, genotype = line.split()
				numSNPs += 1

				ReferenceSNPCollection.insert({
					'_id': rsid,
					CHROMOSOME: chromosome,
					POSITION: position, 
					GENOTYPE: genotype
					})

		print "%s SNPs added to ReferenceSNPCollection" % numSNPs
		f.close()
	else:
		print "Path <%s> not found" % file

# addRefRSIDs_toDB(DEFAULT_REF_FILEPATH)

def addUsersRSIDs_toDB(file, userObjID=''):
	"""
	Adds every user snp from the file output of scoreAlleles() to UsersSNPCollection
	as a JSON. The object id value for each SNP JSON collection is the same object
	id as the user's object id in users_collection.
	
	The file input MUST be the file output from scoreAlleles().

	"""
	if userObjID == '':
		userObjID = raw_input('Please enter a user ID: ')

	UsersSNPCollection.insert({ '_id': userObjID, snps: {} })
	if os.path.exists(file):
		f = open(file, 'r')

		numSNPs = 0
		for line in f:
			line = line.strip()
			if line[0] != "#":
				cchr, rsid, pos, refAllele, sampleAllele, variant, score = line.split()
				numSNPs += 1

				# ReferenceSNPCollection.insert({
				# 	'_id': userObjID,
				# 	RSID =  
				# 	CHROMOSOME: chr,
				# 	POSITION: position, 
				# 	GENOTYPE: genotype
				# 	})

		print "%s SNPs added to ReferenceSNPCollection" % numSNPs
		f.close()
	else:
		print "Path <%s> not found" % file

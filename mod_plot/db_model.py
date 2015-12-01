from parseNstream import _23andmeObject, printMsg
# from scoreAlleles import scoreAlleles

import datetime 
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
UsersSNPCollection = mongo_db.SNPCollection.users
ChromosomeCollection = mongo_db.ChromosomeCollection
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

				if not ReferenceSNPCollection.find({ '_id': rsid }):				
					ReferenceSNPCollection.insert({
						'_id': rsid,
						CHROMOSOME: chromosome,
						POSITION: position, 
						GENOTYPE: genotype
						})

		print "%s SNPs added to ReferenceSNPCollection" % numSNPs
		f.close()
	else:
		print "Path <%s> not found" % fieldnames

# addRefRSIDs_toDB(DEFAULT_REF_FILEPATH)

CHECKLIST = [1,
 10001,
 20001,
 30001,
 40001,
 50001,
 60001,
 70001,
 80001,
 90001,
 100001,
 110001,
 120001,
 130001,
 140001,
 150001,
 160001,
 170001,
 180001,
 190001,
 200001,
 210001,
 220001,
 230001,
 240001,
 250001,
 260001,
 270001,
 280001,
 290001,
 300001,
 310001,
 320001,
 330001,
 340001,
 350001,
 360001,
 370001,
 380001,
 390001,
 400001,
 410001,
 420001,
 430001,
 440001,
 450001,
 460001,
 470001,
 480001,
 490001,
 500001,
 510001,
 520001,
 530001,
 540001,
 550001,
 560001,
 570001,
 580001]

def addUsersRSIDs_toDB(file, userObjID=''):
	"""
	Adds every user snp from the file output of scoreAlleles() to UsersSNPCollection
	as a JSON. The object id value for each SNP JSON collection is the same object
	id as the user's object id in users_collection.
	
	file: a file output from scoreAlleles().
	userObjID: a user id from the users_collection.users

	"_id": {
        "$oid": "555a83687a349b6910bdff6c"
    }

	"""
	COUNT = 0
	k = 0

	if userObjID == '':
		userObjID = raw_input('Please enter a user ID: ')

	if os.path.exists(file):
		f = open(file, 'r')

		numNewSNPs = 0
		for line in f:
			line = line.strip()
			if line[0] != "#":
				chr, rsid, pos, refAllele, genotype, variant, score = line.split()
				COUNT += 1

				blue = '<span class="label label-primary">'
				orange = '<span class="label label-warning">'
				gray = '<span class="label label-default">'
				green = '<span class="label label-success">'

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

				# if not UsersSNPCollection.find({ '_id': rsid }):	
				if not UsersSNPCollection.find({'_id': rsid}).count():  # = 1 if exists, 0 if doesn't
					numNewSNPs += 1
					UsersSNPCollection.insert({
						'_id': rsid,
						CHROMOSOME: chr,
						POSITION: pos,
						GENOTYPE: genotype,
						RSID: rsid,
						'REF': refAllele,
						'VARIANT': variant,
						'GENOTYPE_TAG': tag,
						'MATCH_SCORE': score,
						'SNPEDIA_LINK': 'http://www.snpedia.com/index.php/'+rsid,
						'DB_SNP_LINK': 'http://www.ncbi.nlm.nih.gov/SNP/snp_ref.cgi?rs='+rsid,
						'DATE': datetime.datetime.now().ctime(),
						'USER_ID': userObjID,
						'HTML': html_tag
						})

				if COUNT == CHECKLIST[k]:
					print "[x] Check %s-th complete. %s SNPs parsed so far. %s new SNPs added to the DB. %s parsed SNPs were already in the DB." % (k+1, CHECKLIST[k], numNewSNPs, COUNT-numNewSNPs)
					k += 1 

		print "[x] Last check complete. %s total SNPs added to the UsersSNPCollection." % (k+1, CHECKLIST[k])
		f.close()
	else:
		print "Path <%s> not found" % file

addUsersRSIDs_toDB(DEFAULT_OUTPUT_FILEPATH, userObjID="555a83687a349b6910bdff6c")

# usersSNPs = [snpColl for snpColl in UsersSNPCollection.find()]
# count = 0
# nadas = []
# for snp in UsersSNPCollection.find():
# 	if 'HTML' in snp:
# 		count += 1
# 		if snp['HTML'] == '<span class="label label-danger">':
# 			UsersSNPCollection.update_one(
# 				{ '_id': snp['RSID'] }, 
# 				{ '$set': 
# 					{
# 						"HTML": '<span class="label label-primary">'
# 					}
# 				}
# 			)
# 		elif snp['HTML'] == '<span class="label label-primary">' and snp['MATCH_SCORE'] == '2' and snp['GENOTYPE_TAG'] == 'normal':
# 			UsersSNPCollection.update_one(
# 				{ '_id': snp['RSID'] }, 
# 				{ '$set': 
# 					{
# 						"HTML": '<span class="label label-default">'
# 					}
# 				}
# 			)
# 		elif snp['HTML'] == '<span class="label label-primary">' and snp['MATCH_SCORE'] == '0' and snp['GENOTYPE_TAG'] == 'normal':
# 			UsersSNPCollection.update_one(
# 				{ '_id': snp['RSID'] }, 
# 				{ '$set': 
# 					{
# 						"HTML": '<span class="label label-warning">'
# 					}
# 				}
# 			)
# 	else:
# 		pass

	# if 'HTML' not in snp:
	# 	count += 1
	# 	if snp['MATCH_SCORE'] == '0' and snp['GENOTYPE_TAG'] == 'normal':
	# 		UsersSNPCollection.update_one(
	# 			{'_id': snp['RSID']},
	# 			{ '$set': 
	# 				{
	# 					"HTML": '<span class="label label-warning">'	# Orange
	# 				}
	# 			}
	# 		)
	# 	elif snp['MATCH_SCORE'] == '1' and snp['GENOTYPE_TAG'] == 'normal':
	# 		UsersSNPCollection.update_one(
	# 			{ '_id': snp['RSID'] }, 
	# 			{ '$set': 
	# 				{
	# 					"HTML": '<span class="label label-success">'	# Green
	# 				}
	# 			}
	# 		)
	# 	elif snp['MATCH_SCORE'] == '2' and snp['GENOTYPE_TAG'] == 'normal':
	# 		UsersSNPCollection.update_one(
	# 			{ '_id': snp['RSID'] }, 
	# 			{ '$set': 
	# 				{
	# 					"HTML": '<span class="label label-default">'
	# 				}
	# 			}
	# 		)
	# 	elif snp['GENOTYPE_TAG'] == 'deletion' or snp['GENOTYPE_TAG'] == 'insertion' or snp['GENOTYPE_TAG'] == 'indel':
	# 		UsersSNPCollection.update_one(
	# 			{ '_id': snp['RSID'] }, 
	# 			{ '$set': 
	# 				{
	# 					"HTML": '<span class="label label-danger">'
	# 				}
	# 			}
	# 		)
	# 	else:
	# 		nadas.append(snp)

printMsg("SNP's updated = %s; SNP's not updated and don't know why = %s, SNP's already updated = %s" % (len(usersSNPs)-count, len(nadas), count))
from scoreAlleles import scoreAlleles
import parseNstream
import db_model 

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

	# Implement assertion for file type, ensure all column headers are accurate
	ScoredSNPdict = parseNstream._scoredAllelesObject(file, userObjID)

	if userObjID == '':
		userObjID = raw_input('Please enter a user ID: ')

	for chr in parseNstream.CHROMOSOME_LIST:
		positions = ScoredSNPdict[chr].keys()
		positions.sort()

		# Iterates through each chromosomal position adding new RSIDS to DB in ascending order
		for position in positions:
			rsid = ScoredSNPdict[chr][position][RSID]

			if not UsersSNPCollection.find({'_id': rsid}).count():
				data = ScoredSNPdict[chr][position]
				newNumSNPs += 1
				UsersSNPCollection.insert(data)

			if COUNT == db_model.CHECKLIST[k]:
				print "[x] Check %s-th complete. %s SNPs parsed so far. %s new SNPs added in total. %s parsed SNPs were already in the DB." % (k+1, CHECKLIST[k], numNewSNPs, COUNT-numNewSNPs)
				k += 1 

		print "[x] Last check complete. %s total SNPs added to the UsersSNPCollection." % (k+1, CHECKLIST[k])
		f.close()
	else:
		print "Path <%s> not found" % file


if name == '__main__':

	# scoreAlleles(DEFAULT_REF_FILEPATH, DEFAULT_USER_FILEPATH)
	addUsersRSIDs_toDB(DEFAULT_OUTPUT_FILEPATH, userObjID="555a83687a349b6910bdff6c")


	# LIMIT = 2
	# while LIMIT < 1:
	# 	for snp in UsersSNPCollection.find():
	# 		if 'HTML' in snp:
	# 			count += 1
	# 			if snp['HTML'] == '<span class="label label-danger">':
	# 				UsersSNPCollection.update_one(
	# 					{ '_id': snp['RSID'] }, 
	# 					{ '$set': 
	# 						{
	# 							"HTML": '<span class="label label-primary">'
	# 						}
	# 					}
	# 				)
	# 			elif snp['HTML'] == '<span class="label label-primary">' and snp['MATCH_SCORE'] == '2' and snp['GENOTYPE_TAG'] == 'normal':
	# 				UsersSNPCollection.update_one(
	# 					{ '_id': snp['RSID'] }, 
	# 					{ '$set': 
	# 						{
	# 							"HTML": '<span class="label label-default">'
	# 						}
	# 					}
	# 				)
	# 			elif snp['HTML'] == '<span class="label label-primary">' and snp['MATCH_SCORE'] == '0' and snp['GENOTYPE_TAG'] == 'normal':
	# 				UsersSNPCollection.update_one(
	# 					{ '_id': snp['RSID'] }, 
	# 					{ '$set': 
	# 						{
	# 							"HTML": '<span class="label label-warning">'
	# 						}
	# 					}
	# 				)
	# 		else:
	# 		pass
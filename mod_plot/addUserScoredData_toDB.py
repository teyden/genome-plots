import parseNstream
import db_model
import datetime
import os 

DEFAULT_SCORED_FILEPATH = db_model.DEFAULT_SCORED_FILEPATH
DEFAULT_REF_FILEPATH = db_model.DEFAULT_REF_FILEPATH
DEFAULT_USER_FILEPATH = db_model.DEFAULT_USER_FILEPATH

# Value... (fieldnames)
RSID = 'RSID'
DESCRIPTION = 'DESCRIPTION'
CHROMOSOME = 'CHROMOSOME'
POSITION = 'POSITION'
GENOTYPE = 'GENOTYPE'
DATE = 'DATE'

def f(x):
	if any(chr == x for x in ['1', '2', '3', '4', '5']):
		signal += 1
		return db_model.CollectbyChromosome_1to5
	elif any(chr == x for x in ['6', '7', '8', '9', '10', '11']):
		signal += 1
		return db_model.CollectbyChromosome_6to11 
	elif any(chr == x for x in ['12', '13', '14', '15', '16', '17']):
		signal += 1
		return db_model.CollectbyChromosome_12to17 
	elif any(chr == x for x in ['18', '19', '20', '21', '22', '23', '24', '25']):
		signal += 1
		return db_model.CollectbyChromosome_18to25

def addUserScoredData_toDB(file, userObjID='', streamStatus=''):
	"""
	Adds every single SNP inside the _scoredAllelesObject to the DB. 

	_scoredAllelesObject queries the DB and outputs a dictionary containing all
	SNPs that don't already exist in the DB
	
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
		assert(userObjID != '')

	# Date/time stamp for start of run
	parseNstream.printMsg(datetime.datetime.now().ctime())
	newNumSNPs = 0
	if os.path.exists(file):
		# Implement assertion for file type, ensure all column headers are accurate
		ScoredSNPdict = parseNstream._scoredAllelesObject(file, userObjID)
		alreadyinDB = {}
		alreadyinDB['total'] = 0
		alreadyinDB['ids'] = []
		signal = 0
		for chr in parseNstream.CHROMOSOME_LIST:

			alreadyinDB[chr] = 0

			collect_signals = []
			if any(chr == x for x in ['1', '2', '3', '4', '5']):
				signal += 1
				collection = db_model.CollectbyChromosome_1to5
			elif any(chr == x for x in ['6', '7', '8', '9', '10', '11']):
				signal += 1
				collection = db_model.CollectbyChromosome_6to11 
			elif any(chr == x for x in ['12', '13', '14', '15', '16', '17']):
				signal += 1
				collection = db_model.CollectbyChromosome_12to17 
			elif any(chr == x for x in ['18', '19', '20', '21', '22', '23', '24', '25']):
				signal += 1
				collection = db_model.CollectbyChromosome_18to25
			collect_signals.append(str(signal))

			positions = ScoredSNPdict[chr].keys()
			positions.sort()

			# Iterates through each chromosomal position adding new RSIDS to DB in ascending order
			for position in positions:
				# if not UsersSNPCollection.find({'_id': rsid}).count():
				data = ScoredSNPdict[chr][position]

				if newNumSNPs == 0: 
					parseNstream.printMsg("Sample data object:")
					print data 

				# Insert into DB
				if streamStatus == 'empty':
					collection.insert(data)
					newNumSNPs += 1

				if streamStatus != 'empty':
					if not collection.find({'_id': data[RSID]}).count(): 
						collection.insert(data)
						newNumSNPs += 1
					else: 
						alreadyinDB['total'] += 1
						alreadyinDB[chr] += 1
						alreadyinDB['ids'] += [data[RSID]]

				if newNumSNPs == db_model.CHECKLIST[k]:
					print "[x] Check %s-th complete. %s SNPs parsed so far. %s new SNPs added in total. %s parsed SNPs were already in the DB." % (k+1, db_model.CHECKLIST[k], newNumSNPs, COUNT-newNumSNPs)
					k += 1 

			if collect_signals == ['1', '2', '3', '4', '5']:
				parseNstream.printMsg("Interval 1 complete: (1-5)")
			elif collect_signals == ['6', '7', '8', '9', '10', '11']:
				parseNstream.printMsg("Interval 1 complete: (6-11)")
			elif collect_signals == ['12', '13', '14', '15', '16', '17']:
				parseNstream.printMsg("Interval 1 complete: (12-17)")
			else:
				if collect_signals == ['18', '19', '20', '21', '22', '23', '24', '25']:
					parseNstream.printMsg("Interval 1 complete: (18-25)")

			for chr in alreadyinDB:
				print alreadyinDB[chr]

		print "[x] Last check complete. %s total SNPs added to the UsersSNPCollection." % (db_model.CHECKLIST[k])

		# Date/time stamp for end of run
		parseNstream.printMsg(datetime.datetime.now().ctime())
		print alreadyinDB['ids']
		parseNstream.printMsg('SNPS ALREADY IN DB: %s' % alreadyinDB['total'])
		for chr in alreadyinDB:
			print alreadyinDB[chr]

	else:
		print "Path <%s> not found" % file

addUserScoredData_toDB(DEFAULT_SCORED_FILEPATH, userObjID="555a83687a349b6910bdff6c", streamStatus='empty')

# if name == '__main__':

# 	# scoreAlleles(DEFAULT_REF_FILEPATH, DEFAULT_USER_FILEPATH)
# 	addUserScoredData_toDB(DEFAULT_SCORED_FILEPATH, userObjID="555a83687a349b6910bdff6c")


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
from parser import _23andmeObject
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


UserChromosomeDict = _23andmeObject('../../BIO_DATA/raw23andme_SNPs_teyden.txt', 'RSID')

for item in rsIDs.find():
	if item['RSID'] not in UserChromosomeDict:
		print item['RSID']



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
CollectbyChromosome_1to5 = mongo_db.SNPCollection.chr1to5
CollectbyChromosome_6to11 = mongo_db.SNPCollection.chr6to11
CollectbyChromosome_12to17 = mongo_db.SNPCollection.chr12to17
CollectbyChromosome_18to25 = mongo_db.SNPCollection.chr18to25

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
 580001,
 586283, 
 -1]

DEFAULT_SCORED_FILEPATH = '../../BIO_DATA/alleleScores.txt'
DEFAULT_REF_FILEPATH = '../../BIO_DATA/23andme_v4_hg19_ref.txt'
DEFAULT_USER_FILEPATH = '../../BIO_DATA/raw23andme_SNPs_teyden.txt'

# Value... (fieldnames)
RSID = 'RSID'
DESCRIPTION = 'DESCRIPTION'
CHROMOSOME = 'CHROMOSOME'
POSITION = 'POSITION'
GENOTYPE = 'GENOTYPE'
DATE = 'DATE'
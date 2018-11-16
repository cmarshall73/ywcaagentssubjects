import json
import os
from archivesspace import archivesspace
import pprint
from utilities import *
import argparse
import logging
from cache_setup import * 
from spreadsheet_genre_subs import ywca_spreadsheet_objs

## -----Connect to ASpace API----- ##

CONFIGFILE = "archivesspace.cfg"

argparser = argparse.ArgumentParser()
argparser.add_argument("SERVERCFG", nargs="?", default="DEFAULT", help="Name of the server configuration section e.g. 'production' or 'testing'. Edit archivesspace.cfg to add a server configuration section. If no configuration is specified, the default settings will be used host=localhost user=admin pass=admin.")
cliArguments = argparser.parse_args()

aspace = archivesspace.ArchivesSpace()
aspace.setServerCfg(CONFIGFILE, section=cliArguments.SERVERCFG)
aspace.connect()

logging.basicConfig(level=logging.INFO)

## -----Pulling Corporate Agents from ASpace----- ## (uncomment when need to use)

# subs = aspace.get('/subjects?all_ids=true')

# logging.info('Querying ArchivesSpace for current People Agents')
# aspace_subs = []
# for sub in subs:
# 	logging.info('Querying Subject %s' % sub)
# 	record = aspace.get('/subjects/' + str(sub))
# 	aspace_subs.append(record)

## -----Caching Agent Query for later use----- ##
identifier = makeIdentifier('subjects')

# Uncomment below when need to make new query
# set_in_data_cache(identifier, aspace_subs, 14) 

response = get_from_cache(identifier, CACHE_DICTION)
print(pprint.pformat(response[67]))

## --------------------------------------------- ##

'Functions to add new Agents to ArchivesSpace'

def getDataDict_sg(sub_object):
	'Returns data dictionary necessary to add new Person Agent to ArchivesSpace'
		
	data = { "jsonmodel_type":"subject",
	"external_ids":[],
	"publish":True,
	"used_within_repositories":[],
	"used_within_published_repositories":[],
	"terms":[{ "jsonmodel_type":"term",
	"term": sub_object['term_1'],
	"term_type": sub_object['term_type'],
	"vocabulary":"/vocabularies/1"}],
	"external_documents":[],
	"vocabulary":"/vocabularies/1",
	"authority_id": sub_object['authority_id'],
	"source": sub_object['source']}

	return data


def addSubject(data_obj):
	'Adds new Subject to ArchivesSpace'

	try:
		response = aspace.post('/subjects', data_obj)
		return response
	except:
		logging.info('Could not add Subject')
		pass


## --Comparing ASpace Subjects with YWCA Subjects-- ##

aspace_subject_titles = []
for sub in response:
	title = sub['title']
	aspace_subject_titles.append((title))

subs_to_add = []
for obj in ywca_spreadsheet_objs: # taken from spreadsheet_people_agents.py
	if obj[0] in aspace_subject_titles:
		pass
	else:
		subs_to_add.append(obj[1])

## -------Adding Subjects to ArchivesSpace------- ## (uncomment when need to use)

# for sub in subs_to_add:
# 	sub_dict = getDataDict_sg(sub)
# 	added_sub = addSubject(sub_dict)
# 	print(added_sub)

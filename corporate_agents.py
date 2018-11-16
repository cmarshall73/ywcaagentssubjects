import json
import os
from archivesspace import archivesspace
import pprint
from utilities import *
import argparse
import logging
from cache_setup import *
from spreadsheet_corp_agents import ywca_spreadsheet_objs

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

# agents = aspace.get('/agents/corporate_entities?all_ids=true')

# logging.info('Querying ArchivesSpace for current Corporate Agents')
# aspace_agents = []
# for agent in agents:
# 	logging.info('Querying Agent %s' % agent)
# 	record = aspace.get('/agents/corporate_entities/' + str(agent))
# 	aspace_agents.append(record)

## -----Caching Agent Query for later use----- ##

identifier = makeIdentifier('agent_corporate_entities')

# Uncomment below when need to make new query
# set_in_data_cache(identifier, aspace_agents, 4) 

response = get_from_cache(identifier, CACHE_DICTION)

## --------------------------------------------- ##

'Functions to add new Agents to ArchivesSpace'

def getDataDict_c(agent_object):
	'Returns data dictionary necessary to add new Corporate Agent to ArchivesSpace'

	data = {"jsonmodel_type":"agent_corporate_entity",
	"names":[{"jsonmodel_type":"name_corporate_entity",
	"use_dates":[],
	"authorized":False,
	"is_display_name":True,
	"sort_name_auto_generate":True,
	"rules": agent_object['rules'],
	"primary_name": agent_object['primary_part_of_name'],
	"subordinate_name_1": agent_object['subordinate_name_1'],
	"subordinate_name_2": agent_object['subordinate_name_2'],
	"number":"",
	"sort_name":"auto",
	"dates":"",
	"qualifier":"",
	"authority_id": agent_object['authority_id'],
	"source": agent_object['source'] }],
	"related_agents":[],
	"agent_type":"agent_corporate_entity"}

	return data


def addAgent_c(data_obj):
	'Posts new Corporate Agent to ArchivesSpace'

	try:
		response = aspace.post('/agents/corporate_entities', data_obj)
		return response
	except:
		pass


## --Comparing ASpace Agents with YWCA Agents-- ##

aspace_agent_names = []
for agent in response:
	name = agent['title']
	aspace_agent_names.append(name)


agents_to_add = []
for obj in ywca_spreadsheet_objs: # taken from spreadsheet_corp_agents.py
	if obj[0] in aspace_agent_names:
		pass
	else:
		agents_to_add.append(obj[1])

## -------Adding Agents to ArchivesSpace------- ## (uncomment when need to use)

# for agent in agents_to_add:
# 	agent_dict = getDataDict_c(agent)
# 	added_agent = addAgent_c(agent_dict)
# 	print(added_agent)

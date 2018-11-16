import json
import os
from archivesspace import archivesspace
import pprint
from utilities import *
import argparse
import logging

## -----Connect to ASpace API----- ##

CONFIGFILE = "archivesspace.cfg"

argparser = argparse.ArgumentParser()
argparser.add_argument("SERVERCFG", nargs="?", default="DEFAULT", help="Name of the server configuration section e.g. 'production' or 'testing'. Edit archivesspace.cfg to add a server configuration section. If no configuration is specified, the default settings will be used host=localhost user=admin pass=admin.")
cliArguments = argparser.parse_args()

aspace = archivesspace.ArchivesSpace()
aspace.setServerCfg(CONFIGFILE, section=cliArguments.SERVERCFG)
aspace.connect()

## -----YWCA Topical Subject Data----- ##

# test = aspace.get('/subjects/6589')
# print(pprint.pformat(test))


def getDataDict_st(sub_object):
	
	if len(sub_object['subdivision_1']) == 0:
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

	else:
		data = {"jsonmodel_type":"subject",
		"external_ids":[],
		"publish":True,
		"used_within_repositories":[],
		"used_within_published_repositories":[],
		"terms":[{ "jsonmodel_type":"term",
		"term": sub_object['term_1'],
		"term_type": sub_object['term_type'],
		"vocabulary":"/vocabularies/1"}, 
		{"jsonmodel_type":"term",
		"term": sub_object['subdivision_1'],
		"term_type": sub_object['subdivision_1_term_type'],
		"vocabulary":"/vocabularies/1"}],
		"external_documents":[],
		"vocabulary":"/vocabularies/1",
		"authority_id": sub_object['authority_id'],
		"source": sub_object['source']}


	return data


test = { "term_1" : "Claire's Second Test Subject",
      "term_type" : "topical",
      "subdivision_1" : "Wisconsin",
      "subdivision_1_term_type" : "geographic",
      "subdivision_2" : "",
      "subdivision_2_term_type" : "",
      "subdivision_3" : "",
      "subdivision_3_term_type" : "",
      "source" : "local-lcsh-cx",
      "authority_id" : "tsbj_tmp_73743251" }

data = getDataDict_st(test)
posttest = aspace.get('/subjects/7293')
print(pprint.pformat(posttest))



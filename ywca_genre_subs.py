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

## -----YWCA People Agent Data----- ##

with open('ywcagenresubs.json') as json_file:
    try:
    	json_data = json.load(json_file)
    except ValueError:
    	exit(1)

## -----String Cleaning----- ## (JSON exported the numbers wonky)

for obj in json_data['rows']:
	num = str(obj['authority_id'])
	if len(num) > 9:
		obj['authority_id'] = num[:-2]
	else:
		obj['authority_id'] = num

## -----Adding all Genre Subjects from the YWCA spreadsheet to a list for comparison with the ASpace data----- ##

ywca_spreadsheet_objs = []
for obj in json_data['rows']:
	term = obj['term_1']
	ywca_spreadsheet_objs.append((term, obj))




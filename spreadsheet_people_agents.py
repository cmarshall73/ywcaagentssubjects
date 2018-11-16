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

with open('ywcaagentpersons.json') as json_file:
    try:
    	json_data = json.load(json_file)
    except ValueError:
    	exit(1)

## -----Adding all People Agents from the YWCA spreadsheet to a list for comparison with the ASpace data----- ##
ywca_spreadsheet_objs = []
for obj in json_data['rows']:
	name = obj['primary_part_of_name'] + ", " + obj['rest_of_name']
	ywca_spreadsheet_objs.append((name, obj))











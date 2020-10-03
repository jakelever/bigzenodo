import argparse
import json
import os
from .upload import upload

def checkFilePermissions(filename):
	status = os.stat(filename) 
	permissions = str(oct(status.st_mode)[-3:])
	assert permissions == '600', "Zenodo API access token must have 600 file permissions"

def main():
	parser = argparse.ArgumentParser('Tool to upload large files to Zenodo using the Zenodo RESTFUL API')
	parser.add_argument('--submission',required=True,type=str,help='JSON file with submission details')
	parser.add_argument('--accessTokenFile',required=True,type=str,help='File with Zenodo API access token')
	parser.add_argument('--sandbox',action='store_true',help='Whether to use the sandbox for testing purposes')
	parser.add_argument('--publish',action='store_true',help='Whether to actually complete the publication of the data to Zenodo. Irreversible!')
	args = parser.parse_args()

	checkFilePermissions(args.accessTokenFile)

	with open(args.accessTokenFile) as f:
		zenodo_access_token = f.read().strip()

	with open(args.submission) as f:
		submission = json.load(f)

	file_list = submission['file_list']
	title = submission['title']
	author = submission['author']
	author_affiliation = submission['author_affiliation']
	description_file = submission['description_file']
	existing_zenodo_id = int(submission['existing_zenodo_id']) if 'existing_zenodo_id' in submission else None

	upload(file_list,title,author,author_affiliation,description_file,zenodo_access_token,publish=args.publish,existing_zenodo_id=existing_zenodo_id,use_sandbox=args.sandbox)


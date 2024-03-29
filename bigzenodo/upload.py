import os
import shutil
import requests
import json
import markdown2

def upload(file_list,title,author,author_affiliation,description_file,zenodo_access_token,publish=False,existing_zenodo_id=None,use_sandbox=True):
	for f in file_list:
		assert os.path.isfile(f) or os.path.isdir(f), f"Output ({f}) was not found. It must be a file or directory."

	if use_sandbox:
		ZENODO_URL = 'https://sandbox.zenodo.org'
	else:
		ZENODO_URL = 'https://zenodo.org'

	headers = {"Content-Type": "application/json"}

	if existing_zenodo_id:
		print("Getting main ID for existing Zenodo submissions %d" % existing_zenodo_id)

		r = requests.get(ZENODO_URL + '/api/records/%d' % existing_zenodo_id, json={}, headers=headers)
		assert r.status_code == 200, f'Unable to find existing Zenodo record to update ({existing_zenodo_id=} {r.status_code=})'

		# Update with the latest ID
		existing_zenodo_id = r.json()['id']

		print("Create new version of Zenodo submission %d" % existing_zenodo_id)
		r = requests.post(ZENODO_URL + '/api/deposit/depositions/%d/actions/newversion' % existing_zenodo_id,
							params={'access_token': zenodo_access_token}, json={},
							headers=headers)

		assert r.status_code == 201, f'Unable to create new version of Zenodo record. You may need to manually delete any current draft deposits through the web interface. ({existing_zenodo_id=} {r.status_code=} {r.json()=})'

		jsonResponse = r.json()
		newversion_draft_url = r.json()['links']['latest_draft']
		deposition_id = newversion_draft_url.split('/')[-1] 

		r = requests.get(ZENODO_URL + '/api/deposit/depositions/%s' % deposition_id, params={'access_token':zenodo_access_token})

		assert r.status_code == 200, f'Unable to find Zenodo record ({deposition_id=} {r.status_code=})'

		bucket_url = r.json()['links']['bucket']
		doi = r.json()["metadata"]["prereserve_doi"]["doi"]
		doi_url = "https://doi.org/" + doi
	
		print("Clearing old files from new version of %s" % deposition_id)
		for f in r.json()['files']:
			file_id = f['id']
			r = requests.delete(ZENODO_URL + '/api/deposit/depositions/%s/files/%s' % (deposition_id,file_id), params={'access_token': zenodo_access_token})

			assert r.status_code == 204, f'Unable to clear old files in Zenodo record ({f=} {deposition_id=} {r.status_code=} {r.json()=})'

		print("Got provisional DOI: %s" % doi_url)
	else:
		print("Creating new Zenodo submission")
		r = requests.post(ZENODO_URL + '/api/deposit/depositions',
						params={'access_token': zenodo_access_token}, json={},
						headers=headers)

		assert r.status_code == 201, f"Unable to create Zenodo submission ({r.status_code=})"

		bucket_url = r.json()['links']['bucket']
		deposition_id = r.json()['id']
		doi = r.json()["metadata"]["prereserve_doi"]["doi"]
		doi_url = "https://doi.org/" + doi

		print("Got provisional DOI: %s" % doi_url)

	print("Adding files to Zenodo submission")
	if len(file_list) > 1:
		for f in file_list:
			assert not os.path.isdir(f), "If output includes a directory, it must be the only output"

	# Replace output list with directory listing
	if os.path.isdir(file_list[0]):
		outputDir = file_list[0]
		file_list = [ os.path.join(outputDir, f) for f in os.listdir(outputDir) ]

	for f in file_list:
		assert os.path.isfile(f), f"Cannot upload non-file to Zenodo ({f=})"
		basename = os.path.basename(f)

		r = requests.put('%s/%s' % (bucket_url,basename),
						data=open(f, 'rb'),
						headers={"Accept":"application/json",
						"Authorization":"Bearer %s" % zenodo_access_token,
						"Content-Type":"application/octet-stream"})

		assert r.status_code == 201, f"Unable to add file to Zenodo submission ({r.status_code=} {r.status_code=}) "

	assert os.path.isfile(description_file), f"Unable to find output_description_file ({description_file=})"
	with open(description_file) as f:
		description = f.read().strip()

	if description_file.endswith('.md'):
		description = markdown2.markdown(description)

	print("Adding metadata to Zenodo submission")
	data = {
			'metadata': {
					'title': title,
					'upload_type': 'dataset',
					'description':	description,
					'creators': [{'name': author,
							'affiliation': author_affiliation}]
			}
	}

	r = requests.put(ZENODO_URL + '/api/deposit/depositions/%s' % deposition_id,
					params={'access_token': zenodo_access_token}, data=json.dumps(data),
					headers=headers)

	assert r.status_code == 200, f"Unable to metadata to Zenodo submission ({r.status_code=})"

	if publish:
		print("Publishing Zenodo submission")
		r = requests.post(ZENODO_URL + '/api/deposit/depositions/%s/actions/publish' % deposition_id,
						 params={'access_token': zenodo_access_token} )
		assert r.status_code == 202, f"Unable to publish to Zenodo submission ({r.status_code=})"
	else:
		print("Did not publish Zenodo submission")

	return doi_url


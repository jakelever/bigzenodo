# BigZenodo

This is a command-line tool for making large uploads to [Zenodo](https://zenodo.org/). It requires a [Zenodo API access token](https://zenodo.org/account/settings/applications/) and uses the [Restful API](https://developers.zenodo.org/).

## Installation

This tool can be installed using PyPi, which will also install the dependencies of [requests](https://pypi.org/project/requests/) and [markdown2](https://pypi.org/project/markdown2/).

```
pip install bigzenodo
```

## Usage

It is a command-line tool that takes in a JSON file (described below) that lists the information for the submission, and the API token for the Zenodo account (in a separate file). It also takes two flags, whether to use the Zenodo sandbox and whether to complete the submission.

```
usage: Tool to upload large files to Zenodo using the Zenodo RESTFUL API
       [-h] --submission SUBMISSION --accessTokenFile ACCESSTOKEN 
       [--sandbox] [--publish]

optional arguments:
  -h, --help                     show this help message and exit
  --submission SUBMISSION        JSON file with submission details
  --accessTokenFile ACCESSTOKEN  File with Zenodo API access token
  --sandbox                      Whether to use the sandbox for testing purposes
  --publish                      Whether to actually complete the publication of the data to Zenodo. Irreversible!
```

## Submission File

The tool takes in a JSON file with the fields below. *existing_zenodo_id* is optional and denotes the identifier for an existing Zenodo submission which this submission will update.

```
{
  "file_list": [
    "colour_of_magic.tsv",
    "light_fantastic.tsv",
  ],
  "title": "The Troubles of Luggage",
  "author": "Rincewind",
  "author_affiliation": "Unseen University",
  "description_file": "output_description.md",
  "existing_zenodo_id": "1156241"
}
```

The description_file should be a file that contains text to be shown on the Zenodo page. If it is a Markdown file (and the filename ends with '.md'), it will be rendered appropriately.


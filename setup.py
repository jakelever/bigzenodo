#!/usr/bin/env python

from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

import sys
if sys.version_info[0] < 3:
	raise Exception("Requires Python 3")

VERSION='0.1.1'

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
	long_description = f.read()

with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
	requirements = f.readlines()

setup(name='bigzenodo',
	version=VERSION,
	description='A tool for doing big uploads to Zenodo',
	long_description=long_description,
	long_description_content_type='text/markdown',
	classifiers=[
		'Intended Audience :: Science/Research',
		'License :: OSI Approved :: MIT License',
		'Operating System :: Unix',
		'Programming Language :: Python :: 3.6',
		'Topic :: Scientific/Engineering',
	],
	url='http://github.com/jakelever/bigzenodo',
	author='Jake Lever',
	author_email='jake.lever@gmail.com',
	license='MIT',
	packages=['bigzenodo'],
	install_requires=requirements,
	include_package_data=True,
	entry_points = {
		'console_scripts': ['bigzenodo=bigzenodo.main:main'],
	},
	zip_safe=False,
	test_suite='nose.collector',
	tests_require=['nose'])


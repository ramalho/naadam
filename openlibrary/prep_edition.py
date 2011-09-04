#!/usr/bin/env python
# coding: utf-8

from json import loads, dumps
from datetime import datetime
from pprint import pprint
import sys

# 2008-04-29T15:03:11.581851
ISO_8601_FORMAT = '%Y-%m-%dT%H:%M:%S.%f'

def date_from_iso_str(iso_str):
	return datetime.strptime(iso_str, ISO_8601_FORMAT)

INFILE = '../../data/ol_dump_editions_2011-08-31.txt'
LIMIT = sys.maxsize
LIMIT = 100000

MANDATORY_FIELDS = set([u'last_modified', u'revision', u'title'])
TYPE_STR = '/type/edition'

#common_fields = set()
with open(INFILE) as infile:
	for line_index, lin in enumerate(infile):
		if line_index == LIMIT:
			break
		#print line_index + 1
		type_str, key, rev, last_modified, json_part = lin.split(None, 4)
		record = loads(json_part)
		assert type_str == TYPE_STR
		#assert 'title' in record, record
		assert record['type']['key'] == type_str
		assert record['key'] == key
		assert record['revision'] == int(rev)
		assert record['last_modified']['value'] == last_modified
		del record['type']
		del record['key']
		#if common_fields:
		#	common_fields.intersection_update(set(record.keys()))
		#else:
		#	common_fields = set(record.keys())
		extra_fields = sorted(set(record.keys()) - MANDATORY_FIELDS)
		if extra_fields:
			record['EXTRA_FIELDS'] = extra_fields
		record['_id'] = key.split('/')[-1]
		print dumps(record)

#print common_fields

"""
/authors/OL4906340A has no name field
/books/OL23406038M has no title field
"""
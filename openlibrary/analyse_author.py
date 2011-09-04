#!/usr/bin/env python
# coding: utf-8

from json import loads, dumps
from datetime import datetime
from pprint import pprint

# 2008-04-29T15:03:11.581851
ISO_8601_FORMAT = '%Y-%m-%dT%H:%M:%S.%f'

def date_from_iso_str(iso_str):
	return datetime.strptime(iso_str, ISO_8601_FORMAT)

INFILE = 'fixtures/ol_au_sample.txt'
#INFILE = '../../data/ol_dump_authors_2011-08-31.txt'

MANDATORY_FIELDS = set([u'last_modified', u'name', u'revision'])
TYPE_STR = '/type/author'

with open(INFILE) as infile:
	for line_index, lin in enumerate(infile):
		#print line_index + 1
		type_str, key, rev, last_modified, json_part = lin.split(None, 4)
		record = loads(json_part)
		assert type_str == TYPE_STR
		assert 'name' in record
		assert record['type']['key'] == type_str
		assert record['key'] == key
		assert record['revision'] == int(rev)
		assert record['last_modified']['value'] == last_modified
		#record['last_modified'] = date_from_iso_str(last_modified)
		#if 'created' in record:
		#	record['created'] = date_from_iso_str(record['created']['value'])
		del record['type']
		del record['key']
		extra_fields = sorted(set(record.keys()) - MANDATORY_FIELDS)
		if extra_fields:
			record['EXTRA_FIELDS'] = extra_fields
		record['_id'] = key.split('/')[-1]
		print dumps(record)

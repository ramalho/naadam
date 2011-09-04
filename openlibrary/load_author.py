#!/usr/bin/env python
# coding: utf-8

from json import loads
from datetime import datetime
from pprint import pprint

# 2008-04-29T15:03:11.581851
ISO_8601_FORMAT = '%Y-%m-%dT%H:%M:%S.%f'

INFILE = 'fixtures/ol_au_sample.txt'
#INFILE = '../data/ol_dump_authors_2011-08-31.txt'

MANDATORY_FIELDS = set([u'last_modified', u'name', u'revision'])
TYPE_STR = '/type/author'

with open(INFILE) as infile:
	for line_index, lin in enumerate(infile):
		#print line_index + 1
		type_str, key, rev, last_modified, record = lin.split(None, 4)
		record = loads(record)
		assert type_str == TYPE_STR
		assert 'name' in record
		assert record['type']['key'] == type_str
		assert record['key'] == key
		assert record['revision'] == int(rev)
		assert record['last_modified']['value'] == last_modified
		last_modified = datetime.strptime(last_modified, ISO_8601_FORMAT)
		record['last_modified'] = last_modified
		if 'created' in record:
			created = datetime.strptime(record['created']['value'], ISO_8601_FORMAT)
			record['created'] = created
		else:
			created = None
		del record['type']
		del record['key']
		extra_fields = sorted(set(record.keys()) - MANDATORY_FIELDS)
		if extra_fields:
			record['EXTRA_FIELDS'] = extra_fields
		record['_id'] = key.split('/')[-1]
		pprint(record)

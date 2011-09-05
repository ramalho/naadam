#!/usr/bin/env/python
'''
OpenLibrary loader

'''
import sys, json, os, calendar, time
from datetime import datetime
from glob import glob
from bz2 import BZ2File

DATA_DIR = '/home/luciano/prj/naadam/data/openlibrary/'

try:
    collection_name = sys.argv[1]
except IndexError:
    print 'usage:\n\t{0} <collection_name>'.format(sys.argv[0])
    raise SystemExit()

file_mask = '{0}ol_{1}_??.bz2'.format(DATA_DIR, collection_name)

ISO_8601_FORMAT = '%Y-%m-%dT%H:%M:%S.%f'

def log(lin_idx, lin):
    return 'line: {0}\n{1}'.format(lin_idx+1, lin)

for file_path in sorted(glob(file_mask))[:1]:
    print 'processing', file_path
    with BZ2File(file_path) as in_file:
        for idx, lin in enumerate(in_file):
            rec_type, key, revision_str, last_modified_str, record_str = lin.split(None, 4)
            record = json.loads(record_str)
            # get anc check record type
            assert record['type']['key'] == rec_type, log(idx, lin)
            # get and check primary key
            assert record['key'] == key, log(idx, lin)
            key = key.split('/')[2]
            assert key.startswith('OL'), log(idx, lin)
            # get and check revision
            assert record['revision'] == int(revision_str)
            # get and check last modified date and time            
            assert record['last_modified']['value'] == last_modified_str, log(idx, lin)
            last_modified = datetime.strptime(last_modified_str, ISO_8601_FORMAT)
            last_modified_tuple = last_modified.utctimetuple()
            last_modified_secs = calendar.timegm(last_modified_tuple)
            last_modified_rebuilt = datetime(*time.gmtime(last_modified_secs)[:-2])
            print last_modified_str, last_modified
            #last_modified_secs, last_modified_rebuilt.strftime(ISO_8601_FORMAT)

            

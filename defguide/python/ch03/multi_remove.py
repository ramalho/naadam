#!/usr/bin/env/python
# coding: utf-8

"""
Removing documents is usually a fairly quick operation, but if you want to 
clear an entire collection, it is faster to drop it (and then re-create any 
indexes).

“MongoDB: The Definitive Guide by Kristina Chodorow and Michael Dirolf 
(O’Reilly). Copyright 2010 Kristina Chodorow and Michael Dirolf, 
978-1-449-38156-1.”

"""

from __future__ import print_function

import time
from pymongo import Connection
db = Connection().naadam

#collection = db.create_collection('megaints')
db.drop_collection('megaints')
collection = db.megaints

start_t = time.time()
for i in xrange(100000):
    collection.insert({"foo": "bar", "baz": i, "z": 10 - i})
insert_t = time.time() - start_t
print('%0.3f seconds to insert' % insert_t)

start = time.time()
collection.remove()
collection.find_one()
total = time.time() - start
print('%0.3f seconds to remove' % total)


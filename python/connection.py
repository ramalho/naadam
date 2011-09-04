#!/usr/bin/env/python
# coding: utf-8

"""
Learning about Connection objects

"""
import pymongo

def get_attrs(obj):
    attrs = []
    for name in dir(obj):
        if name.startswith('_'): continue
        value = getattr(obj, name)
        if callable(value):
            callable_flag = True
            try:
                value = value()
            except TypeError, ex:
                value = '*** ' + str(ex)
        else:
            callable_flag = False
        value_type = type(value).__name__
        if value_type == 'module':
            value = value.__name__
        attrs.append( ('()' if callable_flag else '', value_type, name, value) )
    attrs.sort()
    return attrs

def dump_attrs(obj):
    for attr in get_attrs(obj):
        print '{0:2} {1:10}\t{2:20}\t{3}'.format(*attr)

print '*'*60, 'pymongo module'
dump_attrs(pymongo)
cnx = pymongo.Connection()
print '*'*60, 'Connection instance'
dump_attrs(cnx)



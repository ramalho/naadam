#!/bin/sh
time mongoimport -d openlibrary -c $1 $2

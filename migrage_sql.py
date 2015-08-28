#! /usr/bin/env python

"""
    this script migrate Model to sql
    work for sqlalchemy, peewee, etc.
"""
,
import os
import itertools
import yaml
import MySQLdb

# database config
db_config = {
            "host":"localhost",
            "user":"root",
            "passwd":"",
            "db":"asa",
            "port":3306
            }

try:
    conn = MySQLdb.connect(**db_config)
except Exception, e:
    print e

try:
    yaml_data = yaml.load("models.yaml", "r") # your schema file
except:
    print "valid file"

cur = conn.cursor()
cur.execute("SELECT * FROM INFORMATION_SCHEMA.COLUMNS \
            WHERE TABLE_SCHEMA = '%s';"%(db_config["db"]))

"""
|TABLE_CATALOG | TABLE_SCHEMA | TABLE_NAME | COLUMN_NAME | ORDINAL_POSITION |
COLUMN_DEFAULT | IS_NULLABLE | DATA_TYPE | CHARACTER_MAXIMUM_LENGTH |
CHARACTER_OCTET_LENGTH | NUMERIC_PRECISION | NUMERIC_SCALE | DATETIME_PRECISION |
CHARACTER_SET_NAME | COLLATION_NAME  | COLUMN_TYPE | COLUMN_KEY | EXTRA |
PRIVILEGES| COLUMN_COMMENT |
"""
# convert schemas
schemas = cur.fetchall()
schemas = map(list, schemas)

# refactor schemas as we got so much information

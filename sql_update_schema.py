#! /usr/bin/env python

"""
    this script update mysql scheme
    work for sqlalchemy, peewee, etc.
    just a simple one ,without foreign key ,manytomany, ...etc
"""

import os
import re
import sys
import argparse
from itertools import groupby
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

parser = argparse.ArgumentParser(prog="python %s"%os.path.dirname(__file__),
                                 usage='%(prog)s [options]')
parser.add_argument("-f", help=" 'F' or 'f' force to update")
args = parser.parse_args()
UPDATE = True if args.get("f") in ("f", "F") else False

try:
    """'version': {'version': {'default': '', 'type': 'int', 'nullable':False},
                   'id': {'default': '', 'type': 'int', 'key': 'pri', 'nullable':False},
                   'name': {'default': '', 'type': 'varvhar(10)','nullable': True},
                   'desc': {'default':'', 'type':'varchar(20)','nullable':False}}
    """
    yaml_schemas = yaml.load(file("schema.yaml")) # your schema file
except:
    print "valid file"

col_type = re.compile(r"(.*?int(.*)|.*?char(.*)|.*?text(.*))", re.IGNORECASE)

def null_default(type, nullable, default=''):
    # set default value
    if default:
        return default
    elif "int" in type and nullable:
        return "0"
    else:
        return "NULL"

cur = conn.cursor()
cur.execute("show tables")
tables = [cf[0] for cf in cur.fetchall()]
sql_schemas = {}
for table in tables:
    """| Field | Type | Null | Key | Default | Extra |"""
    cur.execute("desc %s"%table)
    pro_col = ['type', "nullable", "key", "default"]
    pro_data = [cf[:-1] for cf in list(cur.fetchall())]
    cur_table = dict()
    for data in pro_data:
        cur_table[data[0]] = dict(zip(pro_col, data[1:]))
    sql_schemas[table] = cur_table

for schema in yaml_schemas:
    # we don't do the delete
    # default id as  primary key, auto_increment
    yaml_table = yaml_schemas[schema]
    if schema in sql_schemas:
        print "update table: %s"%(schema)
        sql_table  = sql_schemas[schema]
        for col in yaml_table:
            if col in sql_table:
                flag = col_type.match(yaml_table[col]["type"])
                if flag:
                    # type has length
                    if yaml_table[col]["type"] > sql_table[col]["type"]:
                        sql = "alter table %s modify %s %s"%(schema, col,\
                                                             yaml_table[col]["type"])
                        print sql
                        if UPDATE:
                            cur.execute(sql)
                    elif not flag.groups()[1] or flag.groups()[2] or flag.groups()[3]:  # with default length
                        sql = "alter table %s modify %s %s"%(schema, col,\
                                                             yaml_table[col]["type"])
                        print sql
                        if UPDATE:
                            cur.execute(sql)
                else:
                    # other type, like date, I dont think we will change them
                    print "***********other type: %s"%col
            else:
                pro_col = yaml_table[col]
                base = "primary key auto_increment" if col == "id" else ""
                sql = "alter table %s add column %s %s %s"%(schema, col, pro_col["type"], base)
                #sql = "alter table %s add column %s %s %s default %s"%\
                #       (schema, col, pro_col["type"], pro_col["nullable"] and\
                #        "NULL" or "NOT NULL", pro_col["default"] or 'NULL',)
                print sql
                if UPDATE:
                    cur.execute(sql)
    else:
        sql = "create table %s \n("%(schema)
        cols = []
        for col in yaml_table:
            base = "primary key auto_increment" if col == "id" else ""
            cols.append("%s %s %s"%(col, yaml_table[col]["type"], base))
        sql += " ,\n".join(cols)
        sql += ");"
        print sql
        if UPDATE:
            cur.execute(sql)

if not UPDATE:
    print "We won't update schema only if you force to do that"

cur.close()
conn.close()

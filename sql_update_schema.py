#! /usr/bin/env python

"""
    this script migrate Model to sql
    work for sqlalchemy, peewee, etc.
    just a simple one ,without foreign key ,manytomany, ...etc
"""

import os
import re
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

def null_transfer(type, null):
    if "int" in type and null == "no":
        return "0"
    else:
        return ""

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
    # we set primary id auto_increment
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
                        cur.execute(sql)
                    elif not flag.groups()[1]:
                        sql = "alter table %s modify %s %s"%(schema, col,\
                                                             yaml_table[col]["type"])
                        print sql
                        cur.execute(sql)
                else:
                    # other type, like date
                    print "***********other type: %s"%col
                    pass
            else:
                pro_col = yaml_table[col]
                base = "primary key auto_increment" if col == "id" else ""
                sql = "alter table %s add column %s %s %s"%(schema, col, pro_col["type"], base)
                #sql = "alter table %s add column %s %s %s default %s"%\
                #       (schema, col, pro_col["type"], pro_col["nullable"] and\
                #        "NULL" or "NOT NULL", pro_col["default"] or 'NULL',)
                print sql
                cur.execute(sql)
    else:
        sql = "create table %s \n("%("what")
        cols = []
        for col in yaml_table:
            base = "primary key auto_increment" if col == "id" else ""
            cols.append("%s %s %s"%(col, yaml_table[col]["type"], base))
        sql += " ,\n".join(cols)
        sql += ");"
        print sql


cur.close()
conn.close()

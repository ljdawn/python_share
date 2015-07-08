#! /usr/bin env python

import sys
import os
import pprint

"""
this file help u to find the related (foreign table) to the specified table
it's for django orm
"""

##TODO  update the specified table and then change the relational tables

if len(sys.argv) < 3:
    print "usage python get_related_tables ${paths} ${model(m)|views(v)} ${table_name}"
    sys.exit()

if len(sys.argv) == 4:
    tb_name = sys.argv[3]
else:tb_name = ''

paths, fl_type = sys.argv[1], sys.argv[2]

models_lst = []
views_lst  = []
## "." is the paths
for dirpath, dirnames, filenames in os.walk(paths):
    ### just use models.py for general
    if "models.py" in filenames:
        models_lst.append(dirpath + "/models.py")
    if "views.py" in filenames:
        views_lst.append(dirpath + "/views.py")

fl_lst = {"m":models_lst, "v":views_lst}

relations = []
for fl in fl_lst[fl_type]:
    with open(fl, "r") as file:
        class_name, foreign_table, line_no = "", "", 0
        if tb_name:
            for line in file:
                line_no += 1
                if line.startswith("class "):
                    class_name = line[6:] ## class name
                elif class_name and tb_name in line and "Field" in line :
                    relations.append(["/".join(fl.split("/")[-2:]), \
                                  class_name.split("(")[0],line.strip()])
        else:
            for line in file:
                line_no += 1
                if not line.strip().startswith("#") and ("message_set" in line or \
                                                         "get_and_delete_messages" in line):
                    print fl, line_no

for relation in relations:
    pprint.pprint(relation)

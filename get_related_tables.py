#! /usr/bin env python

import sys
import os

"""
this file help u to find the related (foreign table) to the specified table
it's for django
"""
if len(sys.argv) != 3:
    print "usage python <paths> <table_name>"
    sys.exit()

paths, tb_name = sys.argv[1], sys.argv[2]

lst = []
## "." is the paths
for dirpath, dirnames, filenames in os.walk(paths):
    if "models.py" in filenames:
        lst.append(dirpath + "/models.py")

total = []
for fl in lst:
    with open(fl, "r") as file:
        class_name, foreign_table, line_no = "", "", 0
        for line in file:
            line_no += 1
            if line.startswith("class "):
                class_name = line[6:] ## class name
            elif  class_name and tb_name in line and "Field" in line :
                total.append([fl, class_name, line])
            else:
                pass
for tot in total:
    print tot

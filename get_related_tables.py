#! /usr/bin env python

import os

lst = []
## "." is the paths
for dirpath, dirnames, filenames in os.walk("."):
    if "models.py" in filenames:
        lst.append(dirpath + "/models.py")

current = []
for fl in lst:
    with open(fl, "r") as file:
        class_name, foreign_table, line_no = "", "", 0
        for line in file:
            line_no += 1
            if line.startswith("class "):
                class_name = line[6:] ## class name
            elif  class_name and "Region" in line and "Field" in line :
                current.append([fl, class_name, line])
            else:
                pass
for cur in current:
    print cur

#! /usr/bin/env python

"""
    in django1.3, we can use add_auto and default at the same time
    but in 1.8, just use add_auto instead
"""

import sys
import os
import re
import pprint


if len(sys.argv) != 3:
    print "usage:python %s ${old_style_path} ${new_style_path}\n\
            old_style_path -> old files\n\
            new_style_path -> new files"%sys.argv[0]
    sys.exit()

old = sys.argv[1]
new = sys.argv[2]

if not (os.path.exists(old) and os.path.exists(new)):
    print "bad path"
    sys.exit()

#patterns = {
#            r"ad"    : r'.*?(auto_now\s?=).*?(default\s?=).*',
#            r"class" : r'.*?class\s*(.*?)'
#            }
pattern = re.compile(r'.*?(auto_now\s?=).*?(default\s?=).*')

# we just process model files
# and dont need django files
old_files = []
new_files = []

for root, dirs, filenames in os.walk(old):
    if "/django/" not in root and "models.py" in filenames:
        old_files.append(root+ "/models.py")

for root, dirs, filenames in os.walk(new):
    if "/django/" not in root and "models.py" in filenames:
        new_files.append(root+ "/models.py")

# diff files
couples = zip(old_files, new_files)
#pprint.pprint(couples)

for old_file in old_files:
    with open(old_file, "r") as file:
        line_no = 0
        cur_class = ''
        for line in file:
            line_no += 1
            if line.strip().startswith("class "):
                cur_class = line.strip()
            ## mv them to regular
            elif pattern.match(line):
                print old_file
                print(cur_class.split("(")[0], line.strip().split("=")[0])


if __name__ == "__main__":
    pass

#! /usr/bin/env python

"""
    this file mv html files from original to updating projects
"""

import os
import sys
import pprint
from shutil import copy2

if len(sys.argv) != 3:
    print "usage: python restore_html_files.py ${from_paths} ${to_paths}"
    sys.exit()

from_paths = sys.argv[1]
to_paths   = sys.argv[2]

if not to_paths.endswith("/"):
    to_paths += '/'

html_files = []

for root, dirs, files in os.walk("%s"%from_paths):
    for file in files:
        # cause we got django in the project
        if "/django/" not in root and (file.endswith(".html") or\
                                       file.endswith(".htm")):
            html_files.append(os.path.join(root, file))

if to_paths == "findsomething/":
    for html in html_files:
        with open(html, "r") as file:
            for line in file:
                if line.strip().startswith("{% load staticfiles"):
                    print html
    sys.exit()

# change file to relative paths
if os.path.isdir(to_paths):
    for html in html_files:
        pprint.pprint(html)
        to_html = to_paths + '/'.join(html.split('/')[5:])
        if not os.path.exists(to_html):
            try:
                to_html = to_html.replace("media", "static")
                file = open(to_html, "w")
                file.close()
            except:print "what the hell"
        copy2(html, to_html)

if __name__ == "__main__":
    pass

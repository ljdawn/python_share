#! /usr/bin/env python

"""
    this file convert url to "url"
    update django 1.2.7 to 1.8
"""

import re
import os
import sys

from tempfile import mkstemp
from shutil import move

pattern = re.compile(r"(.*?)({%\s*url\s*(\S*)?\s*(.*?)%})(.*)")

if len(sys.argv) != 2:
    print "usage: python replace_content.py ${paths}"
    sys.exit()

paths = sys.argv[1]
html_files = []

for root, dirs, files in os.walk("%s"%paths):
    for file in files:
        if file.endswith(".html") or file.endswith(".htm"):
            html_files.append(os.path.join(root, file))

# FIXME if several urls in line?
for html_file in html_files:
    #Create temp file
    fh, abs_path = mkstemp()
    with open(abs_path, "w") as newfile:
        with open(html_file, 'r') as file:
            for line in file:
                if line == '\n':
                    continue
                matchs = pattern.match(line)
                if matchs and not (matchs.groups()[2].startswith('"') or\
                                 matchs.groups()[2].startswith("'")):
                    new_line = matchs.groups()[0] + '{% url "' + matchs.groups()[2] +\
                               '" ' + matchs.groups()[3] + '%}' + matchs.groups()[4] + '\n'
                    rep_str = matchs.groups()[2]
                    newfile.write(new_line)
                else:
                    newfile.write(line)

    os.close(fh)
    os.remove(html_file)
    move(abs_path, html_file)

if __name__ == "__main__":
    pass

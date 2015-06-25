#! /usr/bin/env python

"""
    thif file convert url to "url"
    update django 1.2.7 to 1.8
"""

import re
import os
import sys

from tempfile import mkstemp
from shutil import move

pattern = re.compile(r"(.*?)({%\s*url\s*(.*?)\s*%})(.*)")
pattern_to = '{% url "%s" %}'

if len(sys.argv) != 2:
    print "usage: python replace_content.py ${paths}"
    sys.exit()

paths = sys.argv[1]
html_files = []

for root, dirs, files in os.walk("%s"%paths):
    for file in files:
        if file.endswith(".html") or file.endswith(".htm"):
            html_files.append(os.path.join(root, file))

for html_file in html_files:
    #Create temp file
    fh, abs_path = mkstemp()
    with open(abs_path, "w") as newfile:
        with open(html_file, 'r') as file:
            for line in file:
                flag = pattern.match(line)
                if flag and not (flag.groups()[1].startswith('"') or\
                                 flag.groups()[1].startswith("'")):
                    rep_str = flag.groups()[2]
                    new_line = flag.groups()[0] + '{% url "' + flag.groups()[2] +\
                                                  '" %}' + flag.groups()[3]
                    newfile.write(new_line)
                    newfile.write('\n')
                else:
                    newfile.write(line)
                    newfile.write('\n')

    os.close(fh)
    os.remove(html_file)
    move(abs_path, html_file)

if __name__  == "__main__":
    pass

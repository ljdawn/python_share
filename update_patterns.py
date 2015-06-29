#! /usr/bin/env python

"""
    update django 1.2.7 to 1.8
    {% url ${url} %} to {% url "${url}" %}
    change "MEDIA_URL" to "STATIC_URL"
"""

import re
import os
import sys

from tempfile import mkstemp
from shutil import move

from lxml import etree

# "href" line startswith "<link", "src" line startswith "<script"
pattern = { r"url" : r"(.*?)({%\s*url\s*(\S*)?\s*(.*?)%})(.*)",
            r"href": r'(.*?)(href="\s?{{\s?MEDIA_URL\s?}})(.*?)"(.*)',
            r"src" : r'(.*?)(src="\s?{{\s?MEDIA_URL\s?}})(.*?)"(.*)',
          }

for pat in pattern:
    pattern[pat] = re.compile(pattern[pat])

if len(sys.argv) != 3:
    print "usage: python update_urls_reverse.py ${paths} {replace_type}\n\
          {0:update urls reverse, 1:media ro static}"
    sys.exit()

paths = sys.argv[1]
try:
    type = int(sys.argv[2])
except:
    print "bad argv"
    sys.exit()

TYPE = {0:"URL", 1:"STATIC"}
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
            if TYPE.get(type) == "URL":
                for line in file:
                    if line == '\n':
                        continue
                    matchs = pattern["url"].match(line)
                    # FIXME if several urls in line?
                    if matchs and not (matchs.groups()[2].startswith('"') or\
                                     matchs.groups()[2].startswith("'")):
                        new_line = matchs.groups()[0] + '{% url "' + matchs.groups()[2] +\
                                   '" ' + matchs.groups()[3] + '%}' + matchs.groups()[4] + '\n'
                        rep_str = matchs.groups()[2]
                        newfile.write(new_line)
                    else:
                        newfile.write(line)
            elif TYPE.get(type) == "STATIC":
                # TODO link, src
                newfile.write("{% load staticfiles %}\n")
                for line in file:
                    if line == '\n':
                        continue
                    if line.strip().startswith("<link"):
                        matchs = pattern["href"].match(line)
                        if matchs:
                            line = matchs.groups()[0] + 'href="{% static \"' + \
                                   matchs.groups()[2] + '\" %}"' + matchs.groups()[3]
                            newfile.write(line)
                        else:
                            newfile.write(line) # should check this
                    elif line.strip().startswith("<script"):
                        matchs = pattern["src"].match(line)
                        if matchs:
                            line = matchs.groups()[0] + 'href="{% static \"' + \
                                   matchs.groups()[2] + '\" %}"' + matchs.groups()[3]
                            newfile.write(line)
                        else:
                            newfile.write(line)
                    else:
                        newfile.write(line)

    os.close(fh)
    os.remove(html_file)
    move(abs_path, html_file)

if __name__ == "__main__":
    pass

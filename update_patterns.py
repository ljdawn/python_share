#! /usr/bin/env python

"""
    update django 1.2.7 to 1.8
    {% url ${url} %} to {% url "${url}" %}
    change "MEDIA_URL" to "STATIC_URL"
    and other stuffs come to check debug
"""

import re
import os
import sys

from tempfile import mkstemp
from shutil import move

# "href" line startswith "<link", "src" line startswith "<script"
# FIXME now we cant replace all urls
pattern = { r"url"  : r"(.*?)({%\s*url\s*(\S*)?\s*(.*?)%})(.*)",
            r"href" : r'(.*?)(href="\s?{{\s?MEDIA_URL\s?}})(.*?)"(.*)',
            r"src"  : r'(.*?)(src="\s?{{\s?MEDIA_URL\s?}})(.*?)"(.*)',
            r"start": r'^{%\s?extends.*?',
          }

for pat in pattern:
    pattern[pat] = re.compile(pattern[pat])

if len(sys.argv) != 4:
    print "usage: python update_patterns.py ${paths} ${replace_type} ${debug}\n\
            replace_tyle:\n\
                          {0:update urls reverse, \n\
                           1:media to static, \n\
                           2:changelocation, \n\
                           3:href of script to src, \n\
                           4:2.5->2.7(replace simplejson)}\n\
            debug:\n\
                           {0:false,\n\
                            1:true(show msg)}\n\
          "
    sys.exit()

paths = sys.argv[1]

try:
    type  = int(sys.argv[2])
    debug = int(sys.argv[3])
except:
    print "bad argv goto check"
    sys.exit()

TYPE = {0:"URL", 1:"STATIC", 2:"CHANGELOC", 3:"HREF2SRC", 4:"UPDATEPY"}

pattern_files = []

for root, dirs, files in os.walk("%s"%paths):
    for file in files:
        if TYPE.get(type) != "UPDATEPY":
            if file.endswith(".html") or file.endswith(".htm"):
                pattern_files.append(os.path.join(root, file))
        else:
            if file.endswith(".py"):
                pattern_files.append(os.path.join(root, file))

def update_url(file, newfile = None):
    """
        update url patterns 1.2->1.8
    """
    file = open(file, "r")
    if debug:
        for line in file:
            matchs = pattern["url"].match(line)
            # FIXME if several urls in line?
            if matchs and not (matchs.groups()[2].startswith('"') or\
                               matchs.groups()[2].startswith("'")):
                print matchs
        return
    newfile = open(newfile, "w")
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
    file.close()
    newfile.close()

def update_static(file, newfile = None):
    """
        update static patterns 1.2->1.8

    """
    # TODO link, src
    # if we got {% extends %} then we should add {% load staticfiles %}
    # FIXME anyway ,this is bad, should fix this later
    file = open(file, "r")
    if debug:
        for line in file:
            if line.strip().startswith("<link"):
                matchs = pattern["href"].match(line)
                if matchs:
                    print matchs.groups()
        return
    newfile = open(newfile, "w")
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
                if debug:
                    print matchs.groups()
                line = matchs.groups()[0] + 'src="{% static \"' + \
                       matchs.groups()[2] + '\" %}"' + matchs.groups()[3]
                newfile.write(line)
            else:
                newfile.write(line)
        else:
            newfile.write(line)
    file.close()
    newfile.close()

def update_loc(file, newfile=None):
    """
        change location of {% load staticfiles %}
         1.2->1.8
    """
    file = open(file, "r")
    lines = file.readlines()
    if debug:
        for line in lines[:4]:
            print line
        return
    newfile = open(newfile, "w")
    if len(set(lines[:2])) == 1:
        lines = lines[1:] ## forgot when done something bad?
    if len(lines)>1 and pattern["start"].match(lines[1].strip()):
        lines[0], lines[1] = lines[1], lines[0]
    for line in lines:
        newfile.write(line)
    file.close()
    newfile.close()

def update_href(file, newfile = None):
    """"
        href to src {fix error} 1.2->1.8
    """
    file = open(file, "r")
    if debug:
        for line in file:
            if line.strip().startswith("<script"):
                print line
        return
    newfile = open(newfile, "w")
    for line in file:
        if line.strip().startswith("<script"):
            newfile.write(line.replace("href=", "src="))
        else:
            newfile.write(line)
    file.close()
    newfile.close()

def update_py(file, newfile = None):
    """"
        simplejson to json
    """
    ## TODO 2 conditions: 1,import; 2,json.dumps
    ## other changes?  forgot that......
    file = open(file, "r")
    if debug:
        for line in file:
            if line.strip().startswith("import json as simplejson"):
                print line
            elif "simplejson.dumps" in line:
                print line
            elif "simplejson.loads" in line:
                print line
        return
    newfile = open(newfile, "w")
    for line in file:
        if line.strip().startswith("import json as simplejson"):
            newfile.write(line.replace("import json as simplejson", "import json"))
        else:
            newfile.write(line.replace("simplejson.dumps", "json.dumps")\
                              .replace("simplejson.loads", "json.loads"))
    file.close()
    newfile.close()

functions = { 0: update_url,
              1: update_static,
              2: update_loc,
              3: update_href,
              4: update_py,
            }

for file in pattern_files:
    print file
    if debug:
        functions[type](file)
    else:
        #Create temp file
        fh, abs_path = mkstemp()
        #replace_file = functions[type](file, abs_path)
        functions[type](file, abs_path)
        os.close(fh)
        os.remove(file)
        move(abs_path, file)

if __name__ == "__main__":
    pass

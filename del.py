import threading
import os
import sys

if len(sys.argv) != 2:
    print "usage python del.py ${filename}"
    sys.exit()

filename = sys.argv[1]

editor = os.environ.get('EDITOR', 'vim')
def delete():
    threading.Timer(2.0, delete).start()
    with open(filename, 'rb+') as filehandle:
        filehandle.seek(-1, os.SEEK_END)
        filehandle.truncate()

if __name__ == "__main__":
   delete() 

#! /usr/bin/env python

"""no use activate env first"""


import re
import os
import argparse
import traceback
from multiprocessing import Pool

queues = []

class cd:

    def __init__(self, newpath):
        self.newpath = os.path.expanduser(newpath)

    def __enter__(self):
        self.savedpath = os.getcwd()
        os.chdir(self.newpath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedpath)

def init():
    """inits the environment"""
    args = get_arguments()
    pro_paths  = args.pro_paths
    cmds_paths = args.commands_file
    return cmds_paths, pro_paths

def get_queues(commands_file):
    """gets queue of commands"""
    with open(commands_file, "r") as file:
        flag = False
        for line in file:
            if line.startswith("[") and not line[1:].startswith("django]"):
                flag = True
            elif flag and line.strip():
                queues.append(line.strip())
            else:
                pass
    return queues

def get_arguments():
    parser = argparse.ArgumentParser(description='Process arguments.')
    parser.add_argument('commands_file', help='commands_file paths')
    parser.add_argument('pro_paths', help='project paths')
    return parser.parse_args()

def test_command(command):
    """python manage.py command"""

if __name__ == "__main__":
    cmds_file, pro_paths = init()
    p = Pool(4)
    with cd(pro_paths):
        p.map(test_command, get_queues(cmds_file))

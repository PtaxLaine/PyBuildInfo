#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
\file run.py
\brief PyBuildInfo
\author Andrei Vorobev (http://www.ptaxa.net)
\date 2015
\copyright
Copyright © 2015 Andrei Vorobev (http://www.ptaxa.net) All rights reserved.
"""

import sys
import os
import re
import subprocess
import configparser
import argparse
import importlib.util
import json
from . import scm
from . import resource

def run():
    args = argparse.ArgumentParser()
    args.add_argument('-cfg', '--cfg',
                      type=str,
                      help="configuration file",
                      metavar='*.ini',
                      default=os.path.join(resource.get_resource_directory(), 'BuildInfo.ini'))
    args.add_argument('-in', '--in',
                      dest='uin',
                      type=str,
                      help="input json",
                      metavar='{...}',
                      default='{}')
    args.add_argument('-dir', '--dir',
                      type=str,
                      help="scm dir")
    args.add_argument('-out', '--out',
                      type=str,
                      help="filename or :STDOUT:")

    args = args.parse_args()

    config = configparser.ConfigParser()
    config.read(args.cfg)
    
    if args.out:
        config['global']['output'] = args.out
    if args.dir:
        config['global']['scm_directory'] = args.dir

    template_engine = importlib.import_module(config['global']['template_engine']).Template
    template = None
    if 'template' in config['global']:
        if config['global']['template'][0] == ':':
            config['global']['template'] = os.path.join(resource.get_resource_directory(),
                                                        config['global']['template'][1:])
        origin_wd = os.getcwd()
        os.chdir(os.path.dirname(args.cfg))
        with open(config['global']['template'], 'rb') as fs:
            template = fs.read().decode()
        os.chdir(origin_wd)

    if config['global']['scm'].lower() == 'git':
        SCM = scm.git.SCM

    if 'scm_directory' in config['global']:
        scm_dir = config['global']['scm_directory']
    else:
        scm_dir = os.getcwd()    

    res = SCM(scm_dir, config).result()
    res.update(json.loads(args.uin))
    res = str(template_engine(template, res))

    if config['global']['output'].strip().lower() == ':stdout:':
        print(res)
    else:
        with open(config['global']['output'], 'wb') as fs:
            fs.write(res.encode())


if __name__ == '__main__':
    run()

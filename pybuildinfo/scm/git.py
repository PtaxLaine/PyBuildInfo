#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
\file git.py
\brief PyBuildInfo > SCM > GIT
\author Andrei Vorobev (http://www.ptaxa.net)
\date 2015
\copyright
Copyright © 2015 Andrei Vorobev (http://www.ptaxa.net) All rights reserved.
"""

import os
import re
import subprocess
import time
from . import abs


class SCM(abs.SCM):
    def __init__(self, scm_dir, config):
        self.__scm_dir = scm_dir
        self.__result = {}
        self.__version_tag_rx = re.compile(config['git']['version_tag_rx'])
        self.__tags_rx = re.compile(config['git']['tags_rx'], re.IGNORECASE)
        self.__process()


    def __process(self):
        origin_wd = os.getcwd()
        os.chdir(self.__scm_dir)
        try:
            result = abs.SCM._pre_process()
            result['scm_name'] = 'git'
            with subprocess.Popen(['git', 'log', '--pretty=format:%H'], stdout=subprocess.PIPE) as proc:
                proc.wait()
                commits = [x.decode().strip() for x in proc.stdout.readlines()]

            with subprocess.Popen(['git', 'log', '-n', '1', '--pretty=format:%H\t%at\t%an\t%ae'], stdout=subprocess.PIPE) as proc:
                proc.wait()
                commit = [x.strip() for x in proc.stdout.read().decode().split('\t')]
                result['scm_revisions'] = commit[0]
                result['scm_timestamp'] = commit[1]
                result['scm_author'] = commit[2]
                result['scm_author_email'] = commit[3]

            with subprocess.Popen(['git', 'log', '-n', '1', '--pretty=format:%B'], stdout=subprocess.PIPE) as proc:
                proc.wait()
                result['scm_message'] = proc.stdout.read().decode()
                result['scm_message_escaping'] = abs.SCM._escape_string(result['scm_message'])

            def find_ver():
                for commit in commits:
                    with subprocess.Popen(['git', 'describe', '--tags', '--exact-match', commit], stdout=subprocess.PIPE, stderr=subprocess.PIPE) as proc:
                        proc.wait()
                        if proc.returncode == 0:
                            for x in [x.decode().strip() for x in proc.stdout.readlines()]:
                                x = self.__version_tag_rx.match(x)
                                if x:
                                    return [(t.strip() if t.strip() else '0') if t else '0' for t in [x.group(2), x.group(3), x.group(4)]]
                return [0,0,0]

            tmp = find_ver()
            result['scm_version'] = '{}.{}.{}'.format(tmp[0], tmp[1], tmp[2])
            result['scm_version_major'] = tmp[0]
            result['scm_version_minor'] = tmp[1]
            result['scm_version_patch'] = tmp[2]
            result['scm_version_stable'] = (0x01 - (int(tmp[1]) & 0x01)) if int(tmp[0]) > 0 else 0x00

            result['scm_version_tags'] = ''
            with subprocess.Popen(['git', 'describe', '--tags', '--exact-match', result['scm_revisions']], stdout=subprocess.PIPE, stderr=subprocess.PIPE) as proc:
                proc.wait()
                if proc.returncode == 0:
                    tmp = [x.decode().strip() for x in proc.stdout.readlines()]
                    result['scm_version_tags'] = '\t'.join([abs.SCM._escape_string.__escape(x) for x in tmp if self.__tags_rx.match(x)])

            with subprocess.Popen(['git', 'branch'], stdout=subprocess.PIPE) as proc:
                proc.wait()
                result['scm_branch'] = proc.stdout.read().decode()[2:].strip()

            self.__result = abs.SCM._post_process(result)
        finally:
            os.chdir(origin_wd)

    def result(self):
        return dict(self.__result)

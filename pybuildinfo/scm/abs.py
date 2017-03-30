#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
\file abs.py
\brief PyBuildInfo > SCM > ABS
\author Andrei Vorobev (http://www.ptaxa.net)
\date 2015
\copyright
Copyright © 2015 Andrei Vorobev (http://www.ptaxa.net) All rights reserved.
"""


import abc
import time
import platform
import os
import subprocess
try:
	import pwd
except:
	pass


class SCM(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def result(self):
        raise NotImplementedError();
    
    @staticmethod
    def _pre_process():
        pre = {}
        pre['scm_name'] = ''
        pre['scm_revisions'] = ''
        pre['scm_revisions_short'] = ''
        pre['scm_timestamp'] = ''
        pre['scm_rfc2822'] = ''
        pre['scm_author'] = ''
        pre['scm_author_email'] = ''
        pre['scm_message'] = ''
        pre['scm_message_escaping'] = ''
        pre['scm_version'] = '0.0.0'
        pre['scm_version_major'] = 0
        pre['scm_version_minor'] = 0
        pre['scm_version_patch'] = 0
        pre['scm_version_stable'] = 0x00
        pre['scm_version_tags'] = ''
        pre['build_time'] = ''
        pre['build_rfc2822'] = ''
        pre['build_system'] = ''
        pre['build_system_version'] = ''
        pre['build_machine'] = ''
        pre['build_node'] = ''
        pre['build_node_login'] = ''
        pre['build_toolchain'] = ''
        pre['build_toolchain_version'] = ''
        pre['build_target_system'] = ''
        pre['build_target_machine'] = ''
        return pre;

    @staticmethod
    def _ut_to_rfc2822(timestamp):
        if isinstance(timestamp, time.struct_time):
            return time.strftime("%a, %d %b %Y %H:%M:%S +0000", timestamp)
        else:
            return time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime(int(timestamp)))
        
    @staticmethod
    def _escape_string(str):
        for x in [['\t', '\\t'], ['\n', '\\n'], ['\r', '\\r'], ["'", "\\'"], ['"', '\\"']]:
            str = str.replace(x[0], x[1])
        return str

    @staticmethod
    def _post_process(result):
        for x in result:
            result[x] = str(result[x])

        result['scm_revisions_short'] = result['scm_revisions'][:7]

        if not result['scm_rfc2822']:
            result['scm_rfc2822'] = SCM._ut_to_rfc2822(result['scm_timestamp'])

        tmp = time.gmtime()
        if not result['build_time']:
            result['build_time'] = int(time.mktime(tmp))
        if not result['build_rfc2822']:
            result['build_rfc2822'] = SCM._ut_to_rfc2822(tmp)
        if not result['build_system']:
            result['build_system'] = platform.system()
        if not result['build_system_version']:
            result['build_system_version'] = platform.version()
            if 'linux' in platform.system().lower():
                try:
                    result['build_system_version'] = SCM._lsb_release()
                except:
                    result['build_system_version'] = platform.release()
                        
                
        if not result['build_machine']:
            result['build_machine'] = platform.machine()
        if not result['build_node']:
            result['build_node'] = platform.node()
        if not result['build_node_login']:
            try:
                result['build_node_login'] = os.getlogin()
            except FileNotFoundError:
                result['build_node_login'] = pwd.getpwuid(os.getuid())[0]

        return result

    @staticmethod
    def _lsb_release():
        try:
            with subprocess.Popen(['lsb_release', '-d'], stdout=subprocess.PIPE, stderr=subprocess.PIPE) as lbs:
                lbs.wait()
                result = lbs.stdout.readlines()[0].decode()
                description = 'description:'
                if result.lower().startswith(description):
                    return result[len(description):].strip()
                else:
                    raise RuntimeError()
        except:
            raise RuntimeError()

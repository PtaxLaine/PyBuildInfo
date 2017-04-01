# -*- coding: UTF-8 -*-
"""
Python Build Info Tool
VCS Module
"""
import logging
import os
from pybuildinfo.vcs.git import Git
from pybuildinfo.vcs.hg import Hg


def all_vcs():
    return [Git, Hg]


def detect_vcs(path):
    path = os.path.abspath(path)
    if not os.path.isdir(path):
        raise FileNotFoundError("{} not a directory".format(path))

    for x in all_vcs():
        try:
            if x(path).status()[0] == 0:
                return x
        except OSError:
            logging.info("detect_vcs skipping '%s' - not installed", x(void=True).name)

    return None


def vcs_by_name(name):
    name = name.lower()
    for x in all_vcs():
        if name in [a.lower() for a in x(void=True).alias]:
            return x
    return None

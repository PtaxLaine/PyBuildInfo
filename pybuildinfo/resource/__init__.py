# -*- coding: UTF-8 -*-
"""
Python Build Info Tool
Resource Module
"""
import os


def r_find(name):
    path = os.path.join(os.path.dirname(__file__), name)
    assert os.path.exists(path)
    return path


def r_open(name, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True, opener=None):
    return open(r_find(name), mode, buffering, encoding, errors, newline, closefd, opener)


def r_load(name, mode='r'):
    with r_open(name, mode) as fs:
        return fs.read()

#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import os
from setuptools import setup
import pybuildinfo


with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'README.md')) as fs:
    long_description = fs.read()

info = pybuildinfo.version_dict()

setup(
    name=info['name'],
    version=info['version'],
    description=info['description'],
    long_description=long_description,
    author=info['author'],
    author_email=info['author_email'],
    license=info['license'],
    url=info['url'],
    classifiers=info['classifiers'],

    package_data={'pybuildinfo.resource': ['default.hpp']},
    data_files = [("", ["LICENSE.md"])],
    packages=['pybuildinfo', 'pybuildinfo.resource', 'pybuildinfo.vcs'],
    entry_points={
        'console_scripts': [
            'pybuildinfo=pybuildinfo.cmd:main',
        ],
    }
)

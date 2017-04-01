#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
{
    "name": "PyBuildInfo",
    "version": "0.2.0",
    "license": "BSD 3-Clause License",
    "author": "Andrei V",
    "author_email": "andrei@ptaxa.net",
    "description": "Python Build Info Tool",
    "url": "https://github.com/PtaxLaine/PyBuildInfo",
    "date": "2015-2017",
    "classifiers": [
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: Microsoft",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.6"
    ]
}
"""


def version():
    return __doc__.strip()


def version_dict():
    import json
    return json.loads(__doc__)

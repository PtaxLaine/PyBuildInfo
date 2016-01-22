#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

from distutils.core import setup

setup(name='pybuildinfo',
      version='1.0',
      description='Python Build Info',
      author='Andrei V',
      author_email='andrei@ptaxa.net',
      url='https://github.com/PtaxLaine/pybuildinfo',
      package_data={'pybuildinfo.resource_data': ['BuildInfo.ini', 'example.hpp']},
      packages=['pybuildinfo', 'pybuildinfo.resource_data', 'pybuildinfo.scm', 'pybuildinfo.templating'],
     )

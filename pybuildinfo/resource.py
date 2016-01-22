#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
\file resource.py
\brief PyBuildInfo > Resource
\author Andrei Vorobev (http://www.ptaxa.net)
\date 2015
\copyright
Copyright © 2015 Andrei Vorobev (http://www.ptaxa.net) All rights reserved.
"""

import os

def get_resource_directory():
    return os.path.join(os.path.dirname(__file__), 'resource_data/')

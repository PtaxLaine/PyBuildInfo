#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
\file default.py
\brief PyBuildInfo > Templating > Default
\author Andrei Vorobev (http://www.ptaxa.net)
\date 2015
\copyright
Copyright © 2015 Andrei Vorobev (http://www.ptaxa.net) All rights reserved.
"""

from . import abs

class Template(abs.TemplateEngine):
    def __init__(self, template, dictonary):
        self.__template = template
        self.__dictonary = dictonary

    def __str__(self):
        result = self.__template
        for x in self.__dictonary:
            result = result.replace('${}$'.format(x), str(self.__dictonary[x]))
        return result

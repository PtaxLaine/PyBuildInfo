#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
\file abs.py
\brief PyBuildInfo > Templating > ABS
\author Andrei Vorobev (http://www.ptaxa.net)
\date 2015
\copyright
Copyright © 2015 Andrei Vorobev (http://www.ptaxa.net) All rights reserved.
"""

import abc


class TemplateEngine(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __str__(self):
        raise NotImplementedError();

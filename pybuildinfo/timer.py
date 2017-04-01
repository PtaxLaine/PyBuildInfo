# -*- coding: UTF-8 -*-
"""
Python Build Info Tool
Timer
"""
import time
import logging


def log(func):
    def test(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        stop = time.time()
        logging.info("function {} execution time is {:0.4F}s".format(str(func), stop-start))
        return result
    return test

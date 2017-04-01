import unittest
import os
import pybuildinfo.resource as resource


class TestResource(unittest.TestCase):
    def test_main(self):
        path = resource.r_find('default.hpp')
        path_test = os.path.dirname(__file__)
        path_test = os.path.join(path_test, '..', 'pybuildinfo', 'resource', 'default.hpp')
        path_test = os.path.abspath(path_test)
        self.assertEqual(path, path_test)

        with open(path_test) as fs:
            self.assertEqual(resource.r_load('default.hpp'), fs.read())

        with open(path_test) as fs:
            fs2 = resource.r_open('default.hpp')
            self.assertEqual(fs2.read(), fs.read())

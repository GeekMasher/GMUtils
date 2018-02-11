#!/usr/bin/env python

import os
import unittest
import threading
import time

from gmutils import Config
from gmutils.utils.paths import Paths


class UtilsPathsTest(unittest.TestCase):

    def setUp(self):
        self.paths = Paths()

    def tearDown(self):
        pass

    def test_01_init(self):
        
        # Check standard paths were added
        self.assertIsNotNone(self.paths.get('project'))
        self.assertIsNotNone(self.paths.get('project_libs'))
        self.assertIsNotNone(self.paths.get('project_data'))

    def test_02_load_assumefile(self):
        
        self.paths.load(
            test_01={
                'path': '/tmp/gmutils'
            }
        )

        self.assertEqual(self.paths.get('test_01'), '/tmp/gmutils')

        full_results = self.paths.getFull('test_01')

        self.assertFalse(full_results['required'])
        self.assertFalse(full_results['create'])
        self.assertFalse(full_results['directory'])
    
    def test_03_load_create(self):
        
        self.paths.load(
            test_02={
                'path': '/tmp/gmutils',
                'create': True
            }
        )

        full_results = self.paths.getFull('test_02')

        self.assertTrue(full_results['create'])
        # make sure the file was created
        self.assertTrue(os.path.exists('/tmp/gmutils'))

    def test_04_load_required(self):
        
        self.paths.load(
            test_03={
                'path': '/tmp/gmutils',
                'required': True
            }
        )

        full_results = self.paths.getFull('test_03')

        self.assertTrue(full_results['required'])

        # TODO: check for when the required file doesn't match


    def test_10_remove(self):
        self.paths.add('test_10', '/random/path/to/file.txt')

        self.assertTrue(self.paths.get('test_10'))

        self.paths.remove('test_10')
        self.assertFalse(self.paths.get('test_10'))


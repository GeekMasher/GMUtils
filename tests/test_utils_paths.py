#!/usr/bin/env python

import os
import unittest
import threading
import time

import gmutils

from gmutils import Config
from gmutils.utils.paths import Paths


class UtilsPathsTest(unittest.TestCase):

    def setUp(self):
        self.paths = Paths(
            duplications=True
        )
        self.paths.duplications = False

    def tearDown(self):
        self.paths.clear()

    def test_01_init(self):

        self.assertFalse(self.paths.duplications)
        self.assertTrue(self.paths.security_checks)

        # Check standard paths were added
        self.assertIsNotNone(self.paths.get('project'))
        self.assertIsNotNone(self.paths.get('project-libs'))
        self.assertIsNotNone(self.paths.get('project-data'))

    def test_02_load(self):

        self.paths.load(
            duplications=True,
            paths={
                'gmutils_tmp': {
                    'path': '/tmp/gmutils/'
                },
                'gmutils_tmpfile': {
                    'path': '/tmp/gmutils/test.txt'
                }
            }
        )

        self.assertTrue(self.paths.duplications)

        self.assertEqual(self.paths.get('gmutils_tmpfile'), '/tmp/gmutils/test.txt')
        self.assertEqual(self.paths.get('gmutils_tmp'), '/tmp/gmutils/')

        full_results_01 = self.paths.getFull('gmutils_tmpfile')
        self.assertFalse(full_results_01['required'])
        self.assertFalse(full_results_01['create'])
        self.assertFalse(full_results_01['directory'])

        full_results_02 = self.paths.getFull('gmutils_tmp')
        self.assertFalse(full_results_02['required'])
        self.assertFalse(full_results_02['create'])
        self.assertTrue(full_results_02['directory'])

    def test_03_create(self):

        self.paths.add('test_02', '/tmp/gmutils', create=True)

        full_results = self.paths.getFull('test_02')

        self.assertTrue(full_results['create'])
        # make sure the file was created
        self.assertTrue(os.path.exists('/tmp/gmutils'))

    def test_04_required(self):
        self.paths.add('test_04', '/tmp/gmutils', required=True)

        full_results = self.paths.getFull('test_04')
        self.assertTrue(full_results['required'])

        # check if an exception is thrown if the file doesn't exist
        with self.assertRaises(gmutils.utils.exceptions.GMException) as context:
            self.paths.add('test_04_1', '/tmp/gmutils/random_path/', required=True)

    def test_06_mime(self):
        self.paths.add(
            'test_06', Paths.join(self.paths.get('cwd'), 'tests', 'test-data')
        )

        self.assertIsNotNone(self.paths.get('test_06'))
        self.assertTrue(os.path.exists(self.paths.get('test_06')))

        self.paths.add(
            'test_06_json',
            Paths.join(self.paths.get('test_06'), 'testfile.json'),
            mime='application/json'
        )

        with self.assertRaises(gmutils.utils.exceptions.GMSecurity) as context:
            self.paths.add(
                'test_06_xml',
                Paths.join(self.paths.get('test_06'), 'testfile.xml'),
                mime='not/x_m_l'
            )

    def test_07_directory(self):
        self.paths.add('test_07', '/tmp/gmutils', directory=True)

        full_results = self.paths.getFull('test_07')
        self.assertTrue(full_results['directory'])

        # based off name
        self.paths.add('dir-tmp', '/tmp')
        full_results = self.paths.getFull('dir-tmp')
        self.assertTrue(full_results['directory'])

        # detect dir
        self.paths.add('test_07_1', '/tmp')
        full_results = self.paths.getFull('test_07_1')
        self.assertTrue(full_results['directory'])

    def test_08_duplications(self):

        self.paths.add('test_08', '/tmp/gmutils/test_file_01.txt')

        self.assertIsNotNone(self.paths.get('test_08'))

        with self.assertRaises(gmutils.utils.exceptions.GMException) as context:
            # try to overwrite `test_08`
            self.paths.add('test_08', '/tmp/gmutils/test_file_02.txt')

        # Turn on duplications
        self.paths.duplications = True
        self.paths.add('test_08', '/tmp/gmutils/test_file_03.txt')

    def test_09_clear(self):
        self.paths.clear()
        self.assertDictEqual(Paths.__PATHS__, {})

    def test_10_remove(self):
        self.paths.add('test_10', '/random/path/to/file.txt')

        self.assertTrue(self.paths.get('test_10'))

        self.paths.remove('test_10')
        self.assertFalse(self.paths.get('test_10'))

    def test_11_recursive(self):
        rnd_path = '/tmp/gm/random/path/0712346'
        self.paths.add(
            'randompath_0712346', rnd_path, create=True, directory=True
        )

        self.assertTrue(os.path.exists(rnd_path))



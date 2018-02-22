#!/usr/bin/env python

import os
import json
import unittest
import threading
import time

from gmutils import Config
from gmutils.utils.exceptions import GMException


class UtilsConfigTest(unittest.TestCase):

    def setUp(self):
        # TODO: make this path cross-platform
        if not Config.paths.get('dir-tmp'):
            Config.paths.add(
                'dir-tmp', '/tmp/gmutils',
                directory=True,
                create=True
            )

    def tearDown(self):
        pass

    def test_00_defaults(self):

        self.assertEqual(Config.ENV, 'TESTING')

    def test_04_loadFile(self):

        # Load empty JSON file

        # Load non-supported formats
        with self.assertRaises(GMException) as context:
            Config.loadFile('./test-data/testfile.xml')


    def test_10_export(self):
        tmp_export = os.path.join(
            Config.paths.get('dir-tmp'), 'export_01.json'
        )

        # Create a `private` testing var
        Config.TESTING_EXPORT = 'testing string'

        Config.export(path=tmp_export)

        self.assertTrue(os.path.exists(tmp_export))
        self.assertEqual(
            Config.paths.checkMime(tmp_export), 'application/json'
        )

        with open(tmp_export, 'r') as fl:
            EXPORTED_DATA = json.loads(fl.read())

        # Make sure certain variables/functions are now exported
        self.assertTrue(EXPORTED_DATA.get('TESTING_EXPORT'))
        self.assertFalse(EXPORTED_DATA.get('load'))

        self.assertTrue(EXPORTED_DATA.get('ENV'))
        self.assertEqual(EXPORTED_DATA.get('ENV'), Config.ENV)


#!/usr/bin/env python

import os
import json
import unittest
import threading
import time

from gmutils.utils.constants import Constants


class UtilsConstantsTest(unittest.TestCase):

    def setUp(self):
        self.const = Constants()

        self.variables_01 = {
            'prefix': {
                'HTTP': 'http://',
                'HTTPS': 'https://',
                'FTP': 'ftp://'
            },
            'THREADS': {
                'MAX_THREADS': 10,
                'pools': {
                    'prod_01': {
                        'testing01': 'testing.example.com:4444'
                    }
                }
            },
            'trusted_hosts': [
                'geekmasher.com',
                'blog.geekmasher.com',
                'random.subdomain.geekmasher.com',
            ]
        }

    def tearDown(self):
        pass

    def test_01_add(self):
        
        self.const.add('MAX_THREAD', 10)

        self.assertTrue(Constants.__CONSTS__.get('MAX_THREAD'))
        self.assertEqual(Constants.__CONSTS__.get('MAX_THREAD'), 10)

    def test_02_get(self):
        # self.const.add('MAX_THREAD', 10)
        self.assertEqual(
            self.const.get('MAX_THREAD'), 10
        )

        self.const.add('MAX_THREAD', 20)

        self.assertEqual(
            self.const.get('MAX_THREAD'), 20
        )

    def test_03_load(self):
        
        self.const.load(
            **self.variables_01
        )

        self.assertTrue(self.const.get('prefix'))
        self.assertDictEqual(
            self.const.get('prefix'),
            self.variables_01['prefix']
        )
        self.assertTrue(self.const.get('trusted_hosts'))
        self.assertListEqual(
            self.const.get('trusted_hosts'),
            self.variables_01['trusted_hosts']
        )
        
    def test_05_getquery(self):
        self.assertTrue(self.const.get('prefix'))
        self.assertEqual(
            self.const.get('prefix.HTTP'), 'http://'
        )

        self.assertTrue(self.const.get('THREADS'))
        self.assertTrue(self.const.get('THREADS.MAX_THREADS'))
        self.assertEqual(
            self.const.get('THREADS.pools.prod_01.testing01'),
            'testing.example.com:4444'
        )

    def test_06_clear(self):
        self.assertTrue(
            self.const.get('MAX_THREAD')
        )

        self.const.clear()

        self.assertFalse(
            self.const.get('MAX_THREAD')
        )

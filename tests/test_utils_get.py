#!/usr/bin/env python

import unittest
import threading
import time

from gmutils import Config
from gmutils.utils.exceptions import GMException
from gmutils.utils.get import get, _query_extracter



class GetTest(unittest.TestCase):

    def test_00_queryext(self):
        self.assertListEqual(
            _query_extracter('test'),
            ['test']
        )
        self.assertListEqual(
            _query_extracter('test.me.out'),
            ['test', 'me', 'out']
        )

        with self.assertRaises(GMException) as context:
            _query_extracter(0)


    def test_01_init(self):
        test = {
            'test01': {
                'test01_sub': 'winning'
            }
        }

        self.assertEqual(
            get(test, 'test01.test01_sub'), 'winning'
        )


    def test_01_simple(self):
        
        test01 = {
            'test': 'correct'
        }
        self.assertEqual(
            get(test01, 'test'),
            'correct'
        )

    def test_02_incorrect(self):
        
        test02 = {
            'testme': 'wrong'
        }
        self.assertEqual(
            get(test02, 'test'),
            None
        )

    def test_03_default(self):
        
        test03 = {
            'testthis': 'can not find me'
        }

        self.assertEqual(
            get(test03, 'test', default='thisiscorrect'),
            'thisiscorrect'
        )





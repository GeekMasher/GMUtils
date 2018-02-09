#!/usr/bin/env python

import unittest
import threading
import time

from gmutils import Config
from gmutils.helpers.helpme_thread import createThreads



class ThreadTest(unittest.TestCase):

    def tearDown(self):
        Config.haltThreads()

    def pauseAndStopCurrentTests(self):
        time.sleep(2)
        Config.haltThreads()

    def test_01_wrapper(self):
        name = 'test_wrapper'
        # Use the simple wrapper
        @createThreads(name)
        def simple_function():
            time.sleep(.5)

        self.assertEqual(len(Config.THREADS), 1)

        for thr in Config.THREADS:
            self.assertIsInstance(thr, threading.Thread)
            self.assertEqual(thr.name, 'test_wrapper-01')

        self.pauseAndStopCurrentTests()

        self.assertEqual(len(Config.THREADS), 0)

    def test_02_multiple(self):

        self.assertEqual(len(Config.THREADS), 0)

        # Use the simple wrapper
        @createThreads('test_multiple', thread_count=3)
        def simple_function():
            sleep(.5)

        self.assertEqual(len(Config.THREADS), 3)

        for index, thr in enumerate(Config.THREADS):
            self.assertEqual(thr.name, 'test_multiple-0{}'.format(index+1))

        self.pauseAndStopCurrentTests()


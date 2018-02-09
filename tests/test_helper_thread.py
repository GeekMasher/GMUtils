#!/usr/bin/env python

import unittest
from time import sleep

from gmutils import Config
from gmutils.helpers.helpme_thread import createThreads



class ThreadTest(unittest.TestCase):

    def tearDown(self):
        Config.haltThreads()

    def pauseAndStopCurrentTests(self):
        sleep(2)
        Config.haltThreads()

    def test_01_wrapper(self):
        name = 'test_wrapper'
        # Use the simple wrapper
        @createThreads(name)
        def simple_function():
            sleep(.5)

        self.assertEqual(len(Config.THREADS), 1)

        self.pauseAndStopCurrentTests()

        self.assertEqual(len(Config.THREADS), 0)

    def test_02_multiple(self):

        # Use the simple wrapper
        @createThreads('test_multiple', thread_count=3)
        def simple_function():
            sleep(.5)

        self.pauseAndStopCurrentTests()


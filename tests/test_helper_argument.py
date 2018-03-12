#!/usr/bin/env python

import os
import sys 
import unittest
import threading
import time

sys.path.append('src')

from gmutils import Config
from gmutils.helpers.helpme_argument import Arguments


class ArgumentsTest(unittest.TestCase):

    def tearDown(self):
        pass

    def test_00_init(self):
        pass

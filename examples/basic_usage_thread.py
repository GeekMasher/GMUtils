#!/usr/bin/env python

from time import sleep

from gmutils import Config
from gmutils.helpers.helpme_thread import createThreads

# Define a function that you want to thread and wrap the function with
# `createThreads()` and setting a name you want to give the function.

@createThreads('simple_func')
def simple_function():
    time(.5)

# Kill the function and threads using:
Config.haltThreads()

# Note: This will kill all the threads you have running

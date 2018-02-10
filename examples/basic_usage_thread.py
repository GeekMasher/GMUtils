#!/usr/bin/env python

from time import sleep

from gmutils import Config
from gmutils.helpers.helpme_thread import createThreads

# Define a function that you want to thread and wrap the function with
# `createThreads()` and setting a name you want to give the function.

@createThreads('my-little-function')
def simple_function():
    sleep(.5)

# You can also create multiple threads in the same way as before
# This will spawn 3 threads at the same time 

@createThreads('my-many-functions', thread_count=3)
def simple_func2():
    sleep(.5)

# You can also add pauses between each thread function call

@createThreads('my-slow-function', waitfor=5)
def simple_func3():
    sleep(.5)

# You can also get access to the Thread objects that have been created
for thread in Config.THREADS:
    print(thread.name)

# Kill the function and threads using:
Config.haltThreads()

# Note: This will kill all the threads you have running

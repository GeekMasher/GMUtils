#!/usr/bin/env python

from time import sleep

from gmutils.utils.config import Config


def createThreads(name, thread_count=1, waitfor=0):
    """ The createThreads() function is a Python wrapper that allows you to
    quickly and easily create thead-able tasks.

    If the thead_count is greater than 1, a `-` separator and an interger will
    be attached automatically to the end of the name string.

    Example:
    createThreads('test', thread_count=3)

        <Thread name='test-01' />
        <Thread name='test-02' />
        <Thread name='test-03' />

    :param name: The name of the thread
    :type name: type str
    :param thread_count: The number of threads that will be spawned
    :type thread_count: type int
    :param waitfor: The wait timer between function execution
    :type waitfor: type double
    """
    def thread_wrapper(func):

        def thread_call(*args, **kwargs):
            while not Config.HALT:
                sleep(waitfor)
                return func(*args, **kwargs)

        return thread_call
    return thread_wrapper

#!/usr/bin/env python

import time
import threading

from gmutils.utils.config import Config
from gmutils.helpers.helpme_printing import Printing


def main():
    """The main function allows an applications main thread to do nothing
    except halt all threads on KeyboardInterrupt.
    """

    while True:
        try:
            time.sleep(.25)
        except KeyboardInterrupt:
            break
        except Exception as err:
            if Config.isTesting():
                Printing.error(
                    1, 'Unknown exception ins main thread',
                    exp=err
                )
                break

    Config.haltThreads()


def createThreads(name, thread_count=1, waitfor=0):
    """This is a wrapping / annotation to allow applications to wrapper
    functions that they want to thread quickly. This allows you to quickly
    spwan threads by wrapping functions

    Arguments:
        name {str} -- name of the groups of threads

    Keyword Arguments:
        thread_count {int} -- the number of threads spawned (default: {1})
        waitfor {int} -- default wait time between function executions
        (default: {0})
    """

    def thread_wrapper(func):
        def thread_call(*args, **kwargs):
            ret_val = None
            while not Config.HALT:
                time.sleep(waitfor)
                ret_val = func(*args, **kwargs)

            return ret_val

        for thread_id in range(1, thread_count+1):
            name_thread = '{}-{:02d}'.format(name, thread_id)

            new_thread = threading.Thread(
                name=name_thread, group=None, target=thread_call
            )

            new_thread.start()
            Config.THREADS.append(new_thread)

        return thread_call
    return thread_wrapper

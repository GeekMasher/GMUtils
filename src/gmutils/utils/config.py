#!/usr/bin/env python

from os.path import exists, join

from gmutils.utils.paths import Paths

class Config:
    ENV = 'TEST'

    HALT = False
    THREADS = []

    paths = Paths()

    @staticmethod
    def load():
        """ The load function runs though a predeterminded list of of loading
        paths, env vars and command argvs.
        """

        # TODO: load from `Project root`

        # TODO: load from `Env vars`

        # TODO: load from `CLI arguments`
        return

    @staticmethod
    def loadFile(path_file):
        return

    @staticmethod
    def isTesting():
        """ This function is used to determine if the current enviroment is for
        testing or production.

        :return: returns a boolean if the current system is in testing or prod
        :rtype: boolean
        """
        test_strings = [
            'TEST', 'TESTING', 'DEV', 'DEVELOPMENT'
        ]
        return True if Config.ENV.upper() in test_strings else False

    @staticmethod
    def haltThreads(name=None):
        """ This function is used to stop all registered threads added to the
        `Config.THREADS` list. This will set the `Config.HALT` boolean to True
        which should make stop threads from executing if they are using the
        `helpme_thread` wrappers.
        """
        Config.HALT = True

        for thread in Config.THREADS:
            thread.wait(timeout=5)

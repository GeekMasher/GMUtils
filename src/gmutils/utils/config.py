#!/usr/bin/env python

from os.path import exists, join

from gmutils.utils.paths import Paths

class Config:
    ENV = 'TEST'

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

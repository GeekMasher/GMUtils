#!/usr/bin/env python

from os.path import exists, join
from json import loads

from gmutils.utils.paths import Paths
from gmutils.utils.exceptions import GMException

class Config:
    ENV = 'TEST'

    HALT = False
    THREADS = []

    quite = False

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
        if exists(path_file) and Config.paths.checkMime(path_file, 'application/json'):
            with open(path_file, 'r') as config_file:
                conf = loads(config_file.read())

            Config.loadDict(conf)

    @staticmethod
    def loadDict(config_dct):
        if not isinstance(config_dct, dict):
            raise GMException('Config.load only supports dicts')

        for key, value in config_dct.items():
            if key.startswith('_') or not hasattr(Config, key):
                continue
            attr = getattr(Config, key)
            # Make sure it isn't a function
            if callable(attr):
                continue
            
            if isinstance(value, dict):
                # Check if the object has a function called `load`
                if hasattr(attr, 'load') and callable(getattr(attr, 'load')):
                    attr.load(**value)
                # Check if the `__setattr__` function is present
                elif hasattr(attr, '__setattr__'):
                    for attr_k, attr_v in value.items():
                        attr.__setattr__(attr_k, attr_v)
            elif isinstance(value, list):
                if hasattr(attr, 'append'):
                    for v in value:
                        attr.append(v)
            else:
                setattr(Config, key, value)

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
        # TODO: add support for `name` halting functionality
        Config.HALT = True

        for thread in Config.THREADS:
            thread.join(timeout=5)

        Config.THREADS = []

    @staticmethod
    def export(path):
        pass

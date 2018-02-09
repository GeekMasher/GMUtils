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



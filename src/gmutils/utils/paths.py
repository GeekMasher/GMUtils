#!/usr/bin/env python

from os.path import exists, join, abspath, dirname
from sys import modules

import logging


class Paths:
    __PATHS__ = {}

    def __init__(self, **paths):
        """
        """

        __project__ = modules['__main__']
        if hasattr(__project__, '__file__'):
            # Add standard project paths
            self.add(
                'project', abspath(dirname(__project__.__file__)),
                directory=True
            )
            self.add(
                'project_libs', join(self.get('project'), 'libs'),
                directory=True
            )
            self.add(
                'project_data', join(self.get('project'), 'data'),
                directory=True
            )

        self.load(**paths)

    def load(self, **paths):
        """
        """
        for key, value in paths.items():
            if key.startswith('_'):
                continue

            self.add(key, value)

    def add(self, name, path, **kargvs):
        """
        """

        if name.startswith('_'):
            raise Exception('Unallowed private path being set')

        if Paths.__PATHS__.get(name):
            logging.info("PATHS: overridding key `{}`".format(name))

        Paths.__PATHS__[name] = path

        # is DIR
        if name.startswith('dir-') or name.startswith('dir_'):
            directory = True


        if kargvs.get('create') and not kargvs.get('directory'):
            # if the file doesn't exist, create it
            if not exists(path):
                with open(path, 'w') as tmp_file:
                    tmp_file.write("")
        elif kargvs.get('create') and kargvs.get('directory'):
            # if the dir doesn't exist, create it
            if not exists(path):
                makedirs(path)

    def _parseAndValidateAddData(self, data):
        return_data = {}



        return return_data

    def get(self, name):
        """
        """
        if Paths.__PATHS__.get(name):
            return Paths.__PATHS__[name]
        return None


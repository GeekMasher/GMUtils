#!/usr/bin/env python

from argparse import ArgumentParser

from gmutils.utils.exceptions import GMException


class Arguments(ArgumentParser):
    def __init__(self, **kargvs):
        options = kargvs

        options['description'] = ''

        super(ArgumentParser).__init(**kargvs)
        self.defaults()

        self._results = None

    def load(self, **options):
        """The load function allows for

        Arguments:
            **options {[type]} -- [description]
        """
        for arg_name, arg_options in options.items():
            pass

    def defaults(self):

        # default groups
        self.add_argument_group('system')

        self.add_argument('-v', '--version')
        self.add_argument('-vvv', '--verbose')
        self.add_argument('-c', '--config')


    def get(self, argument):
        if self._results is None:
            self._results = self.parse_args()

        if hasattr(self._results, argument):
            return getattr(self._results, argument)
        raise GMException('Argument Key does not exist')

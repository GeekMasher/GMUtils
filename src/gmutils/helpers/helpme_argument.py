#!/usr/bin/env python

from argparse import ArgumentParser

from gmutils.utils.exceptions import GMException


class Arguments(ArgumentParser):
    def __init__(self, **kargvs):
        options = kargvs
        self._groups = {}

        options['description'] = ''

        super().__init__(**kargvs)
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
        self._groups['system'] = self.add_argument_group(
            'system',
            'System Operation'
        )

        self._groups['system'].add_argument('-v', '--version')
        self._groups['system'].add_argument('-vvv', '--verbose')
        self._groups['system'].add_argument('-c', '--config')


    def get(self, argument):
        if self._results is None:
            self._results = self.parse_args()

        if hasattr(self._results, argument):
            return getattr(self._results, argument)
        raise GMException('Argument Key does not exist')

#!/usr/bin/env python

from argparse import ArgumentParser
from logging import getLogger
from gmutils.utils.exceptions import GMException

logger = getLogger(__name__)

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
        logger.warning('Arguments() does not currently support loading')

    def defaults(self):

        # default groups
        self._groups['system'] = self.add_argument_group(
            'system',
            'System Operations'
        )

        self._groups['system'].add_argument(
            '-v', '--version', action='store_true'
        )
        self._groups['system'].add_argument(
            '-vvv', '--verbose', action='store_true'
        )
        self._groups['system'].add_argument(
            '-q', '--quite', action='store_true'
        )

        self._groups['system'].add_argument(
            '-c', '--config', action='append'
        )

    def get(self, argument):
        if hasattr(self._results, argument):
            return getattr(self._results, argument)
        raise GMException('Argument Key does not exist')

    def __export__(self):
        ret_val = {
            'groups': [str(grp) for grp in self._groups]
        }
        return ret_val

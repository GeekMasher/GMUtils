#!/usr/bin/env python

from argparse import ArgumentParser
from logging import getLogger
from gmutils.utils.exceptions import GMException

logger = getLogger(__name__)


class Arguments(ArgumentParser):
    def __init__(self, **options):
        """Arguments allows you to create a more powerful experience with
        Argument parsing and loading from configuration files.

        Arguments:
            **kargvs {dict} -- argument options
        """
        self._groups = {}

        options['description'] = ''

        super().__init__(**options)

        self.defaults()

        self._results = None

    def load(self, **options):
        """The load function allows for

        Arguments:
            **options {dict} -- the different options + arguments
        """
        logger.warning('Arguments() does not currently support loading')

    def defaults(self):
        """Default arguments that get added to Arguments()
        """

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
        """Gets the argument by name

        Arguments:
            argument {str} -- argument name

        Raises:
            GMException -- if the argument does not exist

        Returns:
            object -- arguments
        """

        if hasattr(self._results, argument):
            return getattr(self._results, argument)
        raise GMException('Argument Key does not exist')

    def __export__(self):
        """Export functionality for Config().export()

        Returns:
            dict -- dict to export
        """

        ret_val = {
            'groups': [str(grp) for grp in self._groups]
        }
        return ret_val

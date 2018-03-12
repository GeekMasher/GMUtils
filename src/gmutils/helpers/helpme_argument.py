#!/usr/bin/env python

from argparse import ArgumentParser, ArgumentError
from logging import getLogger
from gmutils.utils.exceptions import GMException

from cerberus import Validator

logger = getLogger(__name__)


class Arguments(ArgumentParser):
    def __init__(self, **options):
        """Arguments allows you to create a more powerful experience with
        Argument parsing and loading from configuration files.

        Arguments:
            **kargvs {dict} -- argument options
        """
        self._groups = {}
        self._parameters = []
        self._groups_export = []

        options['description'] = ''

        super().__init__(**options)

        self.defaults()

        self._results = None

    def load(self, **options):
        """The load function allows for

        Arguments:
            **options {dict} -- the different options + arguments
        """
        validator = Validator()
        
        if options.get('groups'):
            for group in options.get('groups'):
                if not validator.validate(group, GROUPS_SCHEMA):
                    raise GMException(
                        'Arguments `groups` schema validation failed'
                    )

                title = group.get('title')
                description = group.get('description')

                new_group = self.add_argument_group(title, description)

                self._groups[title] = new_group

        if options.get('parameters'):
            for param in options.get('parameters'):
                if not validator.validate(param, PARAMETERS_SCHEMA):
                    raise GMException(
                        'Arguments `parameters` schema validation failed'
                    )

                param_options = param.pop('options')
                param_group = param.pop('group', '')

                if self._groups.get(param_group):
                    self._groups.get(param_group).add_argument(
                        *param_options, **param
                    )
                else:
                    self.add_argument(
                        *param_options, **param
                    )

    def add_argument(self, *argv, **kargvs):
        Arguments._report_parameter(
            options=argv,
            **kargvs
        )
        return super().add_argument(*argv, **kargvs)

    def add_argument_group(self, *argv, **kargvs):
        title = argv[0] if len(argv) > 0 else ''
        # If the group already exists
        if self._groups.get(title):
            return self._groups.get(title)
        else:
            grp = super().add_argument_group(*argv, **kargvs)

        from gmutils import Config
        if Config.arguments is None:
            Config.arguments = self

        Config.arguments._groups_export.append(
            {
                'title': argv[0] if len(argv) > 0 else '',
                'description': argv[1] if len(argv) > 1 else ''
            }
        )

        def _report_group_parameter(*h_argv, **h_kargvs):
            print('>>>> ' + str(h_argv))
            Arguments._report_parameter(
                options=h_argv,
                group=grp.title,
                **h_kargvs
            )
            try:
                grp._hooked_add_argument(*h_argv, **h_kargvs)
            except ArgumentError:
                pass

        setattr(grp, '_hooked_add_argument', getattr(grp, 'add_argument'))
        setattr(grp, 'add_argument', _report_group_parameter)

        return grp

    @staticmethod
    def _report_parameter(**kargvs):

        from gmutils import Config
        blacklist = ['help']
        if kargvs.get('action') not in blacklist:
            Config.arguments._parameters.append(kargvs)

    def defaults(self):
        """Default arguments that get added to Arguments()

        Standard Arguments:
            - `-c` or `--config` to set the locaitons of multiple configuration
                files
            - `-q` or `--quiet` to set if the application can print of the
                console
            - `-vvv` or `--verbose` to set the application verbosity level
            - `-v` or `--version` to display the softwares version and exit the
                program
            - `--help` to display the help options
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
            '-q', '--quiet', action='store_true'
        )

        self._groups['system'].add_argument(
            '-c', '--config', action='append'
        )

    def get(self, argument, default=None):
        """Gets the argument by name

        Arguments:
            argument {str} -- argument name
            default {None} -- if the argument does not exist, this is the
                return value

        Raises:
            GMException -- if the argument does not exist

        Returns:
            object -- arguments
        """

        if hasattr(self._results, argument):
            return getattr(self._results, argument)
        return default

    def __export__(self):
        """Export functionality for Config().export()

        Returns:
            dict -- dict to export
        """
        from gmutils import Config
        ret_val = {
            'groups': Config.arguments._groups_export,
            'parameters': Config.arguments._parameters
        }
        return ret_val


PARAMETERS_SCHEMA = {
    'action': {'type': 'string', 'required': False},
    'dest': {'type': 'string'},
    'default': {'type': 'string'},
    'group': {'type': 'string', 'required': False},
    'help': {'type': 'string', 'required': False},
    'options': {'type': 'list', 'schema': {'type': 'string'}}
}


GROUPS_SCHEMA = {
    'title': {'type': 'string'},
    'description': {'type': 'string'}
}

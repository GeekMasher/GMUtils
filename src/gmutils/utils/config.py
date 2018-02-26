#!/usr/bin/env python

from os import environ
from os.path import exists, join
from sys import modules, exit
from json import loads, dumps
from inspect import isclass, ismodule

from gmutils.utils.paths import Paths
from gmutils.utils.exceptions import GMException, GMSecurity
from gmutils.helpers.helpme_argument import Arguments


class Config:
    ENV = environ.get('PROJECT_ENV', 'TESTING')
    quite = False

    HALT = False
    THREADS = []

    arguments = Arguments()

    paths = Paths()


    @staticmethod
    def load():
        """ The load function runs though a predeterminded list of of loading
        paths, env vars and command argvs.
        """
        # load from `Project root`
        pro_path = Config.paths.get('config-project')
        if exists(pro_path):
            Config.loadFile(pro_path)

        # load from `Env vars`
        env_path = environ.get('PROJECT_CONFIG')
        if env_path is not None and exists(env_path):
            Config.loadFile(env_path)

        # TODO: load from `CLI arguments`
        return

    @staticmethod
    def loadFile(path_file):
        if Config.paths.check(path_file, mime='application/json'):
            with open(path_file, 'r') as config_file:
                conf = loads(config_file.read())

            Config.loadDict(conf)
        else:
            raise GMException("Configuration file of an unsupport type")

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
    def initCLI():
        from gmutils.helpers.helpme_printing import Printing
        err = None

        Config.arguments._results = Config.arguments.parse_args()

        try:
            if Config.arguments.get('version'):
                if hasattr(modules.get('__main__'), '__version__'):
                    print('v' + modules.get('__main__').__version__)
                    exit(0)
            elif Config.arguments.get('config'):
                for config in Config.arguments.get('config'):
                    Config.loadFile(config)

        except (GMException, GMSecurity) as context:
            err = context

        if not Config.quite:
            Printing.banner()
        if err is not None:
            Printing.error('CLI', str(err), err)


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
    def export(path=None, export_object=None, depth=1):

        def _export_recursively(current_object, current_depth=0):
            DATA = {}

            if current_depth > depth+1:
                return

            if hasattr(current_object, '__export__'):
                return current_object.__export__()

            for variable_name in dir(current_object):
                if variable_name.startswith('_'):
                    continue

                attr = getattr(current_object, variable_name)
                if callable(attr) or attr is None:
                    continue

                if hasattr(attr, '__module__'):
                    new_depth = current_depth+1
                    ret_val = _export_recursively(
                        attr, current_depth=new_depth
                    )
                else:
                    ret_val = attr

                if ret_val is not None:
                    DATA[variable_name] = ret_val

            return DATA
        # default export == `Config()`
        if export_object is None:
            EXPORT_DATA = _export_recursively(Config)
        # Support for arbitrary to be passed in
        else:
            EXPORT_DATA = _export_recursively(export_object)

        if path is not None:
            # write to file
            with open(path, 'w') as export_fl:
                export_fl.write(
                    dumps(EXPORT_DATA, indent=2, sort_keys=True)
                )
        else:
            from gmutils.helpers.helpme_printing import Printing
            Printing.data('Config()', dumps(EXPORT_DATA, indent=2, sort_keys=True))

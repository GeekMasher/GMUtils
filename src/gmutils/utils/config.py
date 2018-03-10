#!/usr/bin/env python

from os import environ
from os.path import exists, join
from sys import modules, exit
from json import loads, dumps
from inspect import isclass, ismodule
from logging import getLogger

from gmutils.utils.paths import Paths
from gmutils.utils.exceptions import GMException, GMSecurity
from gmutils.helpers.helpme_argument import Arguments


logger = getLogger(__name__)


class Config:
    ENV = environ.get('PROJECT_ENV', 'TESTING')
    quite = False

    HALT = False
    THREADS = []

    arguments = Arguments()

    paths = Paths()

    @classmethod
    def load(cls):
        """ The load function runs though a predeterminded list of of loading
        paths, env vars and command argvs.
        """
        # load from `Project root`
        pro_path = Config.paths.get('config-project')
        if exists(pro_path):
            cls.loadFile(pro_path)

        # load from `Env vars`
        env_path = environ.get('PROJECT_CONFIG')
        if env_path is not None and exists(env_path):
            cls.loadFile(env_path)

        # TODO: load from `CLI arguments`
        return

    @classmethod
    def loadFile(cls, path_file):
        """You can load a config from file from this function. This is where
        addition support for different loads can be placed.

        Arguments:
            path_file {str} -- path to a configuration file

        Raises:
            GMException -- If the configuration file doesn't match the\
            critiria, this exception will be thrown.
        """

        if cls.paths.check(path_file, mime='application/json'):
            with open(path_file, 'r') as config_file:
                conf = loads(config_file.read())

            cls.loadDict(conf)
        else:
            raise GMException("Configuration file of an unsupport type")

    @classmethod
    def loadDict(cls, config_dct):
        """The loadDict function allows for dict objects to be loaded into the
        Config() class.

        Arguments:
            config_dct {dict} -- the dict to be loaded into Config()

        Raises:
            GMException -- If a object that isn't a `dict`, this error will be\
            thrown
        """

        if not isinstance(config_dct, dict):
            raise GMException('Config.load only supports dicts')

        for key, value in config_dct.items():
            if key.startswith('_') or not hasattr(cls, key):
                continue
            attr = getattr(cls, key)
            # Make sure it isn't a function
            if callable(attr):
                continue

            if isinstance(value, dict):
                # Check if the object has a function called `load`
                if hasattr(attr, 'load') and callable(getattr(attr, 'load')):
                    attr.load(**value)
                # Check if the `__setattr__` function is present
                else:
                    for attr_k, attr_v in value.items():
                        attr[attr_k] = attr_v
            elif isinstance(value, list):
                if hasattr(attr, 'append'):
                    for v in value:
                        attr.append(v)
            else:
                setattr(cls, key, value)

    @classmethod
    def initCLI(cls):
        """This allows for an application to have an initial CLI flow for
        standard arguments.
        """

        from gmutils.helpers.helpme_printing import Printing
        err = None

        cls.arguments._results = cls.arguments.parse_args()

        try:
            if cls.arguments.get('version'):
                if hasattr(modules.get('__main__'), '__version__'):
                    print('v' + modules.get('__main__').__version__)
                    exit(0)
            elif cls.arguments.get('config'):
                for config in cls.arguments.get('config'):
                    cls.loadFile(config)

        except (GMException, GMSecurity) as context:
            err = context

        if not Config.quite:
            Printing.banner()
        if err is not None:
            Printing.error('CLI', str(err), err)

    @classmethod
    def isTesting(cls):
        """This function is used to determine if the current enviroment is for
        testing or production.

        Returns:
            bool -- if the current system is in testing or prod
        """

        test_strings = [
            'TEST', 'TESTING', 'DEV', 'DEVELOPMENT'
        ]
        return True if cls.ENV.upper() in test_strings else False

    @classmethod
    def haltThreads(cls, name=None):
        """This function is used to stop all registered threads added to the
        `Config.THREADS` list. This will set the `Config.HALT` boolean to True
        which should make stop threads from executing if they are using the
        `helpme_thread` wrappers.

        Keyword Arguments:
            name {str} -- name of the group of threads that you want to
            shutdown (default: {None})
        """
        # TODO: add support for `name` halting functionality
        Config.HALT = True

        for thread in Config.THREADS:
            thread.join(timeout=5)

        Config.THREADS = []

    @classmethod
    def export(cls, path=None, export_object=None, depth=1):
        """This function allows for simple exporting funionality.

        Keyword Arguments:
            path {str} -- path for the output to be saved too (default: {None})
            export_object {object} -- arbatiry object (default: {Config})
            depth {int} -- the depth of the exporting (default: {1})

        Returns:
            dict -- returns a dictonary for exporting if path is not set
        """

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
            EXPORT_DATA = _export_recursively(cls)
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
            return EXPORT_DATA

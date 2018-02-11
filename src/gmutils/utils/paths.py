#!/usr/bin/env python

from os import makedirs, getcwd
from os.path import exists, join, abspath, dirname, isdir
from sys import modules
from mimetypes import MimeTypes

from gmutils.utils.exceptions import GMException, GMSecurity

import logging


class Paths:
    __PATHS__ = {}

    def __init__(self, **kargvs):
        """The Paths() class supplies Utils with an interface to set, get and
        other functionality to GMUtils.s
        """
        # Defaults:
        self.duplications = kargvs.get('duplications', False)
        self.security_checks = kargvs.get('security_checks', True)

        __project__ = modules['__main__']
        if hasattr(__project__, '__file__'):
            # Add standard project paths
            self.add(
                'cwd', getcwd(), directory=True
            )
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

        if kargvs.get('paths'):
            self.load(**kargvs.get('paths'))

    def load(self, **load_paths):
        """ The Path.load() function is used for loads all the projects predetermined
        path variables. Normally these are defined in the projects `config.json` file.

        "name": {
            "path": "/path/to/the/file.ext",
            "create": bool,
            "required": bool,
            "directory": bool
            "mime": "file/mime"
        }
        """
        for name, options in load_paths.items():
            for key, value in options.items():
                if key.startswith('_'):
                    continue
                options[key] = value

            if name != '':
                self.add(name, **options)

    def add(self, name, path, **kargvs):
        """ The add function allows developers to add paths for their project,
        allowing many options for the developer to use.

        :param name: The name of the resource
        :type name: type str

        :param path: The path or location to a resource
        :type path: type str 

        :param required: The `required` paramater allows the developer to make sure that the
        file/dir exists before using it. An example of this is to check if a
        config file exists, if it doesn't an exception will be raised.
        :type required: type boolean

        :param create: The `create` parameter will create the file for the user if the file doesn't exist already.
        :type create: type boolean

        :param directory: The `directory` flag is set when a developer wants to create/use the path as a directory.
        :type directory: type boolean

        :param mime: The `mime` paramater allows for the developer to quickly check the file type before its used.
        An example of this is if you are expecting a JSON file, using 'application/json' will make
        sure that the correct files are used without the developer having to write any more code.
        :type mime: type str
        """
        OPTIONS = {
            '_exists': False,
            'required': False,
            'create': False,
            'directory': False,
            'mime': ''
        }

        # Set options from kargvs
        for key, value in kargvs.items():
            if key.startswith('_') or OPTIONS.get(key) is None:
                raise GMException('Unknown key supplied: ' + str(key))
            if not isinstance(value, type(OPTIONS.get(key))):
                raise GMException(
                    'Value is of unknown type for `{}`: {} != {}'.format(
                        key, type(value), type(OPTIONS.get(key))
                    )
                )
            OPTIONS[key] = value

        # Options setters
        if not self.duplications and Paths.__PATHS__.get(name):
            raise GMException('The Path name already exist')

        if name.startswith('dir-') or name.startswith('dir_'):
            OPTIONS['directory'] = True

        if exists(path):
            OPTIONS['_exists'] = True
            if isdir(path):
                OPTIONS['directory'] = True

        # Log that the path is being overwritten
        if Paths.__PATHS__.get(name):
            logging.info("PATHS: overridding key `{}`".format(name))

        # Perform actions
        if OPTIONS['required']:
            if not exists(path):
                raise GMException('The path being added is required to exist')

        if OPTIONS['_exists'] and OPTIONS['mime'] != '':
            Paths.checkMime(path, OPTIONS['mime'])

        if OPTIONS['create'] and not OPTIONS['_exists']:
            Paths.create(path, is_directory=OPTIONS['directory'])

        # finally, add new path in the __PATHS__ dict
        OPTIONS['path'] = path
        Paths.__PATHS__[name] = OPTIONS

    def get(self, name):
        """ This function allows you to get a path/resource by name that has been registered

        :param name: The name that you can to get
        :type name: type str
        """
        if Paths.__PATHS__.get(name):
            return Paths.__PATHS__[name]['path']
        return None

    def getFull(self, name):
        """ This function will get all the details associated to a path.

        :param name: The name that you can to get
        :type name: type str
        """
        if Paths.__PATHS__.get(name):
            return Paths.__PATHS__[name]
        return None

    def remove(self, name):
        """ The remove function deletes a path by name
        :param name: Name of the path that you want to delete
        :type name: type str
        """
        if Paths.__PATHS__.get(name):
            Paths.__PATHS__.pop(name)
        else:
            raise GMException('Path does not exist; {}'.format(name))

    @staticmethod
    def create(file, is_directory=False):
        # if the file doesn't exist, create it
        if not is_directory:
            makedirs(file)
        else:
            with open(file, 'w') as tmp_file:
                tmp_file.write("")

    @staticmethod
    def join(root, *paths):
        return join(root, *paths)

    @staticmethod
    def checkMime(path, mime=None):
        """ Checking file mime """
        mime_type, _strict = MimeTypes().guess_type(path)

        if mime is not None:
            if mime != mime_type:
                raise GMSecurity(
                    'The file provided is not of the expected type: {} != {}'.format(
                        mime_type, mime
                    )
                )
        else:
            return mime_type
        return True

    def __dict__(self):
        return Paths.__PATHS__

#!/usr/bin/env python

from os import makedirs, getcwd
from os.path import exists, join, abspath, dirname, isdir, realpath
from sys import modules
from mimetypes import MimeTypes

from gmutils.utils.exceptions import GMException, GMSecurity

import logging


class Paths:
    __PATHS__ = {}

    def __init__(self, **kargvs):
        """The Paths() class supplies Utils with an interface to set, get and
        other functionality to GMUtils.

        Arguments:
            **kargvs {dict} -- options being set/loaded into Paths()
        """

        # Defaults:
        self.duplications = None
        self.security_checks = None

        self.load(**kargvs)

        self.defaults()

    def load(self, **kargvs):
        """The Path.load() function is used for loads all the projects
        predetermined path variables. Normally these are defined in the
        projects `config.json` file.

        Arguments:
            **kargvs {dict} -- options being loaded into Paths()
        """

        # Defaults:
        self.duplications = kargvs.get('duplications', False)
        self.security_checks = kargvs.get('security_checks', True)

        if kargvs.get('paths'):
            for name, options in kargvs.get('paths').items():
                for key, value in options.items():
                    if key.startswith('_'):
                        continue
                    options[key] = value

                if name != '':
                    self.add(name, **options)

    def add(self, name, path, **kargvs):
        """The add function allows developers to add paths for their project,
        allowing many options for the developer to use.

        Arguments:
            name {str} -- the name of the resource
            path {str} -- the path or location to a resource
            **kargvs {dict} -- the different path options

        Options (kargvs):
            required {bool} -- The `required` paramater allows the developer to
            make sure that the file/dir exists before using it. An example of
            this is to check if a config file exists, if it doesn't an
            exception will be thrown.

            create {bool} -- The `create` parameter will create the file for
            the user if the file doesn't exist already.

            directory {bool} -- The `directory` flag is set when a developer
            wants to create/use the path as a directory.

            mime {str} -- The `mime` paramater allows for the developer to
            quickly check the file type before its used. An example of this is
            if you are expecting a JSON file, using 'application/json' will
            make sure that the correct files are used without the developer
            having to write any more code.

        Raises:
            GMException -- if kargvs option key is unknown
            GMException -- if kargvs option value is of unknown type
            GMException -- if path name already exists
            GMException -- if kargvs.required is True but doesn't exist
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
            raise GMException('The Path name already exist: {}'.format(name))

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

        # A file is required to exist for the MIME check to be performed
        if OPTIONS['_exists'] and OPTIONS['mime'] != '':
            Paths.checkMime(path, OPTIONS['mime'])

        # Create it if the file/folder doesn't exists
        if not OPTIONS['_exists'] and OPTIONS['create']:
            Paths.create(path, is_directory=OPTIONS['directory'])

        # finally, add new path in the __PATHS__ dict
        OPTIONS['path'] = path
        Paths.__PATHS__[name] = OPTIONS

    def get(self, name, mime=None):
        """This function allows you to get a path/resource by name that has
        been registered

        Arguments:
            name {str} -- the name that you can to get

        Keyword Arguments:
            mime {str} -- the mime type that the file must be (default: {None})

        Returns:
            str -- path based off the name provided
        """

        if Paths.__PATHS__.get(name):
            path = Paths.__PATHS__[name]['path']
            if mime is not None:
                Paths.checkMime(path, mime)
            return path
        return None

    def getFull(self, name):
        """This function will get all the details associated to a path.

        Arguments:
            name {str} -- the name that you can to get

        Returns:
            dict -- return the full details of the path
        """

        if Paths.__PATHS__.get(name):
            return Paths.__PATHS__[name]
        return None

    def check(self, path, mime=None):
        """The check function allows you to provide a path and perform various
        checks. This will return if those checks were sucessful.

        Checks:
          - Does the path exist?
          - Does the provided mime type match?

        Arguments:
            path {str} -- path that the checked will be performed against

        Keyword Arguments:
            mime {str} -- the mime type that the file must be (default: {None})

        Returns:
            bool -- return the value
        """

        if not exists(path):
            return False

        # Check mime type
        try:
            self.checkMime(path, mime)
        except GMException as err:
            return False

        return True

    def clear(self):
        """ This function will reset/clear the current paths added in the
        Paths() class.
        """
        Paths.__PATHS__ = {}

    def remove(self, name):
        """The remove function deletes a path by name.

        Arguments:
            name {str} -- Name of the path that you want to delete

        Raises:
            GMException -- if the path does not exist
        """

        if Paths.__PATHS__.get(name):
            Paths.__PATHS__.pop(name)
        else:
            raise GMException('Path does not exist; {}'.format(name))

    @staticmethod
    def create(path, is_directory=False):
        """Create is a static function that will create files or directories
        on behalf other the programmer.

        Arguments:
            path {str} -- the path you want

        Keyword Arguments:
            is_directory {bool} -- is it a directory you want to create?
            (default: {False})
        """

        if is_directory:
            path = path if path.endswith('') else path.rstrip('/')
            makedirs(path, exist_ok=True)
        else:
            with open(path, 'w') as tmp_file:
                tmp_file.write("")

    def join(self, root, *paths):
        """The Paths.join() function is just a wrapper on-top of the standard
        os.path.join() function except it performs some security checks if
        Paths.security_checks is set to true.

        Arguments:
            root {str} -- the root directory
            *paths {str} -- list of paths to join

        Raises:
            GMSecurity -- when a security issue occurs

        Returns:
            str -- the full string of the concatinated paths
        """

        _path = join(root, *paths)

        # TODO: perform checks

        violation = False if realpath(_path) == _path else True
        if violation:
            logging.warning('Paths.join() security issues')
        if self.security_checks and violation:
            raise GMSecurity('Paths.join() possible path traversal detected')
        return _path

    @staticmethod
    def checkMime(path, mime=None):
        """This function allows a user to check if a path provided is the type
        that is expected using mime file types.

        Arguments:
            path {str} -- path that will be checked

        Keyword Arguments:
            mime {str} -- if a mime is provided, the check will be performed.
            if not mime type is provided, the mimetype is returned.
            (default: {None})

        Raises:
            GMSecurity -- if a mime is provided and the file does not match

        Returns:
            str,bool -- string of the mime from the file or True if sucessful
        """

        mime_type, _strict = MimeTypes().guess_type(path)

        if mime is not None:
            if mime != mime_type:
                raise GMSecurity(
                    'The file provided is not of the expected type: ' +
                    mime_type + ' != ' + mime
                )
        else:
            return mime_type
        return True

    def defaults(self):
        """Set multiple default paths

        Paths created:
        - cwd -- Current Working Directory
        - project -- The location where the project is stored
        - project-lib -- local project library directory
        - project-data -- local project data storage area
        - config-project -- local project config file stored
        """

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
                'project-libs', join(self.get('project'), 'libs'),
                directory=True
            )
            self.add(
                'project-data', join(self.get('project'), 'data'),
                directory=True
            )

            self.add(
                'config-project',
                join(self.get('project-data'), 'config.json'),
                mime='application/json'
            )

    def __export__(self):
        """When the object is exported, this is the returned values not the
        whole object. This is used with the `Paths.load()` function to load
        the options back into the class.

        Returns:
            dict -- exported dictorary
        """

        exp = {
            'duplications': self.duplications,
            'security_checks': self.security_checks,
            'paths': Paths.__PATHS__
        }
        return exp

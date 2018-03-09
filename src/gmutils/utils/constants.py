#!/usr/bin/env python
from logging import getLogger

from gmutils.utils.get import get as _get

logger = getLogger(__name__)


class Constants:
    __CONSTS__ = {}

    def load(self, **kargvs):
        """The load function allows a developer to loads constants

        Arguments:
            kargvs {dict} -- dict of constants
        """
        for new_key, new_value in kargvs.items():
            self.add(new_key, new_value)

    def add(self, key, value):
        """Add a constant with a key and value

        Arguments:
            key {str} -- string of the constant that will be added
            value {object} -- value
        """
        if Constants.__CONSTS__.get(key):
            logger.warning('Overwriting key: ' + key)

        Constants.__CONSTS__[key] = value

    def get(self, query, default=None):
        """Query for keys using a query
        
        Arguments:
            query {str} -- query string
            default {object} -- arbitrary object (default: {None})

        Returns:
            object -- returns the arbitrary value found at the end of the
            query, or the default varable
        """
        return _get(Constants.__CONSTS__, query, default=default)

    def clear(self):
        """Resets all the current constants
        """
        Constants.__CONSTS__ = {}

    def __export__(self):
        """Allows for Constants to be exported

        Returns:
            dict -- returns constants in __CONSTS__ dict
        """
        return Constants.__CONSTS__

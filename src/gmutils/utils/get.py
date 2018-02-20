#!/usr/bin/env python

from gmutils.utils.exceptions import GMException


def _query_extracter(query):
    """ This function will return an array of query blocks
    """
    if not isinstance(query, str):
        raise GMException('gmutils.get() query needs to be a string')
    ret_vals = query.split('.')
    return ret_vals if isinstance(ret_vals, list) else [ret_vals]


def _query(query_blocks, dict_object):
    """
    """

    if not isinstance(dict_object, (dict, list)):
        raise GMException('gmutils.get() myobject needs to be of type dict or list')

    def _recursive_query(current_block, remaining_blocks, current_object):
        if current_block == '':
            return current_block
        # Is end of the block chain?
        end = True if len(remaining_blocks) == 0 else False

        # Dict support
        if isinstance(current_object, dict):
            if not end and current_object.get(current_block):
                new_block = remaining_blocks.pop(0)
                return _recursive_query(
                    new_block, remaining_blocks, current_object.get(current_block)
                )
            elif current_object.get(current_block):
                return current_object.get(current_block)

        # TODO: Add better list support
        elif isinstance(current_object, list):
            return current_object
        else:
            return current_object

    return _recursive_query(query_blocks.pop(0), query_blocks, dict_object)


def get(myobject, query, default=None):
    """ This function allows you to query a dict object to get the value
    recursively through dicts and array's, returning the value found at the
    end of the query chain.

    If no value is found, return the `default` object if it's set.

    :param myobject: dictionary or array of objects
    :type myobject: type dict OR type list

    :param query: query string
    :type query: str

    :param default: default return value if query returns None
    :type default: type object
    """
    query_blocks = _query_extracter(query)

    ret_object = _query(query_blocks, myobject)

    # Return `object`, `None` or the default
    if ret_object is None:
        if default is not None:
            return default
        return ret_object
    return ret_object

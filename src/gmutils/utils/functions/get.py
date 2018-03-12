#!/usr/bin/env python

from gmutils.utils.exceptions import GMException


def _query_extracter(query):
    """This function extracts the different attributes of a query.

    Arguments:
        query {str} -- the query you want to split up

    Raises:
        GMException -- if the provided type isn't a string

    Returns:
        list[str] -- list of query blocks
    """
    if not isinstance(query, str):
        raise GMException('gmutils.get() query needs to be a string')

    ret_vals = query.split('.')
    return ret_vals if isinstance(ret_vals, list) else [ret_vals]


def _query(query_blocks, dict_object):
    """this function recursivly queries down objects until completed

    Arguments:
        query_blocks {list[str]} -- list of query blocks
        dict_object {object} -- arbitrary object

    Raises:
        GMException -- when the dict_object isn't a supported type

    Returns:
        object -- returns the arbitrary value found at the end of the query, or
        None/null
    """
    if not isinstance(dict_object, (dict, list)):
        raise GMException(
            'gmutils.get() myobject needs to be of type dict or list'
        )

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
                    new_block, remaining_blocks, current_object.get(
                        current_block
                    )
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
    """This function allows you to query a dict object to get the value
    recursively through dicts and array's, returning the value found at the
    end of the query chain.

    Arguments:
        myobject {object} -- dictionary or array of objects
        query {str} -- query string

    Keyword Arguments:
        default {object} -- the default return type  (default: {None})

    Returns:
        [type] -- return value if query does not return None or returned
        default object
    """
    query_blocks = _query_extracter(query)

    ret_object = _query(query_blocks, myobject)

    # Return `object`, `None` or the default
    if ret_object is None:
        if default is not None:
            return default
        return ret_object
    return ret_object

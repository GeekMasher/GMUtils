#!/usr/bin/env python

import sys
import platform
import traceback
import logging

from gmutils import Config

logger = logging.getLogger(__name__)


class Printing:

    @staticmethod
    def colour(colour, text, out=0):
        """Printing in colour the the text provided

        Arguments:
            colour {str} -- colour by name
            text {str} -- text

        Keyword Arguments:
            out {int} -- std out/err (default: {0})
        """

        colours = {
            'green': '\x1b[0;32;48m',
            'red': '\x1b[0;31;48m',
            'blue': '\x1b[0;34;48m'
        }

        if 'Windows' in platform.platform():
            colour = None

        if colour in colours:
            if out == 0:
                sys.stdout.write(colours[colour] + text + '\x1b[0m\n')
            elif out == 1:
                sys.stderr.write(colours[colour] + text + '\x1b[0m\n')
        else:
            # TODO: add random colour support
            # if colour == 'random':
            #     k = colours.values()[randint(0, len(colours)-1)]
            #     stdout.write(k + text + '\x1b[0m')
            # else:
            if out == 0:
                sys.stdout.write(text + '\n')
            elif out == 1:
                sys.stderr.write(text)
        if out == 0:
            sys.stdout.flush()
        elif out == 1:
            sys.stderr.flush()

    @staticmethod
    def banner():
        """ Printing banner
        """

        if not Config.quite:
            lib = sys.modules.get('__main__')
            if hasattr(lib, "__banner_detailed__"):
                Printing.colour('green', lib.__banner_detailed__)
            # elif :
                # TODO: Add detailed banner support from
                # `__banner__, __version__, __description__`
            elif hasattr(lib, "__banner__"):
                Printing.colour('green', lib.__banner__)

    @staticmethod
    def blank():
        """Enters a blank line in the std out
        """

        if not Config.quite:
            sys.stdout.write('\n')

    @staticmethod
    def format(type, code, text):
        """The formatting

        Arguments:
            type {str} -- info/debug/error codes
            code {str} -- simple message/code
            text {str} -- text for formatting
        """

        types = {
            'info': '+++',
            'data': '```',
            'warning': '---',
            'error': '***'
        }

        if type in types:
            if type == 'data':
                return '[{}] {}\n{}\n[{}]'.format(
                    types[type], code, text, types[type]
                )
            else:
                return '[{}] {:<10} - {}'.format(types[type], code, text)
        else:
            return '[{}] {:<10} - {}'.format('...', code, text)

    @staticmethod
    def info(code, text):
        """Printing infomation

        Arguments:
            code {str} -- simple message
            text {str} -- text
        """

        s = Printing.format('info', code, text)

        if not Config.quite:
            Printing.colour('green', s)

        logger.info(s)

    @staticmethod
    def data(title, text):
        """Printing of data

        Arguments:
            title {str} -- title of the data
            text {str} -- data to be printed
        """

        s = Printing.format('data', title, text)

        if not Config.quite:
            Printing.colour('blue', s)

    @staticmethod
    def error(code, text, exp=None):
        """Printing Errors

        Arguments:
            code {str} -- error code message
            text {str} -- error message

        Keyword Arguments:
            exp {Excecption} -- exception thrown by an applciation
            (default: {None})
        """

        s = Printing.format('error', code, text+'\n')

        if not Config.quite:
            Printing.colour('red', s, 1)

        logger.error(s)

        if exp:
            logger.warning('Printing.error() with exception is not implemented')

            # exc_type, exc_value, exc_tb = sys.exc_info()
            # tbe = traceback.TracebackException(
            #     exc_type, exc_value, exc_tb,
            # )
            # if not Config.quite:
            #     Printing.colour('red', tbe, 1)
            # logger.error(tbe)

#!/usr/bin/env python

import sys
import traceback
import logging

logger = logging.getLogger(__name__)


class Printing:

    @staticmethod
    def colour(colour, text, out=0):
        colours = {
            'green': '\x1b[0;32;48m',
            'red': '\x1b[0;31;48m',
            'blue': '\x1b[0;34;48m'
        }

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
        
        from gmutils.config import Config

        if not Config.quite:
            lib = __import__(__name__)
            if hasattr(lib, "__banner_detailed__"):
                Printing.colour('green', lib.__banner_detailed__)
            elif hasattr(lib, "__banner__"):
                Printing.colour('green', lib.__banner__)

    @staticmethod
    def blank():
        
        from gmutils.config import Config

        if not Config.quite:
            sys.stdout.write('\n')

    @staticmethod
    def format(type, code, text):
        types = {
            'info': '+++',
            'data': '```',
            'warning': '---',
            'error': '***'
        }

        if type in types:
            if type == 'data':
                return '[{}] {}\n{}\n[{}]'.format(types[type], code, text, types[type])
            else:
                return '[{}] {:<10} - {}'.format(types[type], code, text)
        else:
            return '[{}] {:<10} - {}'.format('...', code, text)

    @staticmethod
    def info(code, text):
        s = Printing.format('info', code, text)

        from gmutils.config import Config

        if not Config.quite:
            Printing.colour('green', s)

        logger.info(s)

    @staticmethod
    def data(title, text):
        s = Printing.format('data', title, text)

        from gmutils.config import Config

        if not Config.quite:
            Printing.colour('blue', s)

    @staticmethod
    def error(code, text, exp=False):
        s = Printing.format('error', code, text)

        from gmutils.config import Config

        if not Config.quite:
            Printing.colour('red', s, 1)

        logger.error(s)

        if exp:
            exc_type, exc_value, exc_tb = sys.exc_info()
            tbe = traceback.TracebackException(
                exc_type, exc_value, exc_tb,
            )
            if not Config.quite:
                Printing.colour('red', tbe, 1)
            logger.error(tbe)


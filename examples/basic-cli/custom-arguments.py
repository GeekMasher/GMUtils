#!/usr/bin/env python3

from gmutils import Config

# Init project variables
__version__ = '0.1.0'
__name__ = 'MyCustomArguments'

__description__ = 'My Custom Arguments CLI'


# Adding arguments is the same as using the standard `argparse` module
Config.arguments.add_argument(
    '-m', '--my-argument', action='store_true'
)


# Run the GMUtils simple init cli function
Config.initCLI()

# If the argument has been set or returns a value
if Config.arguments.get('my_argument'):
    print('Running my custom function...')

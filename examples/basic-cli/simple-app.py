#!/usr/bin/env python3

from gmutils import Config

# Init project variables
__version__ = '0.1.0'
__name__ = 'MySimpleProject'

__description__ = 'My Simple CLI tool'

__banner__ = """\
 _____                          _       ______
|  ___|                        | |      | ___ \\
| |____  ____ _ _ __ ___  _ __ | | ___  | |_/ / __ _ _ __  _ __   ___ _ __
|  __\ \/ / _` | '_ ` _ \| '_ \| |/ _ \ | ___ \/ _` | '_ \| '_ \ / _ \ '__|
| |___>  < (_| | | | | | | |_) | |  __/ | |_/ / (_| | | | | | | |  __/ |
\____/_/\_\__,_|_| |_| |_| .__/|_|\___| \____/ \__,_|_| |_|_| |_|\___|_|
                         | |
                         |_|\
"""

# Many standard arguments will be added by the gmutils module such as
# `-c` or `--config` to set the locaitons of multiple configuration files
# `-q` or `--quiet` to set if the application can print of the console
# `-vvv` or `--verbose` to set the application verbosity level
# `-v` or `--version` to display the softwares version and exit the program
# `--help` to display the help options

# Run the GMUtils simple init cli function
Config.initCLI()

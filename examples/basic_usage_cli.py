
from os.path import join
from time import sleep

from gmutils import Config
from gmutils.helpers.helpme_argument import Arguments

# Init project variables
__version__ = '0.1.0'
__name__ = 'MyExampleProject'

__description__ = 'My Example CLI'

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

# Run the GMUtils simple init cli function
Config.initCLI()

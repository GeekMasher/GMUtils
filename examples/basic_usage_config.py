#!/usr/bin/env python

# You can import the Config like this:
from gmutils import Config

# Loading configuration files is simple, using the loadFile function
Config.loadFile('config-examples/config.testing.json')

# You can then load other files on top of the first config
Config.loadFile('config-examples/config.dev.json')

# But this will over write any original settings the first file added/edited


# You can quickly query if you are in production or testing
testing = Config.isTesting()
print('Am I in testing? ' + str(testing))

# For the threading functionality in the Config such as:
# - THREADS = []
# - haltThreads()

# Please take a look at 'basic_usage_thread.py'

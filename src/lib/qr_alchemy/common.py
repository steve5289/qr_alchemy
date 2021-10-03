### Common Lib
# Includes commonly used functions that are really generic

import os

def get_homedir():
    if "HOME" in  os.environ:
        return os.environ['HOME']
    else:
        return os.environ['/']


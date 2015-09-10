'''
Created on 14.05.2015

@author: linux
'''

import os
import pytest
import sys


if __name__ == "__main__":
    testdir = os.path.dirname(os.path.abspath(__file__))
    srcdir = os.path.abspath(os.path.join(testdir, '..', 'src'))

    # Append source directory to search path
    sys.path.append(srcdir)

    # Execute pytest
    args = [ testdir ]
    sys.exit(pytest.main(args))

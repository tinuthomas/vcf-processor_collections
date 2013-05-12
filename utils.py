#!/usr/bin/env python 
"""
Common utility function class 
"""

import os 
import re
import sys 
import gzip 
import bz2

def return_file_handle(fname):
    """
    function open the file and returns the handler 
    """
    try:
        if os.path.splitext(fname)[1] == ".gz":
            FH = gzip.open(fname, 'rb')
        elif os.path.splitext(fname)[1] == ".bz2":
            FH = bz2.BZ2File(fname, 'rb')
        else:
            FH = open(fname, 'rU')
    except Exception as error:
        sys.exit(error)
    return FH


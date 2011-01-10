#!/usr/bin/env python
"""
hbasta._cmd

Various commands / console entry points.
"""

import os
import sys
from optparse import OptionParser

from hbasta import HBasta, InterpolatedOptionParser

# Default locations for our configuration rc files
RCFILES = [os.path.join(os.environ['HOME'], '.hbastarc'), '/etc/hbastarc']

def prefix_scan():
    parser = InterpolatedOptionParser(profile='prefix_scan', rcfiles=RCFILES)
    parser.add_option("-H", "--host", dest="host", help="HBase host")
    parser.add_option("-P", "--port", dest="port", type=int, help="HBase port")
    parser.add_option("-t", "--table", dest="table", help="HBase table name")
    parser.add_option("-p", "--prefix", dest="table", help="HBase table name")

    options, args = parser.parse_args()
    print options.port
    


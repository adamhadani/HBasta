#!/usr/bin/env python
"""
hbasta._cmd

Various commands / console entry points.
"""

import os
import sys
import json
import logging
from optparse import OptionParser

from hbasta import HBasta, InterpolatedOptionParser

# Default locations for our configuration rc files
RCFILES = [os.path.join(os.environ['HOME'], '.hbastarc'), '/etc/hbastarc']

logging.basicConfig(
    level = logging.INFO,
    format = ""
)

def prefix_scan():
    parser = InterpolatedOptionParser(profile='prefix_scan', rcfiles=RCFILES)
    parser.add_option("-H", "--host", dest="host", help="HBase host")
    parser.add_option("-P", "--port", dest="port", type=int, help="HBase port")
    parser.add_option("-t", "--table", dest="table", help="HBase table name")
    parser.add_option("-n", "--num-rows", dest="num_rows", type=int, help="Number of rows to batch")
    parser.add_option("-p", "--prefix", dest="prefix", help="HBase table name")
    parser.add_option("-c", "--colspec", dest="colspec", action="append", help="Columns to fetch")
    parser.add_option("-f", "--format", dest="format", help="Output format ('csv'/'tsv'/'json')")

    options, args = parser.parse_args()
   
    client = HBasta(options.host, options.port)
    scanner_id = client.scanner_open_with_prefix(options.table, options.prefix, 
                    colspec=options.colspec)

    logging.info("* Scanner ID: %s", scanner_id)
    logging.info("* Fetched columns: %s", options.colspec)

    _sep_char = "\t" if options.format == 'tsv' else ","
    def  _print_func(row, columns):
        columns.update(row_key=row)
        return json.dumps(columns)

    if options.format == 'csv' or options.format == 'tsv':
        _print_func = lambda x, y: _sep_char.join([x]+y.values())

        # Print header
        print _sep_char.join(["row_key"]+options.colspec)


    try:
        rows = client.scanner_get_list(scanner_id, num_rows=options.num_rows)

        while rows:
            for row, columns in rows:
                print _print_func(row, columns)
            rows = client.scanner_get_list(scanner_id, num_rows=options.num_rows)
    finally:
        logging.info("Closing scanner %s", scanner_id)
        client.scanner_close(scanner_id)


#!/usr/bin/env python
"""
hbasta._api

API Wrapper for HBase Thrift Client
"""

import sys
import logging
 
from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
 
from hbase import Hbase
from hbase.ttypes import *

class HBasta(object):
    """HBase API entry point"""
    
    LOG = logging.getLogger("HBasta")

    def __init__(self, hostnport):
        """Initialize client.

        Params:
            hostnport - Tuple of (host, port) to connect to
        """
        self._hostnport = hostnport
        self._client = None

    @property
    def client(self):
        """Lazy load of the underlying client"""
        if not self._client:
            self.LOG.debug("* Connecting to HBase at: %s", self._hostnport)
            host, port = self._hostnport
            transport = TTransport.TBufferedTransport(TSocket.TSocket(host, port))
            protocol = TBinaryProtocol.TBinaryProtocol(transport)        
            self._client  = Hbase.Client(protocol)
            transport.open()
        return self._client

    def get_row(self, table, row, colspec=None):
        """Get single row of data, possibly filtered
        using the colspec construct

        Params:
            table - Table name
            key - Row key
            colspec - Specifier of which columns to return, in the form of list of column names
        """
        if not colspec:
            ret = self.client.getRow(table, row)
        else:
            ret = self.client.getRowWithColumns(table, row, colspec)
        return ret

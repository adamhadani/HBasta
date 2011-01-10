#!/usr/bin/env python
"""
OptionParser implementation with interpolation from rcfiles
"""

import os
import sys
from optparse import OptionParser
from ConfigParser import SafeConfigParser

class InterpolatedOptionParser(OptionParser):
    """OptionParser implementation that can interpolate
    option values from an rc file"""

    def __init__(self, profile, usage=None, rcfiles=None):
        OptionParser.__init__(self, usage=usage)
        self._rcfiles = rcfiles
        self._profile = profile

        self.interpolate()
    
    def interpolate(self):
        """Perform interpolation from rc file"""
        defaults = {}
        for rcfile in self._rcfiles:
            if os.path.exists(rcfile):
                config = SafeConfigParser()
                fnames = config.read(rcfile)
                if config.has_section(self._profile):
                    for key, val in config.items(self._profile):
                        defaults[key] = val

                break
                    
        self.set_defaults(**defaults)


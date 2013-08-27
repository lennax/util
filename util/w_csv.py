#!/usr/bin/env python
# Copyright 2013 Lenna X. Peterson. All rights reserved.

import csv
import logging

logging.basicConfig(level=logging.DEBUG)


class WCsv(object):

    def __init__(self, outfile, fieldnames):
        """CONSTRUCTOR"""

        self.outfile = open(outfile, "wb")
        self.writer = csv.DictWriter(self.outfile, fieldnames=fieldnames,
                                     lineterminator="\n")
        self.writer.writeheader()
        setattr(self, "writerow", self.writer.writerow)

    def __del__(self):
        """Close CSV file"""
        try:
            self.outfile.close()
        except AttributeError:
            pass

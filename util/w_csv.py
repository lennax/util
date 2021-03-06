# Copyright 2013-2015 Lenna X. Peterson. All rights reserved.

import csv


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

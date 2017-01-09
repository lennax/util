#!/usr/bin/env python

from __future__ import division

import argparse
import glob
import inspect
import logging
import os

logging.basicConfig(level=logging.DEBUG)

script_dir = os.path.abspath(os.path.dirname(inspect.getfile(inspect.currentframe())))


class FixPdbError(RuntimeError):
    """Exception for class FixPdb"""
    def __init__(self, message):
        super(FixPdbError, self).__init__(message)


class FixPdb(object):

    def __init__(self, directory=None, input=None, pattern=None):
        """CONSTRUCTOR"""
        if pattern is None:
            pattern = "FILEPATTERN"
        filenames = list()
        if input is not None:
            if isinstance(input, str):
                filenames.append(input)
            else:
                filenames.extend(input)
        if directory is not None:
            filenames.extend(glob.glob(os.path.join(directory, pattern)))
        if not filenames:
            raise FixPdbError("No files were found")

    @classmethod
    def commandline(cls, module_args=None):
        desc = """HELPDESCRIPTION"""
        a = argparse.ArgumentParser(description=desc)
        a.add_argument("-i", "--input", nargs="*",
                       help="Input file(s)")
        a.add_argument("-d", "--directory",
                       help="Directory of input files")
        a.add_argument("-p", "--pattern",
                       help="File pattern in directory (default FILEPATTERN)")
        a.add_argument("-v", "--verbose", action="store_true",
                       help="Show debug statements")

        args = a.parse_args(module_args)
        kwargs = vars(args)

        level = logging.INFO
        if kwargs.pop("verbose"):
            level = logging.DEBUG
        logging.basicConfig(level=level)

        c = cls(**kwargs)
        return c


if __name__ == "__main__":
    FixPdb.commandline()

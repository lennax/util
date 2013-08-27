#!/usr/bin/env python

import argparse
import logging

logging.basicConfig(level=logging.DEBUG)


class Pdbre(object):

    def __init__(self):
        """CONSTRUCTOR"""

    @classmethod
    def commandline(cls, module_args=None):
        desc = """HELPDESCRIPTION"""
        a = argparse.ArgumentParser(description=desc)

        args = a.parse_args(module_args)
        c = cls(**vars(args))
        return c


if __name__ == "__main__":
    Pdbre.commandline()

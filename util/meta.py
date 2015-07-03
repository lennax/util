# Copyright 2013-2015 Lenna X. Peterson. All rights reserved.
"""
Metacode: code for writing other code.
"""

class classproperty(property):
    """
    classproperty decorator
    http://stackoverflow.com/a/7864317/1547619
    """
    def __get__(self, cls, owner):
        return classmethod(self.fget).__get__(None, owner)()

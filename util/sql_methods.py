# Copyright 2013-2015 Lenna X. Peterson. All rights reserved.

from contextlib import contextmanager

import apsw
import pandas as pd

@contextmanager
def ro_conn(dbfile):
    try:
        with apsw.Connection(dbfile, flags=apsw.SQLITE_OPEN_READONLY) as conn:
            yield conn
    except apsw.CantOpenError:
        print dbfile, "not found"
        raise

@contextmanager
def write_conn(dbfile):
    try:
        with apsw.Connection(dbfile, flags=apsw.SQLITE_OPEN_READWRITE) as conn:
            yield conn
    except apsw.CantOpenError:
        print dbfile, "not found"
        raise

@contextmanager
def new_conn(dbfile):
    with apsw.Connection(dbfile, flags=apsw.SQLITE_OPEN_CREATE | apsw.SQLITE_OPEN_READWRITE) as conn:
        yield conn

def db_to_pandas(select, dbf, **kwargs):
    """
    Open database and load select into pandas DataFrame.

    :param select: SQL select query
    :param dbf: database file
    :param kwargs: additional arguments to pandas.read_sql_query

    :returns: pandas.DataFrame
    """
    with ro_conn(dbf) as conn:
        return conn_to_pandas(select, conn, **kwargs)

def conn_to_pandas(select, conn, **kwargs):
    """
    Load the results of a select into a pandas DataFrame.

    :param select: SQL select query
    :type select: str
    :param conn: database connection
    :type conn: apsw.Connection
    :param kwargs: additional arguments to pandas.read_sql_query

    :returns: pandas.DataFrame
    """
    try:
        return pd.read_sql_query(select, conn, **kwargs)
    except apsw.ExecutionCompleteError:
        return pd.DataFrame()

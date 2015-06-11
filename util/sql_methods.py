from contextlib import contextmanager

import apsw
import pandas as pd


def create_insert_statement(tablename, columns):
    insert_str = "INSERT INTO {tablename} ({columns}) VALUES ({bindings})"
    return insert_str.format(tablename=tablename,
                             columns=", ".join(columns),
                             bindings=", ".join([":" + v for v in columns]))

@contextmanager
def ro_conn(dbfile):
    with apsw.Connection(dbfile, flags=apsw.SQLITE_OPEN_READONLY) as conn:
        yield conn

@contextmanager
def write_conn(dbfile):
    with apsw.Connection(dbfile, flags=apsw.SQLITE_OPEN_READWRITE) as conn:
        yield conn

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
        return apsw_to_pandas(select, conn, **kwargs)

def apsw_to_pandas(select, conn, **kwargs):
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

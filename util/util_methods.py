# Copyright 2013-2017 Lenna X. Peterson. All rights reserved.

import ConfigParser
import errno
import logging
import os
import re
import shutil
import StringIO
import subprocess
import time
import tempfile

logging.basicConfig(level=logging.DEBUG)


class CHDIR(object):
    def __init__(self, dirname):
        self.dirname = dirname

    def __enter__(self):
        self.old_dir = os.getcwd()
        os.chdir(self.dirname)

    def __exit__(self, exception_type, exception_value, traceback):
        os.chdir(self.old_dir)


class CopyToHost(object):
    temporary_base_dir = "/scratch"
    special_scratch = dict(
        miffy="/kihara-scratch7",
        alien="/alien-scratch",
    )

    def __init__(self, wd, base_dir=None):
        hostname = os.uname()[1]
        logging.info(hostname)
        if base_dir is None:
            base_dir = self.special_scratch.get(hostname, self.temporary_base_dir)
        self.tmpdir = os.path.normpath(tempfile.mkdtemp(dir=base_dir))
        self.wd = os.path.abspath(wd)
        self.new_wd = os.path.join(self.tmpdir, os.path.basename(self.wd))

    def push(self):
        # no need to rsync, dest does not exist
        shutil.copytree(self.wd, self.new_wd)

    def pull(self):
        self.sync(source=self.new_wd, dest=os.path.dirname(self.wd))

    @staticmethod
    def sync(source, dest):
        cmd = ["rsync", "-az", source, dest]
        logging.debug(" ".join(cmd))
        subprocess.check_call(cmd)

    def __enter__(self):
        os.chdir(self.new_wd)
        self.push()
        return self

    def __exit__(self, type, value, traceback):
        try:
            self.pull()
        finally:
            #logging.info("Removing temporary directory")
            shutil.rmtree(self.tmpdir)
            os.chdir(self.wd)


def create_insert_statement(tablename, columns):
    """
    Create insert statement.
    e.g. func("mytable", ["foo", "bar"])
    INSERT INTO mytable (foo, bar) VALUES (:foo, :bar)

    :param tablename: name of table to update
    :type tablename: str
    :param columns: columns to set
    :type columns: list
    """
    insert_str = "INSERT INTO {tablename} ({columns}) VALUES ({bindings})"
    return insert_str.format(tablename=tablename,
                             columns=", ".join(columns),
                             bindings=", ".join([":" + v for v in columns]))

def create_update_statement(tablename, columns, where):
    """
    Create update statement.
    e.g. func("mytable", ["foo", "bar"], ["id"])
    UPDATE mytable SET foo=:foo, bar=:bar WHERE id=:id

    :param tablename: name of table to update
    :type tablename: str
    :param columns: columns to set
    :type columns: list
    :param where: where columns to match
    :type where: list

    :returns: str
    """
    if isinstance(where, basestring):
        where = [where]
    if isinstance(columns, basestring):
        columns = [columns]
    update_fmt = "UPDATE {tablename} SET {values} WHERE {where}"
    update_stmt = update_fmt.format(tablename=tablename,
                                    values=", ".join(["{0}=:{0}".format(c) for c in columns]),
                                    where=" AND ".join(["{0}=:{0}".format(w) for w in where]))
    return update_stmt

def missing(*files):
    "Check whether files are missing or empty"
    return any(not os.path.isfile(f) or not os.path.getsize(f)
               for f in files)

def read_config(config_path):
    """
    Read in a config file optionally containing whitespace
    (normally fails)
    """
    config = ConfigParser.SafeConfigParser()
    # Strip whitespace from config
    # http://stackoverflow.com/a/12822143
    with open(config_path, "r") as ih:
        config_data = StringIO.StringIO("\n".join(line.strip() for line in ih))
    config.readfp(config_data)
    return config

def copy_file(src, dest):
    if os.path.isfile(dest): return
    shutil.copyfile(src, dest)

def mkdir_p(path):
    """
    Pythonic replacement for shell `mkdir -p`
    Creates multiple directories and ignores error caused by existing
    """
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise

def silent_remove(path):
    """
    Remove file, ignore if missing.
    """
    try:
        os.remove(path)
    except OSError as e:
        if e.errno != errno.ENOENT:
            raise

def bash_wrap(cmd, module=None):
    """
    Create a subshell to run a command.

    :param cmd: command to run
    :type cmd: str or list
    :param module: module to load before running
    :type module: str

    :returns: str
    """
    if not isinstance(cmd, basestring):
        cmd = subprocess.list2cmdline(cmd)
    if module is None:
        module_cmd = ""
    else:
        module_cmd = "module load {module}; ".format(module=module)
    kwargs = dict(cmd=cmd, module=module_cmd)
    full_cmd = '/bin/bash --noprofile -c "{module}{cmd}"'.format(**kwargs)
    return full_cmd

def file_suffix(fn, suffix):
    "Place suffix before dot of fn"
    fileparts = list(os.path.splitext(fn))
    fileparts.insert(1, suffix)
    return "".join(fileparts)

def wait_timeout(proc, limit):
    "Kill process if it takes longer than limit seconds"
    start = time.time()
    end = start + limit
    interval = min(limit / 100.0, 1.0)

    while True:
        result = proc.poll()
        if result is not None:
            return result
        if time.time() > end:
            proc.terminate()
            time.sleep(10)
            if proc.poll() is None:
                proc.kill()
            return "timeout"
        time.sleep(interval)

def available_cpu_count():
    """
    Number of available virtual or physical CPUs on this system, i.e.
    user/real as output by time(1) when called with an optimally scaling
    userspace-only program
    credit to http://stackoverflow.com/a/1006301
    """

    # cpuset
    # cpuset may restrict the number of *available* processors
    try:
        m = re.search(r'(?m)^Cpus_allowed:\s*(.*)$',
                      open('/proc/self/status').read())
        if m:
            res = bin(int(m.group(1).replace(',', ''), 16)).count('1')
            if res > 0:
                return res
    except IOError:
        pass

    # Python 2.6+
    try:
        import multiprocessing
        return multiprocessing.cpu_count()
    except (ImportError, NotImplementedError):
        pass

    # http://code.google.com/p/psutil/
    try:
        import psutil
        return psutil.cpu_count()   # psutil.NUM_CPUS on old versions
    except (ImportError, AttributeError):
        pass

def venn(left, right):
    """
    Return a 3-tuple of:
        the items unique to the left iterable,
        the shared items,
        the items unique to the right iterable
    """
    left = set(left)
    right = set(right)
    return left - right, left & right, right - left

_h_re = re.compile(r"[123 ]*H.*")

def strip_h(filename):
    """
    Strip hydrogens from PDBfile
    NB loads entire file into memory, use at your own risk
    """
    with open(filename, "r") as ih:
        ret = StringIO.StringIO("".join(r for r in ih
                                          if r[:4] != "ATOM"
                                          or not _h_re.match(r[12:16])))
    return ret

def head(iterable, n=10):
    """
    Print first n items of iterable
    """
    for i, v in enumerate(iterable):
        print v
        if i > n:
            break

def range_overlap(range1, range2):
    """
    Return True if ranges have any overlap, else False
    Return None if ranges are not sorted
    """
    x1, x2 = range1
    y1, y2 = range2
    if x2 < x1 or y2 < y1:
        return None
    return x1 < y2 and y1 < x2

def dict_slice(the_dict, desired_keys):
    """
    Pop and return a dict of the named keys from the dict
    NB original dict is modified in place
    the_dict: dict to slice
    desired_keys: keys to return
    """
    return {key: the_dict.pop(key) for key in desired_keys}

def fake_agg(g):
    """fix pandas pivot table handling of lists"""
    T = tuple(g)
    if len(T) > 1:
        return T
    else:
        return T[0]

def split_index(s, i):
    """Split a string `s` at the specified index `i`"""
    return s[:i], s[i:]

greek_cardinals = dict(
    mono=1, di=2, tri=3, tetra=4, penta=5,
    hexa=6, hepta=7, octa=8, nona=9, deca=10,
    dodeca=12,
)

def parse_mer(mer, suffix="meric"):
    """
    Convert Greek cardinal description of protein complex to integer
    e.g. MONOMERIC -> 1
    DIMERIC -> 2
    """
    mer = mer.strip().lower()
    suf_len = len(suffix)
    if mer[-suf_len:] == suffix:
        root = mer[:-suf_len]
    else:
        raise ValueError("must end in '%s'", suffix)
    number = greek_cardinals.get(root)
    if number is not None:
        return number
    else:
        if root.endswith("-"):
            try:
                number = int(root[:-1])
            except ValueError:
                pass
            else:
                return number
        raise ValueError("unable to parse '%s'", mer)

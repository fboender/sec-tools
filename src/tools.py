#!/usr/bin/env python

import os
import sys
import copy
import re
from mako import exceptions
from mako.template import Template
from mako.lookup import TemplateLookup


def file_grep(path, match):
    """
    Return the first line that contains 'match'
    """
    with open(path, 'r') as f:
        for line in f:
            if match in line:
                return line
    return False


def file_egrep(path, match):
    """
    Return the first line that matches regexp `match`.
    """
    r = re.compile(match)
    with open(path, 'r') as f:
        for line in f:
            if r.match(line):
                return line
    return False


def deepupdate(target, src):
    """Deep update target dict with src
    For each k,v in src: if k doesn't exist in target, it is deep copied from
    src to target. Otherwise, if v is a list, target[k] is extended with
    src[k]. If v is a set, target[k] is updated with v, If v is a dict,
    recursively deep-update it.

    Examples:
    >>> t = {'name': 'Ferry', 'hobbies': ['programming', 'sci-fi']}
    >>> deepupdate(t, {'hobbies': ['gaming']})
    >>> print t
    {'name': 'Ferry', 'hobbies': ['programming', 'sci-fi', 'gaming']}
    """
    for k, v in src.items():
        if type(v) == list:
            if k not in target:
                target[k] = copy.deepcopy(v)
            else:
                target[k].extend(v)
        elif type(v) == dict:
            if k not in target:
                target[k] = copy.deepcopy(v)
            else:
                deepupdate(target[k], v)
        elif type(v) == set:
            if k not in target:
                target[k] = v.copy()
            else:
                target[k].update(v.copy())
        else:
            target[k] = copy.copy(v)


def tpl_file(path, extra_tpl_dirs=None, **kwargs):
    if extra_tpl_dirs is None:
        tpl_dirs = []
    else:
        tpl_dirs = extra_tpl_dirs

    # Add directory in which the template resides to the lookup.
    tpl_file = os.path.basename(os.path.abspath(path))
    tpl_dir = os.path.dirname(os.path.abspath(path))
    tpl_dirs.append(tpl_dir)

    # Add any caller-specified dirs to the lookup
    if extra_tpl_dirs is not None:
        tpl_dirs.extend(extra_tpl_dirs)

    # Construct template lookup and render template.
    tpl_lookup = TemplateLookup(directories=tpl_dirs)
    try:
        tpl = tpl_lookup.get_template(tpl_file)
        return tpl.render(**kwargs)
    except exceptions.TopLevelLookupException:
        sys.stderr.write("Couldn't find template {}\n".format(path))
        sys.exit(1)
    except Exception:
        raise Exception(exceptions.text_error_template().render())


def tpl_str(string, **kwargs):
    try:
        tpl = Template(string)
        return tpl.render(**kwargs)
    except Exception:
        raise Exception(exceptions.text_error_template().render())


def normalize_conf(path, comment='#'):
    """
    Read a configuration file, remove all commented out lines, convert to
    lowercase and strip whitespacing.
    """
    with open(path, 'r') as f:
        return [
            line.strip().lower()
            for line in f.readlines()
            if not line.startswith(comment)
        ]


def plain_err(err):
    """
    Convert Exception message to plain text string
    """
    return "{} {}".format(str(type(err)).replace('<', '').replace('>', ''), str(err).replace('<', '').replace('>', ''))


def abs_real_path(path):
    """
    Return the absolute (relative to /) real (symlink resolved) full path to
    the given path. Note that it only resolves a symlink if `path` points to a
    symlink. Other symlinks are not resolved.
    """
    if os.path.islink(path):
        path = os.readlink(path)
    return os.path.abspath(path)


def abs_real_dir(path):
    """
    Return the absolute (relative to /) real (symlink resolved) directory part
    of the given path. Note that it only resolves a symlink if `path` points to
    a symlink. Other symlinks are not resolved.
    """
    path = abs_real_path(path)
    if not os.path.isdir(path):
        return os.path.dirname(path)
    else:
        return path

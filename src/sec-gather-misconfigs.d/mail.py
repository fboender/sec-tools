#!/usr/bin/env python

import os


def mail_spool_populated():
    result = Result(
        desc="No mail should arrive in /var/spool/mail",
        explanation="""
            Mail that arrives in /var/spool/mail is generally never read, and
            indicates missing mail forwarding settings for users. This can
            cause important (security) warnings to go unnoticed.
        """,
        severity=5,
        passed=True
    )

    spool_dir = '/var/spool/mail'
    if os.path.isdir(spool_dir):
        for fname in os.listdir(spool_dir):
            path = os.path.join(spool_dir, fname)
            st = os.stat(path)
            result.add_result("{} size is {}".format(path, st.st_size))
            if st.st_size > 0:
                result.passed(False)
    else:
        result.add_result("{} not found".format(spool_dir))

    return result


def root_forward():
    result = Result(
        desc="Root account should have a .forward file",
        explanation="""
            Any mail sent to the root account should be forwarded to a real
            email address, to prevent important messages from being lost.
        """,
        severity=4,
        passed=False
    )

    forward_path = os.path.expanduser("~root/.forward")
    try:
        with open(forward_path, 'r') as f:
            line = f.readline()
            if '@' in line:
                result.passed(True)
                result.add_result("Email address found in {}".format(forward_path))
            else:
                result.add_result("No email address found in {}".format(forward_path))
    except IOError as err:
        result.passed(False)
        result.add_result(str(err))

    return result

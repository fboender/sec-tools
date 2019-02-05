#!/usr/bin/env python

import os

import morestd

tmp_dirs = [
    '/tmp',
    '/var/tmp',
    '/run/lock/',
    '/var/crash/',
    '/var/hoopla',
]


def executable():
    result = Result(
        desc="Temp dirs that allow file execution",
        explanation="Attackers often use temp dirs to launch exploits by placing executable files in them. Temp dirs should be mounted non-executable.",
        severity=3,
        passed=True
    )

    for tmp_dir in tmp_dirs:
        path = os.path.join(tmp_dir, 'whatswrong_tmp_tst')
        try:
            with open(path, 'w') as f:
                f.write('#!/bin/sh\necho "test"')
            os.chmod(path, 0o755)
            res = morestd.shell.cmd(path, raise_err=False)
            if 'test' in res['stdout']:
                result.passed(False)
                result.add_result(tmp_dir)
        except IOError:
            pass
        if os.path.exists(path):
            os.unlink(path)

    return result


def separate_mount():
    result = Result(
        desc="Temp dirs not mounted on separate filesystem",
        explanation="Temporary directories with global write access should be mounted on a separate volume to prevent users from filling the filesystem and interfering with the normal operation of the system",
        severity=2,
        passed=True
    )

    for tmp_dir in tmp_dirs:
        if not os.path.isdir(tmp_dir):
            continue

        tmp_dir_found = False
        with open('/proc/mounts', 'r') as f:
            for line in f:
                if line.split()[1] == tmp_dir:
                    tmp_dir_found = True
        if not tmp_dir_found:
            result.passed(False)
            result.add_result(tmp_dir)

    return result

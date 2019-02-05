#!/usr/bin/env python

import pwd
import os
import stat


def _is_normal_user(user):
    """
    Check output of pwd.getpwall() entry to see if this is a normal user
    instead of a system user.
    """
    is_dir = os.path.isdir(user.pw_dir)
    is_normal_user = (user.pw_uid == 0 or user.pw_uid > 999)
    return (is_dir and is_normal_user)


def world_readable_homedirs():
    result = Result(
        desc="Non-system users whoms home dirs are world readable",
        explanation="World readable home dirs can cause information leaks.",
        severity=3,
        passed=True
    )
    users = pwd.getpwall()
    for user in users:
        if (_is_normal_user(user)):
            homedir_stat = os.stat(user.pw_dir)
            if homedir_stat.st_mode & stat.S_IROTH:
                result.passed(False)
                result.add_result("{} (homedir={})".format(user.pw_name, user.pw_dir))

    return result


def world_writable_homedirs():
    result = Result(
        desc="Non-system users whoms home dirs are world writable",
        explanation="""
            World writable dirs allow attackers to fool users into running
            arbirary commands.
        """,
        severity=5,
        passed=True
    )
    users = pwd.getpwall()
    for user in users:
        if (_is_normal_user(user)):
            homedir_stat = os.stat(user.pw_dir)
            if homedir_stat.st_mode & stat.S_IWOTH:
                result.passed(False)
                result.add_result("{} (homedir={})".format(user.pw_name, user.pw_dir))

    return result


def open_ssh_config_dirs():
    result = Result(
        desc="User .ssh config directories that are readable for others",
        explanation="""
            .ssh directories should only be readable for the user, or keys
            might be leaked.
        """,
        severity=5,
        passed=True
    )

    users = pwd.getpwall()
    for user in users:
        ssh_dir = os.path.join(user.pw_dir, '.ssh')
        if os.path.isdir(ssh_dir):
            ssh_dir_stat = os.stat(ssh_dir)
            if ssh_dir_stat.st_mode & stat.S_IRGRP or \
               ssh_dir_stat.st_mode & stat.S_IWGRP or \
               ssh_dir_stat.st_mode & stat.S_IROTH or \
               ssh_dir_stat.st_mode & stat.S_IWOTH:
                result.passed(False)
                result.add_result("{} (ssh_dir={})".format(user.pw_name, ssh_dir))

    return result


def incorrect_skel_permissions():
    result = Result(
        desc="/etc/skel permissions should be strict",
        explanation="""
            The /etc/skel dir is used as the basis for new unix accounts. Its
            permissions should be 0700 by default, which will be inherited by
            new user home dirs.
        """,
        severity=4,
        passed=True
    )

    skel_dir = '/etc/skel'
    if os.path.isdir(skel_dir):
        skel_dir_stat = os.stat(skel_dir)
        if skel_dir_stat.st_mode & stat.S_IRGRP or \
           skel_dir_stat.st_mode & stat.S_IWGRP or \
           skel_dir_stat.st_mode & stat.S_IROTH or \
           skel_dir_stat.st_mode & stat.S_IWOTH:
            result.passed(False)
            result.add_result("skel_dir={}".format(skel_dir))
    else:
        result.add_result("/etc/skel not found")

    return result

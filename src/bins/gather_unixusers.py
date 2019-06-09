import sys
import argparse
import json
import logging
import pwd
import grp

import binlink
import common


no_login_shells = [
    '/bin/false',
    '/bin/nologin',
    '/sbin/nologin',
    '/usr/sbin/nologin'
]


def get_user_groups(username):
    groups = []

    # Get primary group
    p = pwd.getpwnam(username)
    groupname = grp.getgrgid(p.pw_gid).gr_name
    groups.append(groupname)

    # Get supplimentary groups
    for gr in grp.getgrall():
        if username in gr.gr_mem:
            groups.append(gr.gr_name)
    return groups


def gather(login=False):
    results = {}
    for p in pwd.getpwall():
        if login and p.pw_shell in no_login_shells:
            continue
        username = p.pw_name
        results[username] = {
            "homedir": p.pw_dir,
            "shell": p.pw_shell,
            "groups": get_user_groups(username)
        }

    return results


@binlink.register("sec-gather-unixusers")
def cmdline(version):
    parser = argparse.ArgumentParser(description='Output unix users and their details')
    common.arg_add_defaults(parser, version=version, annotate=True)
    parser.add_argument('--login',
                        dest="login",
                        action='store_true',
                        default=False,
                        help="Only users that can log in")
    args = parser.parse_args()
    common.configure_logger(args.debug)

    results = gather(login=args.login)
    sys.stdout.write(json.dumps({"unixusers": results}, indent=4))

import sys
import json
import argparse
import logging
import pwd
import grp

import binlink
import common


html_tpl = """
<table>
    <tr>
        <th>Group</th>
        <th>Members</th>
    </tr>
    % for groupname in sorted(unixgroups.keys()):
        <%
        members = unixgroups[groupname]
        %>
        <tr>
            <td>${groupname}</td>
            <td>
                <ul>
                    % for username in members:
                        <li>${username}</li>
                    % endfor
                </ul>
            </td>
        </tr>
    % endfor
</table>
"""


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


def gather(not_empty=True):
    results = {}
    for gr in grp.getgrall():
        if not_empty and len(gr.gr_mem) == 0:
            continue
        results[gr.gr_name] = gr.gr_mem

    return results


@binlink.register("sec-gather-unixgroups")
def cmdline(version):
    parser = argparse.ArgumentParser(description='Gather unix users')
    common.arg_add_defaults(parser, version=version, annotate=True)
    parser.add_argument('--not-empty',
                        dest="not_empty",
                        action='store_true',
                        default=True,
                        help="Only groups that are not empty")
    args = parser.parse_args()
    common.configure_logger(args.debug)

    results = gather(not_empty=args.not_empty)

    sys.stdout.write(json.dumps({"unixgroups": results}, indent=4))

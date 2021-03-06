import sys
import argparse
import logging
import json
import copy

import binlink
import common
import morestd


mysql_user_default = {
    "from_hosts": [],
    "dbs": {},
    "rights_all_dbs": ""
}


def gather_connect():
    mysql_users = {}
    cmd = 'mysql -N -B -e "SELECT * FROM mysql.user"'
    hosts_out = morestd.shell.cmd(cmd)['stdout']
    for line in hosts_out.splitlines():
        fields = line.split("\t")
        if fields[0] == "%":
            hostname = "ANY"
        else:
            hostname = fields[0]
        username = fields[1]
        select_priv = fields[2]
        insert_priv = fields[3]
        update_priv = fields[4]
        delete_priv = fields[5]
        rights_all_dbs = []
        if select_priv == "Y":
            rights_all_dbs.append("Read")
        if 'Y' in (insert_priv, update_priv, delete_priv):
            rights_all_dbs.append("Write")

        mysql_user = mysql_users.setdefault(username, copy.deepcopy(mysql_user_default))
        mysql_user['from_hosts'].append(hostname)
        mysql_user["rights_all_dbs"] = "/".join(rights_all_dbs)
    return mysql_users


def gather_db_access():
    mysql_users = {}

    db_access = morestd.shell.cmd('mysql -N -B -e "SELECT * FROM mysql.db"')['stdout']
    for line in db_access.splitlines():
        fields = line.split("\t")
        db = fields[1]
        username = fields[2]
        select_priv = fields[3]
        insert_priv = fields[4]
        update_priv = fields[5]
        delete_priv = fields[6]

        rights = []
        if select_priv == "Y":
            rights.append("Read")
        if 'Y' in (insert_priv, update_priv, delete_priv):
            rights.append("Write")

        mysql_user = mysql_users.setdefault(username, copy.deepcopy(mysql_user_default))
        mysql_user['dbs'][db] = "/".join(rights)

    return mysql_users


def gather():
    mysql_users = gather_connect()
    db_access = gather_db_access()
    morestd.data.deepupdate(mysql_users, db_access)
    return mysql_users


@binlink.register("sec-gather-mysqlusers")
def cmdline(version):
    parser = argparse.ArgumentParser(description='Gather mysql users')
    common.arg_add_defaults(parser, version=version, annotate=False)
    parser.add_argument('--no-conn-error',
                        dest="no_conn_error",
                        action="store_true",
                        default=False,
                        help="If cannot connect to mysql, return empty response")
    args = parser.parse_args()
    common.configure_logger(args.debug)

    # Try MySQL connection
    if args.no_conn_error is True:
        cmd_status = morestd.shell.cmd('mysql -N -B -e "SELECT 1"', raise_err=False)
        if cmd_status['exitcode'] != 0:
            sys.exit(1)

    results = gather()
    sys.stdout.write(json.dumps({"mysqlusers": results}, indent=4))

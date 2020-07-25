import sys
import argparse
import json
import logging

import binlink
import common
import morestd
import stat


def on_find_error(fileinfo, err):
    return

def gather(root_dir):
    results = []
    for fileinfo in morestd.fs.find(root_dir,
                                    one_fs=False,
                                    depth=None,
                                    on_error=on_find_error):

        if fileinfo["type"] == "dir":
            logging.debug("Scanning '{}'".format(fileinfo["path"]))

        is_suid = fileinfo["mode"] & stat.S_ISUID == stat.S_ISUID
        is_world_writable = fileinfo["type"] not in ("file", "link", "char", "socket") and \
                            not fileinfo["path"].startswith("/proc/") and \
                            not "systemd-private-" in fileinfo["path"] and \
                            (fileinfo["mode"] & stat.S_IWOTH == stat.S_IWOTH)

        if is_suid or is_world_writable:
            fileinfo["trigger_modes"] = []

            if is_suid:
                fileinfo["trigger_modes"].append("setuid")
            if is_world_writable:
                fileinfo["trigger_modes"].append("world_writable")

            fileinfo["mode_hr"] = stat.filemode(fileinfo["mode"])
            results.append(fileinfo)
    return results


@binlink.register("sec-gather-perms")
def cmdline(version):
    parser = argparse.ArgumentParser(description='Output files and dirs with dangerous permissions')
    common.arg_add_defaults(parser, version=version, annotate=True)
    parser.add_argument('dir',
                        metavar='DIR',
                        type=str,
                        nargs='+',
                        help='Dir to scan')
    args = parser.parse_args()
    common.configure_logger(args.debug)

    results = []
    for dir in args.dir:
        results.extend(gather(dir))
    sys.stdout.write(json.dumps({"perms": results}, indent=4))

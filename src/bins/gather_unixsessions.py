import sys
import argparse
import json
import logging
import re

import binlink
import common
import morestd
import tools


last_line_re = re.compile(
    r"(?P<username>.*?)"
    r"\s+"
    r"(?P<tty>.*?)"
    r"\s+"
    r"(?P<remote_addr>.*?)"
    r"\s+"
    r"(?P<login_starttime>.*?)(   | - )"
    r"(?P<login_endtime>.*?)\s*($|\()"
    r"(?P<duration>.*?)(\)|$)"
    r".*"
)


def gather():
    last = morestd.shell.cmd("/usr/bin/last -F -w")

    results = []
    for line in last['stdout'].splitlines():
        match = last_line_re.match(line)
        if match:
            results.append(match.groupdict())
    return results


@binlink.register("sec-gather-unixsessions")
def cmdline(version):
    parser = argparse.ArgumentParser(description='Output unix login sessions')
    common.arg_add_defaults(parser, version=version, annotate=True)
    args = parser.parse_args()
    common.configure_logger(args.debug)

    results = gather()
    sys.stdout.write(json.dumps({"unixsessions": results}, indent=4))

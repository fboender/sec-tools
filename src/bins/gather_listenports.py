import sys
import argparse
import logging
import json
import socket
import struct
import pwd
import os

import binlink
import morestd
import tools
import common


def get_ipv4(proto):
    ports = {}

    # Read open ports and skip first (header) line.
    for port in morestd.net.net_open_ports():
        if port["proto"].startswith(proto):
            port["local_address"] = str(port["local_address"])
            port["remote_address"] = str(port["remote_address"])
            key = "{}_{}".format(port["proto"], port["local_port"])
            ports[key] = port

    return ports


def include_port(port, no_local=False, no_verified=False):
    """
    Return True if the port should be included in the output. False otherwise.
    """
    # Do not include tcp ports that are not listening. We always include UDP
    # ports, because there's no way to distinguish between listening ports.
    if port["proto"].startswith("tcp") and port['state'] != "LISTEN":
        return False

    # Do not include locally listening ports if requested
    if no_local is True and port["local_address"].startswith("127.0.0."):
        return False

    # Do not include ports that have been verified if no_verified is True
    if no_verified is True and port.get("verified", False) is True:
        return False

    return True


def gather(no_udp=False, no_local=False, no_verified=False, annotate=None):
    annotations = {}
    if annotate:
        annotations = json.load(open(annotate, 'r'))

    ports = {}
    ports.update(get_ipv4('tcp'))
    if no_udp is not True:
        ports.update(get_ipv4('udp'))

    results = {}
    for port_key, port in ports.items():
        if include_port(port, no_local, no_verified):
            results[port_key] = port

    return results


@binlink.register("sec-gather-listenports")
def cmdline(version):
    parser = argparse.ArgumentParser(description='Gather listening ports')
    common.arg_add_defaults(parser, version=version, annotate=True)
    parser.add_argument('--no-udp',
                        dest="no_udp",
                        action='store_true',
                        default=False,
                        help="No UDP ports")
    parser.add_argument('--no-local',
                        dest="no_local",
                        action='store_true',
                        default=False,
                        help="Don't include services listening locally (127.0.0.0/24)")
    parser.add_argument('--no-verified',
                        dest="no_verified",
                        action='store_true',
                        default=False,
                        help="Don't include verified port")
    args = parser.parse_args()
    common.configure_logger(args.debug)

    results = gather(no_udp=args.no_udp,
                     no_local=args.no_local,
                     no_verified=args.no_verified,
                     annotate=args.annotate)
    sys.stdout.write(json.dumps({"listenports": results}, indent=4))

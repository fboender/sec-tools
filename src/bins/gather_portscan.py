import os
import sys
import argparse
import logging
import subprocess
import json
import shutil
from xml.etree import ElementTree as etree

import binlink
import morestd
import common


# Port states to filter out
state_filter = ["closed", "filtered"]

# -Pn = No host discovery, just assume its online, even if it doesn't respond to ping.
# -T4 = Timing template 4 (0-5, higher is faster)
# -oX - = output to XML on stdout
nmap_opts = "-Pn -T4 -oX -"


def expand_range(s):
    """
    Expand a string with one or more ranges and expand the ranges into a set.
    """
    expanded = set()
    for _range in s.split(','):
        if ':' in _range:
            range_start, range_end = [int(x) for x in _range.split(':', 1)]
        else:
            range_start = range_end = int(_range)
        for i in range(range_start, range_end + 1):
            expanded.add(i)
    return expanded


def run_nmap(ip, ports=None, nmap_extra_opts=""):
    """
    Scan IP and return XML results in nmap format.

    `ip` is a string containing an IP or hostname, `ports` is a string
    containing the range of ports to scan in nmap commandline argument format
    (e.g. "U:53,111,137,T:21-25,80,139,8080,S:9")
    """
    # Build a list of command options
    cmd_opts = [
        "nmap",
        nmap_opts,
        nmap_extra_opts,
    ]
    if ports is not None:
        cmd_opts.extend(["-p", ports])
    cmd_opts.append(ip)

    # Execute command
    cmd = " ".join(cmd_opts)
    logging.info("Executing: {}".format(cmd))
    p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    if p.returncode > 0:
        raise Exception("'{}' return exitcode {}. Stderr: {}".format(cmd, p.returncode, stderr))
    else:
        return stdout


def xml_port_to_dict(node_port):
    """
    Convert a Nmap XML node definition to a dictionary.
    """
    port_state = {
        "protocol": node_port.attrib.get("protocol", "MISSING_PROTOCOL"),
        "port": int(node_port.attrib.get("portid", -1)),
        "state": node_port.find("state").attrib.get("state", "MISSING_STATE"),
        "reason": node_port.find("state").attrib.get("reason", "MISSING_REASON"),
        "service_name": "unknown",
    }

    service_name = node_port.find("service")
    if service_name is not None:
        port_state["service_name"] = service_name.attrib.get("name", "MISSING_NAME")

    return port_state


def scan_ip(ip, ports=None, nmap_extra_opts="", all=False, ports_exclude=None):
    """
    Scan an single or multiple IPs and return a dict of ports and their states.
    """
    hosts = {}

    res = run_nmap(ip, ports=ports, nmap_extra_opts=nmap_extra_opts)
    logging.debug("nmap XML output: {}".format(res))
    xml = etree.XML(res)
    node_root = xml
    node_hosts = node_root.findall("host")
    if node_hosts is not None:
        for node_host in node_hosts:
            addr = node_host.find("address").attrib["addr"]

            # Replace IP address with reverse DNS hostname if one was found by
            # nmap
            if node_host.find("hostnames") is not None and \
               node_host.find("hostnames").find("hostname") is not None:
                addr = node_host.find("hostnames").find("hostname").attrib.get("name", addr)

            # Parse and add port information to this host.
            hosts[addr] = {}
            node_ports = node_host.find("ports")
            for node_port in node_ports.findall("port"):
                port_state = xml_port_to_dict(node_port)
                if ports_exclude is not None and port_state["port"] in ports_exclude:
                    # Skip ports that the requested to exclude
                    continue
                if port_state["state"] in state_filter and all is not True:
                    # skip ports if the state isn't interesting to us, unless
                    # the user specified --all.
                    continue

                hosts[addr][str(port_state["port"])] = port_state
    return hosts


def verify_root():
    """
    Verify the user is root.
    """
    if os.getuid() != 0:
        sys.stderr.write("You're not root. Not all ports would be scanned by nmap. Exiting\n")
        sys.exit(2)


def gather(targets, annotate=None, ports=None, all=False, ports_exclude=None):
    annotations = {}
    if annotate:
        annotations = json.load(open(annotate, 'r'))

    results = {}
    for target in targets:
        result_hosts = scan_ip(target, ports=ports, all=all, ports_exclude=ports_exclude)
        results.update(result_hosts)

        if target in annotations:
            morestd.data.deepupdate(results[target], annotations[target])

    return results


@binlink.register("sec-gather-portscan")
def cmdline(version):
    parser = argparse.ArgumentParser(description='Scan for open ports on machine')
    common.arg_add_defaults(parser, version=version, annotate=True)
    parser.add_argument('--ports',
                        dest="ports",
                        type=str,
                        default=None,
                        help="Port range to scan (nmap format)")
    parser.add_argument('--all',
                        dest="all",
                        action='store_true',
                        default=False,
                        help="Report all ports, not just 'open' states.")
    parser.add_argument('--ports-exclude',
                        dest="ports_exclude",
                        type=str,
                        default=None,
                        help="Port range(s) to skip")
    parser.add_argument('targets',
                        metavar='target',
                        type=str,
                        nargs='+',
                        help='Target(s) to scan')
    args = parser.parse_args()
    common.configure_logger(args.debug)

    if args.targets is None:
        sys.stderr.write("Please specify one or more targets\n")
        sys.exit(1)
    if shutil.which("nmap") is None:
        sys.stderr.write("nmap not found. Please install it.\n")
        sys.exit(1)

    ports_exclude = None
    if args.ports_exclude is not None:
        ports_exclude = expand_range(args.ports_exclude)

    verify_root()

    results = gather(args.targets, args.annotate, args.ports, args.all, ports_exclude)
    sys.stdout.write(json.dumps({"portscan": results}, indent=4))

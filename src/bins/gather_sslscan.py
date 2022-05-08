import os
import sys
import argparse
import logging
import subprocess
import json
import re
import shutil
from xml.etree import ElementTree as etree

import binlink
import morestd
import common


# -Pn = No host discovery, just assume its online, even if it doesn't respond to ping.
# -oX - = output to XML on stdout
nmap_opts = "-Pn -oX - --script +ssl-enum-ciphers "

WEAK_CIPHER_REGEX = [
    ".*_CBC.*",
    ".*_SHA$",
]


def xml_targets(node_root):
    node_targets = node_root.findall("target")
    if node_targets is not None:
        for node_target in node_targets:
            yield node_target

def xml_hosts(node_root):
    node_hosts = node_root.findall("host")
    if node_hosts is not None:
        for node_host in node_hosts:
            yield node_host


def xml_host_ports(node_host):
    node_ports = node_host.find("ports")
    if node_ports is not None:
        for node_port in node_ports.findall("port"):
            yield node_port


def xml_port_protos(node_port):
    node_script = node_port.find("script")
    if node_script is not None:
        node_protos = node_script.findall("table")
        if node_protos is not None:
            for node_proto in node_protos:
                yield node_proto


def xml_proto(node_table):
    proto = {
        "protocol": node_table.attrib.get("key", "MISSING_PROTOCOL"),
        "ciphers": [],
        "warnings": [],
    }

    for table in node_table.findall("table"):
        table_key = table.attrib.get("key")
        if table_key == "warnings":
            for elem in table.findall("elem"):
                proto["warnings"].append(elem.text)
        elif table_key == "ciphers":
            for cipher_table in table.findall("table"):
                cipher = {}
                for elem in cipher_table.findall("elem"):
                    elem_key = elem.attrib.get("key")
                    elem_value = elem.text
                    cipher[elem_key] = elem_value
                proto["ciphers"].append(cipher)

    return proto


def post_process(results):
    """
    Post-process the results to fix outdated nmap's ssl-enum-ciphers outdated
    strenght rating and such.
    """
    for host, scan_results in results.items():
        for port, port_info in scan_results.items():
            for proto in port_info:
                for cipher in proto["ciphers"]:

                    # Downgrade TLSv1.1 and CBC ciphers to grade "B"
                    for weak_cipher_regex in WEAK_CIPHER_REGEX:
                        weak_proto = proto["protocol"].lower() == "tlsv1.1"
                        weak_cipher = re.match(weak_cipher_regex, cipher["name"])

                        if cipher["strength"] < "B" and (weak_proto or weak_cipher):
                            cipher["strength"] = "B"
    return results


def run_nmap(ip, port, nmap_extra_opts=""):
    """
    Scan <hostname|ip>:port and return XML results in nmap format.

    `ip` is a string containing an IP or hostname, `port` is a string
    containing the range of ports to scan in nmap commandline argument format
    (e.g. "U:53,111,137,T:21-25,80,139,8080,S:9")
    """
    # Build a list of command options
    cmd_opts = [
        "nmap",
        nmap_opts,
        nmap_extra_opts,
        "-p",
        str(port)
    ]
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


def scan_host(host, ports, nmap_extra_opts=""):
    """
    Scan a host or IP's ports for SSL / TLS protocols and ciphers. Returns a
    list of supported protocols, ciphers and security warnings about the
    ciphers per port
    """

    all_port_ssl_details = {}

    for port in ports:
        port_ssl_details = all_port_ssl_details.setdefault(port, [])

        # Run scan
        res = run_nmap(host, port, nmap_extra_opts=nmap_extra_opts)

        # Parse XML output
        logging.debug("nmap XML output: {}".format(res))
        xml = etree.XML(res)
        node_root = xml

        # Verify that nmap ran correctly
        for target in xml_targets(node_root):
            specification = target.attrib.get("specification")
            status = target.attrib.get("status")
            reason = target.attrib.get("reason")
            sys.stderr.write("{}: {} ({})\n".format(specification, status, reason))
            sys.exit(3)

        # Extract protocol and cipher details
        logging.debug("xml parse: host '{}'".format(host))
        for xml_host in xml_hosts(node_root):
            logging.debug("xml parse:   {} {}".format(xml_host.tag, xml_host.items()))
            for xml_port in xml_host_ports(xml_host):
                logging.debug("xml parse:     {} {}".format(xml_port.tag, xml_port.items()))
                proto_results = []
                for xml_port_proto in xml_port_protos(xml_port):
                    logging.debug("xml parse:       {} {}".format(xml_port_proto.tag, xml_port_proto.items()))
                    proto = xml_proto(xml_port_proto)
                    proto_results.append(proto)
                all_port_ssl_details[port] = proto_results

    return all_port_ssl_details


def gather(targets, ports, annotate=None):
    annotations = {}
    if annotate is not None:
        annotations = json.load(open(annotate, 'r'))

    results = {}
    for target in targets:
        result_host = scan_host(target, ports=ports)
        results[target] = result_host

        # FIXME: This is probably broken
        if target in annotations:
            morestd.data.deepupdate(results[target], annotations[target])

    return post_process(results)


@binlink.register("sec-gather-sslscan")
def cmdline(version):
    parser = argparse.ArgumentParser(description='Output SSL / TLS protocol and ciphers for ports')
    common.arg_add_defaults(parser, version=version, annotate=True)
    parser.add_argument('--ports',
                        dest="ports",
                        type=str,
                        default=[443],
                        help="Port(s) to scan in nmap format. Defaults to 443")
    parser.add_argument('targets',
                        metavar='target',
                        type=str,
                        nargs='+',
                        help='Target hosts to scan')
    args = parser.parse_args()
    common.configure_logger(args.debug)

    if args.targets is None:
        sys.stderr.write("Please specify one or more targets\n")
        sys.exit(1)
    if shutil.which("nmap") is None:
        sys.stderr.write("nmap not found. Please install it.\n")
        sys.exit(1)
    for target in args.targets:
        if target.lower().startswith("http"):
            sys.stderr.write("Please specify an IP or hostname, not http:// or https:// ({})\n".format(target))
            sys.exit(1)

    results = gather(args.targets, args.ports, args.annotate)
    sys.stdout.write(json.dumps({"sslscan": results}, indent=4))

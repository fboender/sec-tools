#!/usr/bin/env python

import socket
import tools
import urllib2


def hostname():
    result = Result(
        desc="Invalid (fully qualified) hostname",
        explanation="Invalid (fully qualified) hostnames cause a number of problems such as invalid mail handling.",
        severity=0,
        passed=True
    )

    hostname = socket.gethostname()
    fqdn = socket.getfqdn()

    if '.' in hostname:
        result.passed(False)
    if '.' not in fqdn:
        result.passed(False)

    result.add_result("hostname={}, fqdn={}".format(hostname, fqdn))

    return result


def resolve_hostname():
    result = Result(
        desc="(Fully Qualified) hostnames should resolve to a valid IP.",
        explanation="Hostnames that don't resolve to an IP can cause strange behaviour such as hanging sudo sessions, etc.",
        severity=0,
        passed=True
    )

    hostname = socket.gethostname()
    fqdn = socket.getfqdn()
    try:
        hostname_ip = socket.gethostbyname(hostname)
        result.add_result('{} resolves to {}'.format(hostname, hostname_ip))
    except socket.gaierror as err:
        result.passed(False)
        result.add_result("{} couldn't be resolved: {}".format(hostname, tools.plain_err(err)))

    try:
        fqdn_ip = socket.gethostbyname(fqdn)
        result.add_result('{} resolves to {}'.format(fqdn, fqdn_ip))
    except socket.gaierror as err:
        result.passed(False)
        result.add_result("{} couldn't be resolved: {}".format(fqdn, tools.plain_err(err)))

    return result


def reverse_lookup_ip():
    result = Result(
        desc="External IPs should resolve to fully qualified hostname",
        explanation="",
        severity=0,
        passed=True
    )

    fqdn = socket.getfqdn()
    external_ip = urllib2.urlopen("https://ident.me").read()
    reverse = socket.gethostbyaddr(external_ip)

    result.add_result("{} reverse resolves to {} (aliases: {}). We expected {}.".format(external_ip, reverse[0], reverse[1], fqdn))
    if reverse[0] != fqdn and fqdn not in reverse[1]:
        result.passed(False)

    return result

#!/usr/bin/env python

import socket
import tools
import urllib.request
import morestd


def _file_content_is(result, path, content):
    with open(path, 'r') as f:
        if f.read().strip() == content:
            result.passed(True)
            result.add_result("'{}' content is '{}'".format(path, content))
        else:
            result.passed(False)
            result.add_result("'{}' content is not '{}'".format(path, content))
    return result


def tcp_sycookies_disabled():
    result = Result(
        desc="TCP SYN cookies should be enabled",
        explanation="""
            TCP SYN cookie is a technique used to resist SYN flood attacks.
        """,
        severity=2,
        passed=False
    )

    return _file_content_is(result, '/proc/sys/net/ipv4/tcp_syncookies', '1')


def accept_source_route():
    result = Result(
        desc="Source Routing should not be allowed",
        explanation="""
            Source Routing is used to specify a path or route through the
            network from source to destination. This feature can be used by
            network people for diagnosing problems. However, if an intruder was
            able to send a source routed packet into the network, then he could
            intercept the replies and your server might not know that it's not
            communicating with a trusted server.
        """,
        severity=3,
        passed=False
    )

    return _file_content_is(result, '/proc/sys/net/ipv4/conf/all/accept_source_route', '0')


def icmp_ignore_broadcast():
    result = Result(
        desc="ICMP broadcasts should be ignored",
        explanation="""
            Machines should not reply to ICMP ping broadcast requests.
        """,
        severity=1,
        passed=False
    )

    return _file_content_is(result, '/proc/sys/net/ipv4/icmp_echo_ignore_broadcasts', '1')


def icmp_redirects():
    result = Result(
        desc="ICMP redirects should not be allowed",
        explanation="""
            ICMP redirects are used by routers to tell the server that there is
            a better path to other networks than the one chosen by the server.
            However, an intruder could potentially use ICMP redirect packets to
            alter the hosts's routing table by causing traffic to use a path
            you didn't intend.
        """,
        severity=3,
        passed=False
    )

    return _file_content_is(result, '/proc/sys/net/ipv4/conf/all/accept_redirects', '0')


def ip_spoofing_protection():
    result = Result(
        desc="IP spoofing protection should be enabled",
        explanation="""
            Reverse Path filtering (rp_filter) verifies that incoming packets
            are routable and drops those that are not (spoofed packets).
        """,
        severity=3,
        passed=False
    )

    return _file_content_is(result, '/proc/sys/net/ipv4/conf/all/rp_filter', '1')


def hostname():
    result = Result(
        desc="Invalid (fully qualified) hostname",
        explanation="""
            Invalid (fully qualified) hostnames cause a number of problems such
            as invalid mail handling, unexplainable timeouts, etc. See the man
            page for the "hostname" command on how to set the (fully qualified)
            domainname.
        """,
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
        explanation="""
            Hostnames that don't resolve to an IP can cause strange behaviour
            such as hanging sudo sessions, etc.
        """,
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


def caa_record():
    result = Result(
        desc="Fully qualified hostnames should have a CAA DNS record",
        explanation="""
            CAA DNS records indicate to certificate authorities whether they
            are authorized to issue digital certificates for a particular
            domain name.
        """,
        severity=3,
        passed=False
    )

    fqdn = socket.getfqdn()
    fqdn_parts = fqdn.split('.')
    for i in range(len(fqdn_parts)):
        dns_name = ".".join(fqdn_parts[i:])
        output = morestd.shell.cmd('dig +short @1.1.1.1 {} type257'.format(dns_name))['stdout'].strip()
        if output != "":
            result.passed(True)
            result.add_result("{} has CAA record '{}'".format(dns_name, output))
        else:
            result.add_result("No CAA record for '{}'".format(dns_name))

    return result


def reverse_lookup_ip():
    result = Result(
        desc="External IPs should resolve to fully qualified hostname",
        explanation="""
            IP addresses that do not reverse-resolve to the FQDN cause a number
            of problems such as invalid mail handling.
        """,
        severity=0,
        passed=True
    )

    fqdn = socket.getfqdn()
    external_ip = urllib.request.urlopen("https://ident.me").read()
    reverse = socket.gethostbyaddr(external_ip)

    result.add_result("{} reverse resolves to {} (aliases: {}). We expected {}.".format(external_ip, reverse[0], reverse[1], fqdn))
    if reverse[0] != fqdn and fqdn not in reverse[1]:
        result.passed(False)

    return result

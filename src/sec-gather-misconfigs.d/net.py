#!/usr/bin/env python

import socket

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
    if not '.' in fqdn:
        result.passed(False)

    result.add_result("hostname={}, fqdn={}".format(hostname, fqdn))

    return result

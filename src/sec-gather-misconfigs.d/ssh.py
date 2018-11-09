#!/usr/bin/env python

import re
import tools

sshd_config = "/etc/ssh/sshd_config"

def old_protocol(sshd_config=sshd_config):
    result = Result(
        desc="SSH server supports old protocol v1",
        explanation="SSH protocol v1 is unsafe.",
        severity=4,
        passed=True
    )

    for line in tools.normalize_conf(sshd_config):
        if "protocol" in line and "1" in line:
            result.passed(False)
            break

    return result

def whitelist(sshd_config=sshd_config):
    result = Result(
        desc="SSH server does not whitelist users or groups (AllowUsers or AllowGroups)",
        explanation="Which users are allowed to log in with SSH should be whitelisted to prevent temporary accounts and service users from logging in.",
        severity=3,
        passed=False
    )

    for line in tools.normalize_conf(sshd_config):
        if "allowusers" in line:
            result.passed(True)
            break
        elif "allowgroups" in line:
            result.passed(True)
            break

    return result

def permit_empty_passwords(sshd_config=sshd_config):
    result = Result(
        desc="SSH server allows empty passwords (PermitEmptyPasswords)",
        explanation="Allowing empty passwords for SSH logins is a security risk",
        severity=5,
        passed=True
    )

    for line in tools.normalize_conf(sshd_config):
        if "permitemptypasswords" in line and "yes" in line:
            result.passed(False)
            break

    return result

def permit_root_login(sshd_config=sshd_config):
    result = Result(
        desc="SSH server allows remote login as the root user (PermitRootLogin)",
        explanation="The root account has all the priviliges on a system. It should not be directly exposed to the outside world.",
        severity=5,
        passed=True
    )
    bad_values = ["yes", "prohibit-password", "without-password"]

    for line in tools.normalize_conf(sshd_config):
        if "permitrootlogin" in line:
            if any([value in line for value in bad_values]):
                result.passed(False)
                break

    return result

def permit_password_auth(sshd_config=sshd_config):
    result = Result(
        desc="SSH server allows password authentication (PasswordAuthentication)",
        explanation="Passwords are often weak and can be bruteforced. SSH logins should be done with public/private keys",
        severity=3,
        passed=False
    )

    for line in tools.normalize_conf(sshd_config):
        if "PasswordAuthentication" in line and "no" in line:
            result.passed(True)
            break

    return result

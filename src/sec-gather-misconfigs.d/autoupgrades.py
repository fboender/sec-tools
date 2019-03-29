import os

import morestd
import tools


def autosecurityupgrades():
    result = Result(
        desc="Automatic security upgrades should be configured",
        explanation="""
            Vendor-provided security upgrades for Debian, Ubuntu, CentOS and
            RedHat should be configured such that they are installed
            automatically.
        """,
        severity=5,
        passed=False
    )

    os_info = morestd.lsb.get_os()

    if os_info['family'] == 'debian':
        # Check that unattended-upgrades package is installed
        if os.path.exists("/usr/bin/unattended-upgrades"):
            result.add_result("/usr/bin/unattended-upgrades found.")
        else:
            result.passed(False)
            result.add_result("/usr/bin/unattended-upgrades not found.")
            return result

        # Check that unattended-upgrades are configured
        line = tools.file_grep('/etc/apt/apt.conf.d/50unattended-upgrades', '-security";')
        if line is not False and not line.strip().startswith('//'):
            result.passed(True)
            result.add_result('Unattended security upgrades properly configured')
            return result
        else:
            result.passed(False)
            result.add_result("Security repo not found in Allowed-Origins (/etc/apt/apt.conf.d/50unattended-upgrades).")

        # Fail
        return result
    elif os_info['family'] == 'redhat':
        out = morestd.shell.cmd('yum -q list installed yum-cron', raise_err=False)
        if out['exitcode'] == 0:
            result.passed(True)
            result.add_result("yum-cron package installed")
        else:
            result.add_result("yum-cron package not installed")
        return result
    else:
        raise Exception("Unsupported OS family '{}'".format(os_info['family']))

def autoreboot():
    result = Result(
        desc="Automatic reboots when security upgrades require it",
        explanation="""
            Systems should automatically reboot if possible after installing
            security upgrades that require it. E.g. the kernel.
        """,
        severity=3,
        passed=False
    )

    os_info = morestd.lsb.get_os()

    if os_info['family'] == 'debian':
        # Check that unattended-upgrades package is installed
        if os.path.exists("/usr/bin/unattended-upgrades"):
            result.add_result("/usr/bin/unattended-upgrades found.")
        else:
            result.passed(False)
            result.add_result("/usr/bin/unattended-upgrades not found.")
            return result

        # Check that unattended-upgrades are configured
        line = tools.file_grep('/etc/apt/apt.conf.d/50unattended-upgrades', 'Automatic-Reboot-Time')
        if line is not False and not line.strip().startswith('//'):
            result.passed(True)
            result.add_result('Auto reboot time properly configured')
            return result
        else:
            result.passed(False)
            result.add_result("Automatic-Reboot-Time not found / configred in /etc/apt/apt.conf.d/50unattended-upgrades.")

        # Fail
        return result
    elif os_info['family'] == 'redhat':
        raise NotImplementedError("Redhat / Centos doesn't have an official auto-reboot method")
    else:
        raise Exception("Unsupported OS family '{}'".format(os_info['family']))

def reboot_required():
    result = Result(
        desc="Whether the system requires a reboot",
        explanation="""
            For certain security upgrades to take effect, the system needs to
            be rebooted. It has not been rebooted yet.
        """,
        severity=5,
        passed=False
    )

    os_info = morestd.lsb.get_os()

    if os_info['family'] == 'debian':
        if os.path.exists("/var/run/reboot-required"):
            result.passed(False)
            result.add_result("/var/run/reboot-required found.")
        else:
            result.passed(True)
            result.add_result("/var/run/reboot-required not found.")
        return result
    elif os_info['family'] == 'redhat':
        raise NotImplementedError("Redhat / Centos can use yum-utils::needs-restarted, but it's exceptionally slow, so not implemented here.")
    else:
        raise Exception("Unsupported OS family '{}'".format(os_info['family']))

def uninstalled_security_upgrades():
    result = Result(
        desc="Whether there are uninstalled security upgrades",
        explanation="""
            If automatic security upgrades are not configured, there may be
            uninstalled security upgrades that need to installed. Even if
            automatic security upgrades are configured, some packages may be
            not be automatically installed due to requiring user interaction.
        """,
        severity=5,
        passed=False
    )

    os_info = morestd.lsb.get_os()

    if os_info['family'] == 'debian':
        # Preferred method, it's the same as shown in the MOTD
        if os.path.exists('/usr/lib/update-notifier/apt-check'):
            res = morestd.shell.cmd('/usr/lib/update-notifier/apt-check')
            if res['exitcode'] == 0:
                pkg_count = int(res['stderr'].strip().split(";")[1])

        # Fallback method
        if pkg_count is None:
            res = morestd.shell.cmd("apt-get upgrade --dry-run | grep \"^Inst\" | grep \"security\" | wc -l")
            pkg_count = int(res['stdout'].strip())

    elif os_info['family'] == 'redhat':
        res = morestd.shell.cmd("yum -q updateinfo list security | wc -l")
        if res['stderr'].lower() != "":
            raise NotImplementedError("Command 'yum -q updateinfo list security' returned: {}".format(res['stderr']))
        pkg_count = int(res['stdout'].strip())
    else:
        raise Exception("Unsupported OS family '{}'".format(os_info['family']))

    if pkg_count > 0:
        result.passed(False)
        result.add_result("{} uninstalled security upgrades found".format(pkg_count))
    else:
        result.passed(True)
        result.add_result("No uninstalled security upgrades found")

    return result

#def c_pkg_upgradable_sec():
#    """
#    The number of security packages that are upgradable.
#    """
#    pkg_count = None
#
#    if s_os['family'] == 'debian':
#        if os.path.exists('/usr/lib/update-notifier/apt-check'):
#            # Preferred method, it's the same as shown in the MOTD
#            res = t_cmd('/usr/lib/update-notifier/apt-check')
#            # output looks like: $ /usr/lib/update-notifier/apt-check > /dev/null
#            # 121;4
#            # Where 121 is the number of normal updates available and 4 is the security updates
#            if res['exitcode'] == 0:
#                pkg_count = int(res['stderr'].strip().split(";")[1])
#
#        # The above apt-check method can fail due to dbus misconfiguration.
#        # FIXME: This ignores held-back packages!
#        if pkg_count is None:
#            res = t_cmd("apt-get upgrade --dry-run | grep \"^Inst\" | grep \"security\" |  wc -l", raise_err=False)
#            pkg_count = int(res['stdout'].strip())
#    elif s_os['family'] == 'redhat':
#        res = t_cmd("yum -q updateinfo list security | wc -l")
#        if 'no such command' in res['stderr'].lower():
#            return None # Install yum-plugin-security
#        pkg_count = int(res['stdout'].strip())
#

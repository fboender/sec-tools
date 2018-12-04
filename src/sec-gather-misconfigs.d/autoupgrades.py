import os
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

    os_info = tools.get_os()

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
        print(line)
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
        out = tools.cmd('yum -q list installed yum-cron')
        if out['exitcode'] == 0:
            result.passed(True)
            result.add_result("yum-cron package installed")
        return result
    else:
        raise Exception("Unsupported OS family '{}'".format(os_info['family']))

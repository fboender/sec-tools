import os


def cron_allow():
    result = Result(
        desc="No cron.allow file present",
        explanation="""
            If no cron.allow file is present, every user can create cronjobs.
            Cron jobs are sometimes used as a vehicle for privilege escalations
            or to keep backdoors active.
        """,
        severity=4,
        passed=False
    )

    paths = [
        "/etc/cron.allow",
        "/etc/cron.d/cron.allow",
    ]
    for path in paths:
        if os.path.exists(path):
            result.passed(True)
            result.add_result("cron.allow found at {}".format(path))
            break

    return result


def mailto_set():
    result = Result(
        desc="No MAILTO present in crontab",
        explanation="""
            Crontabs should have a MAILTO setting so that mail from cronjobs is
            sent to a real email address. Cron output often contains important
            information about failing jobs that may have security implications.
        """,
        severity=4,
        passed=True
    )

    crontab_dirs = [
        '/var/spool/cron/crontabs/',
        '/var/spool/cron/',
    ]
    crontabs = [
        '/etc/crontab',
    ]

    # Find all user crontabs in crontab dirs (Debian / Redhat)
    for crontab_dir in crontab_dirs:
        if os.path.isdir(crontab_dir):
            for crontab in os.listdir(crontab_dir):
                path = os.path.join(crontab_dir, crontab)
                if os.path.isfile(path):
                    crontabs.append(path)

    # Scan crontabs for MAILTO
    for crontab in crontabs:
        with open(crontab, 'r') as f:
            contents = f.read()
            if 'MAILTO' not in contents:
                result.passed(False)
                result.add_result("MAILTO not found in crontab {}".format(crontab))
            else:
                result.add_result("MAILTO found in crontab {}".format(crontab))

    return result

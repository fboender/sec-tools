import os

def cron_allow():
    result = Result(
        desc="No cron.allow file present",
        explanation="If no cron.allow file is present, every user can create cronjobs. Cron jobs are sometimes used as a vehicle for privilege escalations or to keep backdoors active.",
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
        explanation="Crontabs should have a MAILTO setting so that mail from cronjobs is sent to a real email address.",
        severity=4,
        passed=True
    )

    crontabs = [
        '/etc/crontab',
    ]
    for crontab in os.listdir("/var/spool/cron/crontabs/"):
        crontabs.append(os.path.join("/var/spool/cron/crontabs/", crontab))

    for crontab in crontabs:
        with open(crontab, 'r') as f:
            contents = f.read()
            if 'MAILTO' not in contents:
                result.passed(False)
                result.add_result("MAILTO not found in crontab {}".format(crontab))
            else:
                result.add_result("MAILTO found in crontab {}".format(crontab))

    return result

import tools

def root_password():
    result = Result(
        desc="MySQL root account has no password",
        explanation="Without a password, anyone can connect to the database as the root user. (newer versions of MySQL are not affected, because they use a root-owned socket)",
        severity=5,
        passed=True
    )

    res = tools.cmd('mysql -u root -h 127.0.0.1 -e "exit" ', raise_err=False)
    if res['exitcode'] == 0:
        result.passed(False)

    return result

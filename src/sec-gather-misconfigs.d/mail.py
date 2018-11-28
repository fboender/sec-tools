#!/usr/bin/env python

import os
import tools


def mail_spool_populated():
    result = Result(
        desc="No mail should arrive in /var/spool/mail",
        explanation="Mail that arrives in /var/spool/mail is generally never read, and indicated missing mail forwarding settings for users.",
        severity=5,
        passed=True
    )

    spool_dir = '/var/spool/mail'
    if os.path.isdir(spool_dir):
        for fname in os.listdir(spool_dir):
            path = os.path.join(spool_dir, fname)
            st = os.stat(path)
            result.add_result("{} size is {}".format(path, st.st_size))
            if st.st_size > 0:
                result.passed(False)
    else:
        result.add_result("{} not found".format(spool_dir))

    return result

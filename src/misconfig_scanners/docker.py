import grp


def group_users():
    result = Result(
        desc="Users in the 'docker' group",
        explanation="""
            Due to security vulnerabilities in docker (which won't be fixed),
            putting users in the 'docker' group is the same as giving them root
            without requiring a password. No users should be present in the
            'docker' group, and docker operations should be performed through
            sudo instead.
        """,
        severity=5,
        passed=True
    )

    try:
        docker_group_members = grp.getgrnam('docker').gr_mem
        if len(docker_group_members) > 0:
            result.passed(False)
            result.add_result("The following users are a member of the 'docker' group: {}".format(docker_group_members))
        else:
            result.add_result("No users found in the 'docker' group")
    except KeyError:
        result.add_result("Group 'docker' doesn't exist")

    return result

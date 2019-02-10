% SEC-GATHER-MISCONFIGS(1)
% Ferry Boender
% Nov 2018

# NAME

sec-gather-misconfigs – Scan for security misconfigurations

# SYNOPSIS

 **sec-gather-misconfigs** [**-h**] [**--version**] [**--debug**] [**--skip-passed**] [**--config** *CONFIG*] [**--limit** *LIMITS*]


# DESCRIPTION

**sec-gather-misconfigs** scans the local system for common security (and
other) misconfigurations such as dangerous SSH configurations, insecure web
server configurations, permission problems, etc.

# OPTIONS

**-h**, **--help**
:   Display this help message and exit

**--version**
:   show program's version number and exit

**--debug**
:   Show debug info

**--skip-passed**
:   Do not include tests that passed

**--config** *CONFIG*
:   Configuration file for tests

**--limit** *LIMITS*
:   Limit which tests are executed

# PLUGINS

The scan consist of plugins, each which can run multiple tests. Some examples:

    tmp:executable
    tmp:searate_mounts
    webserver:content_security_policy_header
    webserver:version_in_header
    homedir_perms:world_readable_homedirs
    homedir_perms:incorrect_skel_permissions
    ssh:permit_empty_passwords
    ssh:old_protocol

Scans are Python files located in the *sec-gather-misconfigs.d* directory.
These files are automatically loaded and each function in the file is executed
as a test. Each test returns a *RESULT*, which is included in the output.

# RESULTS

Each test produces a result that includes information on the test and whether
it passed or failed.

**desc**
:   A short description of the what the test does.

**explanation**
:   A short explanation of why the test matters.

**passed**
:   Whether the test passed or failed.

**severity**
:   The severity of the misconfiguration and its impact on security. Rated on a scale from 0 to 5, where 0 is "informational" and 5 is "critical".

**results**
:   Additional information on the results of the test such as a list of files that were scanned.

# CONFIGURATION

Certain tests may require configuration by the user in order to be useful. For
example, the *webserver* tests are more helpful if a full list of URLs served
by the locally running web server is provided. We can pass a configuration
file with the **--config** option.

The configuration file should specify the plugin and specific test, and a
collection of key/value options to configure the test. The format is
semi-JSON, but you can use comments and trailing comma's are also fine. It
would look something like this for the *permit_root_login* and
*permit_empty_passwords* test of the *ssh* plugin:

    {
      "ssh": {
        # We have our own compiled version of OpenSSH server
        "permit_root_login": {
          "sshd_config": "/opt/patched_ssh/sshd_config"
        },
        "permit_empty_passwords": {
          "sshd_config": "/opt/patched_ssh/sshd_config"
        },
      }
    }

To apply a configuration option to all tests in a plugin, you can use the
`_all` option. For example, the above `ssh` configuration would be better
written as:

    {
      "ssh": {
        "_all": {
          "sshd_config": "/opt/patched_ssh/sshd_config"
        }
      }
    }
    
A fully annotated configuration file can be found in
*examples/sec-gather-misconfigs.conf*.

# LIMITS

You can limit which tests are executed with the **--limit** option. Multiple
values may be specified, separated by comma's. Wildcards ('\*') are permitted.
For example:

    # Run all 'net' tests, and the 'ssh:whitelist' test
    sec-gather-misconfigs --limit 'net:*,ssh:whitelist'

# EXAMPLES

The default output looks like the following. Note that most descriptions have
been cut short and many tests have been omitted to keep the example
comprehensible.

    $ sec-gather-misconfigs
    {
        "misconfigs": {
            "tmp": {
                "executable": {
                    "explanation": "Attackers often use temp dirs...", 
                    "desc": "Temp dirs that allow file execution", 
                    "results": [
                        "/tmp", 
                        "/var/tmp", 
                        "/var/crash/"
                    ], 
                    "passed": false, 
                    "severity": 3
                }, 
                "separate_mount": {
                    "explanation": "Prevent users from filling the filesystem...", 
                    "desc": "Temp dirs not mounted on separate filesystem", 
                    "results": [
                        "/tmp", 
                        "/var/tmp", 
                        "/run/lock/", 
                        "/var/crash/"
                    ], 
                    "passed": false, 
                    "severity": 2
                }
            }, 
            "webserver": {
                "version_in_header": {
                    "explanation": "...", 
                    "desc": "Web server exposes version in 'Server' header.", 
                    "results": [
                    ], 
                    "passed": true, 
                    "severity": 1
                }, 
            },
    }

# COPYRIGHT

Copyright 2017-2018, Ferry Boender.

Licensed under the MIT license. For more information, see the LICENSE file.

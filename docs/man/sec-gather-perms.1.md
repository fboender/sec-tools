% SEC-GATHER-PERMS(1)
% Ferry Boender
% Feb 2020

# NAME

sec-gather-perms – Output files and dirs with dangerous permissions

# SYNOPSIS

**sec-gather-perms** [**-h**] [**--version**] [**-d**] [**--annotate** *ANNOTATIONFILE*] [**--root** *ROOT*]

# DESCRIPTION

**sec-gather-perms** outputs files and dirs with dangerous permissions.
Currently that means files and directories that are world-writable or with the
setuid bit set.

# OPTIONS

**-h**, **--help**
:   Display this help message and exit

**--version**
:   show program's version number and exit

**-d** / **--debug**
:   Show debug info

**--annotate** *ANNOTATE*
:   annotation file

**--root** *ROOT*
:   Start from this dir


# EXAMPLES

Executing:

    $ sec-gather-perms --root /bin

The default output looks like this:

    {
        "perms": [
            {
                "filename": "ping",
                "dir": "/bin",
                "path": "/bin/ping",
                "type": "file",
                "size": 64424,
                "mode": 35309,
                "uid": 0,
                "gid": 0,
                "device": 64769,
                "trigger_modes": [
                    "setuid"
                ],
                "mode_hr": "-rwsr-xr-x"
            },
            {
                "filename": "mount",
                "dir": "/bin",
                "path": "/bin/mount",
                "type": "file",
                "size": 43088,
                "mode": 35309,
                "uid": 0,
                "gid": 0,
                "device": 64769,
                "trigger_modes": [
                    "setuid"
                ],
                "mode_hr": "-rwsr-xr-x"
            },
    ...

You can use the `reports/sec-gather-perms.tpl` report to generate a
HTML matrix overview of dirs / files and their permissions:

    $ sec-gather-perms | sec-report reports/sec-gather-perms.tpl > permissions.html

# COPYRIGHT

Copyright 2017-2019, Ferry Boender.

Licensed under the MIT license. For more information, see the LICENSE file.

% SEC-GATHER-UNIXUSERS(1)
% Ferry Boender
% May 2017

# NAME

sec-gather-unixusers – Output unix users and their details

# SYNOPSIS

 **sec-gather-unixusers** [**-h**] [**--version**] [**--debug**] [**--login**]

# DESCRIPTION

**sec-gather-unixusers** gathers information about unix user accounts from
`/etc/passwd` and their details (such as groups) and outputs it in JSON
format.

# OPTIONS

**-h**, **--help**
:   Display this help message and exit

**--version**
:   show program's version number and exit

**--debug**
:   Show debug info

**--login**
:   Only users that can log in

# EXAMPLES

    $ sec-gather-unixusers --login

    {
        "unixusers": {
            "root": {
                "shell": "/bin/bash", 
                "homedir": "/root", 
                "groups": [
                    "root"
                ]
            }, 
            "fboender": {
                "shell": "/bin/bash", 
                "homedir": "/home/fboender", 
                "groups": [
                    "fboender", 
                    "adm", 
                    "cdrom", 
                    "sudo", 
                    "dip", 
                    "plugdev", 
                    "lpadmin", 
                    "sambashare", 
                    "docker"
                ]
            }
        }
    }

# COPYRIGHT

Copyright 2017, Ferry Boender.

Licensed under the MIT license. For more information, see the LICENSE file.

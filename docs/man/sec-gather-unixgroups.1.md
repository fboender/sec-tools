% SEC-GATHER-UNIXGROUPS(1)
% Ferry Boender
% May 2017

# NAME

sec-gather-unixgroups – Output unix groups and their users

# SYNOPSIS

 **sec-gather-unixgroups** [**-h**] [**--version**] [**--debug**] [**--not-empty**]

# DESCRIPTION

**sec-gather-unixgroups** gathers information about unix groups from
`/etc/groups` and their users and outputs it in JSON format.

# OPTIONS

**-h**, **--help**
:   Display this help message and exit

**--version**
:   show program's version number and exit

**--debug**
:   Show debug info

**--not-empty**
:   Only groups that are not empt

# EXAMPLES

    $ sec-gather-unixgroups --not-empty
    {
        "unixgroups": {
            "audio": [
                "pulse"
            ], 
            "plugdev": [
                "fboender"
            ], 
            "sudo": [
                "fboender"
            ], 
            "lpadmin": [
                "fboender"
            ], 
            "cdrom": [
                "fboender"
            ], 
            "sambashare": [
                "fboender"
            ], 
            "docker": [
                "fboender"
            ], 
            "adm": [
                "syslog", 
                "fboender"
            ], 
            "dip": [
                "fboender"
            ]
        }
    }

# COPYRIGHT

Copyright 2017, Ferry Boender.

Licensed under the MIT license. For more information, see the LICENSE file.

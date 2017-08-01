% SEC-GATHER-UNIXGROUPS(1)
% Ferry Boender
% May 2017

<!---
Convert with pandoc to Groff man format:

pandoc this.md -s -t man > this.1
--->

# NAME

sec-gather-unixgroups – Output unix groups and their users

# SYNOPSIS

 **sec-gather-unixgroups** [**-h**] [**--version**] [**--debug**] [**--format** *{json,html}*] [**--not-empty**]

# DESCRIPTION

**sec-gather-unixgroups** gathers information about unix groups from
`/etc/groups` and their users and outputs it in a variety of formats.

# OPTIONS

**-h**, **--help**
:   Display this help message and exit

**--version**
:   show program's version number and exit

**--debug**
:   Show debug info

**--format** *{json,text,html}*
:   Output format. Default is "*text*"

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

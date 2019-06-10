% SEC-GATHER-IPTABLES(1)
% Ferry Boender
% May 2019

# NAME

sec-gather-iptables – Output firewall rules

# SYNOPSIS

 **sec-gather-iptables** [**-h**] [**--version**] [**-d**] [**--annotate** *ANNOTATIONFILE*]

# DESCRIPTION

**sec-gather-iptables** Gather iptables firewall status

# OPTIONS

**-h**, **--help**
:   Display this help message and exit

**--version**
:   show program's version number and exit

**-d** / **--debug**
:   Show debug info

**--annotate** *ANNOTATIONFILE*
:   Annotation file. A JSON file who's information will be joined with the gathered results. This can be used to add custom information to results.

# EXAMPLES

The default output looks like this:

    {
        "iptables": {
            "filter": {
                "INPUT": {
                    "policy": "DROP",
                    "rules": [
                        {
                            "chain": "INPUT",
                            "match": "state",
                            "state": "INVALID",
                            "jump": "DROP"
                        },
                        {
                            "chain": "INPUT",
                            "match": "state",
                            "state": "RELATED,ESTABLISHED",
                            "jump": "ACCEPT"
                        },
                        {
                            "chain": "INPUT",
                            "interface": "lo",
                            "jump": "ACCEPT"
                        },
                        {
                            "chain": "INPUT",
                            "proto": "icmp",
                            "jump": "ACCEPT"
                        },
                        {
                            "chain": "INPUT",
                            "src": "212.212.22.11/32",
                            "proto": "tcp",
                            "match": "tcp",
                            "dest_port": "22",
                            "jump": "ACCEPT"
                        }
                },
                "FORWARD": {
                    "policy": "DROP",
                    "rules": [
                        {
                            "chain": "FORWARD",
                            "match": "state",
                            "state": "INVALID",
                            "jump": "DROP"
                        },
                        {
                            "chain": "FORWARD",
                            "match": "state",
                            "state": "RELATED,ESTABLISHED",
                            "jump": "ACCEPT"
                        }
                    ]
                },
                "OUTPUT": {
                    "policy": "ACCEPT",
                    "rules": [
                        {
                            "chain": "OUTPUT",
                            "match": "state",
                            "state": "RELATED,ESTABLISHED",
                            "jump": "ACCEPT"
                        }
                    ]
                }
            }
        }
    }

# COPYRIGHT

Copyright 2017-2019, Ferry Boender.

Licensed under the MIT license. For more information, see the LICENSE file.

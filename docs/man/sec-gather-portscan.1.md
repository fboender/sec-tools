% SEC-GATHER-PORTSCAN(1)
% Ferry Boender
% May 2017

<!---
Convert with pandoc to Groff man format:

pandoc this.md -s -t man > this.1
--->

# NAME

sec-gather-portscan – Perform port scan and output ports.

# SYNOPSIS

 **sec-gather-portscan** [**-h**] [**--version**] [**--debug**] [**--format** *{json,html}*] [**--annotate** *ANNOTATIONFILE*] [**--ports** *PORTS*] [**--all**] *TARGETS*

# DESCRIPTION

Perform a port scan against a host using nmap (which should be installed) and
return the results in various formats. It must be run as root, or nmap won't
report all open ports for some reason. 

By default, nmap scans the "top 1000 most used ports". Which exactly those are
depends on your version of nmap. You can use the *--debug* option to find out
which ports are included in the scan. Use the *--ports* option to specify your
own range.

The hostnames in the results may not match the names of the specified hosts to
scan, because nmap does a reverse lookup of the hostname and there is no way
to match these up.

You may provide an annotation file (see **EXAMPLES**) to add custom
information to the results such as validated ports. Make sure you specify the
reverse-looked up hostname (see paragraph above).

# OPTIONS

**-h**, **--help**
:   Display this help message and exit

**--version**
:   show program's version number and exit

**--debug**
:   Show debug info

**--format** *{json,html}*
:   Output format. Default is "*json*"

**--annotate** *ANNOTATIONFILE*
:   Annotation file. A JSON file who's information will be joined with the gathered results. This can be used to add custom information to results.

**--ports** *PORTS*
:   TCP ports to scan in nmap format

**--all**
:   Report all ports, not just open ones.

**TARGET**
:   One or more target(s) to scan or a range of targets in the nmap format.


# EXAMPLES

Scan the privileged ports and port 8080 on host test.example.com:

    sudo ./sec-gather-portscan --ports 1-1024,8080 test.example.com
    {
        "openports": {
            "test.example.com": {
                "25": {
                    "reason": "syn-ack", 
                    "service_name": "smtp", 
                    "state": "open", 
                    "protocol": "tcp", 
                    "port": 25
                }, 
                "8080": {
                    "reason": "syn-ack", 
                    "service_name": "http-proxy", 
                    "state": "open", 
                    "protocol": "tcp", 
                    "port": 8080
                }
            }
        }
    }

You can annotate scanned ports your own info such as verified ports. The annotation file
looks like this:

    {
        "localhost": {
            "25": {
                "verified": true,
                "comment": "SMTP server"
            },
            "8080": {
                "verified": true,
                "comment": "Exposed dev backends"
            }
        }
    }

Note that the given hostname in the annotation file *must* match the hostname
as given in the output of *sec-gather-portscan*, because the output has the
reverse-lookup hostname, not the one given as the argument.

    sudo ./sec-gather-portscan --annotate portscan.annotate --ports 1-1024,8080 test.example.com
    {
        "openports": {
            "localhost": {
                "25": {
                    "comment": "SMTP server", 
                    "protocol": "tcp", 
                    "service_name": "smtp", 
                    "state": "open", 
                    "reason": "syn-ack", 
                    "verified": true, 
                    "port": 25
                }, 
                "8080": {
                    "comment": "Exposed dev backends", 
                    "protocol": "tcp", 
                    "service_name": "http-proxy", 
                    "state": "open", 
                    "reason": "syn-ack", 
                    "verified": true, 
                    "port": 8080
                }
            }
        }
    }

# COPYRIGHT

Copyright 2017, Ferry Boender.

Licensed under the MIT license. For more information, see the LICENSE file.

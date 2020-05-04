% SEC-GATHER-SSLSCAN(1)
% Ferry Boender
% May 2020

# NAME

sec-gather-sslscan –  Output SSL / TLS protocol and ciphers for ports

# SYNOPSIS

 **sec-gather-sslscan** [**-h**] [**--version**] [**-d**] [**--annotate** *ANNOTATIONFILE*] [**--ports** *PORTS*] *target [target ...]*


# DESCRIPTION

**sec-gather-sslscan** outputs a ports SSL / TLS protocol and ciphers for one
or more hosts. It tries to follow the same grading as the Qualys SSL lab test.

It relies on `nmap` and the `ssl-enum-ciphers` nmap script, so both of these
must be installed. The `ssl-enum-ciphers` is, as of this date, slightly
outdated with regards to the grading of ciphers. **sec-gather-sslscan** does
some post-processing to apply stricter grading per Qualys SSL lab test.


# OPTIONS

**-h**, **--help**
:   Display this help message and exit

**--version**
:   show program's version number and exit

**-d** / **--debug**
:   Show debug info

**--annotate** *ANNOTATIONFILE*
:   Annotation file. A JSON file who's information will be joined with the gathered results. This can be used to add custom information to results.

**--ports** *PORTS*
:   TCP ports to scan in nmap format

**TARGET**
:   One or more hosts or IPs to scan

# EXAMPLES

Executing:

    $ sec-gather-sslscan example.com www.example.com 192.168.1.10

The default output looks like this:

    {
        "sslscan": {
            "example.com": {
                "443": [
                    {
                        "protocol": "TLSv1.1",
                        "ciphers": [
                            {
                                "kex_info": "rsa 2048",
                                "name": "TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA",
                                "strength": "B"
                            }
                        ]
                    }
                ]
            }
        }
    }

You can use the `reports/sec-gather-sslscan.tpl` report to generate a
HTML matrix overview of hosts and ports and their protocols and ciphers:

    $ sec-gather-sslscan example.com www.example.com 192.168.1.10 | sec-report reports/sec-gather-sslscan.tpl > ssl.html

# COPYRIGHT

Copyright 2017-2020, Ferry Boender.

Licensed under the MIT license. For more information, see the LICENSE file.

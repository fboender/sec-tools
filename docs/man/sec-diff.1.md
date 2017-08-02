% SEC-DIFF(1)
% Ferry Boender
% May 2017

<!---
Convert with pandoc to Groff man format:

pandoc this.md -s -t man > this.1
--->

# NAME

sec-diff – Diff JSON from stdin (sec-gather-X) against JSON from file.

# SYNOPSIS

 **sec-diff** [**-h**] [**--version**] [**--debug**] [**--format** *{json,text,html}*] [**--exclude** *EXCLUDE*] *STATEFILE*

# DESCRIPTION

**sec-diff** can be used to diff (deep compare) JSON output from a
**sec-gather** script with a previous run. The first time **sec-diff** runs,
it will output nothing.  Subsequent invocations will show any differences
(additions, deletions and modifications) in the JSON output.

Diff output can be shown in a variety of formats. The **sec-mail** tool can be
used to mail changes.

# OPTIONS

**-h**, **--help**
:   Display this help message and exit

**--version**
:   show program's version number and exit

**--debug**
:   Show debug info

**--format** *{json,text,html}*
:   Output format. Default is "*text*"

**--exclude** *EXCLUDE*
:   Exclude keys from diffing. Useful for keys that always change.

**STATEFILE**
:   File to compare against and save current output.

# EXAMPLES

The following example stores listening ports in a state file:

    $ sec-gather-listenports | sec-diff listenports.state

If a new service starts listening on a port, and we run the command again, the
output (in `text` format) will look like:

    $ sec-gather-listenports | sec-diff listenports.state

      - Added to "listenports":
    
        {u'local_address': u'127.0.0.1',
        u'local_port': 5555,
        u'pid': 31978,
        u'prog': u'nc',
        u'proto': u'tcp',
        u'recv_queue': 0,
        u'remote_address': u'0.0.0.0',
        u'remote_port': 0,
        u'send_queue': 0,
        u'service': u'Unknown',
        u'state': u'LISTEN',
        u'verified': False}

If the chosen output format is JSON, it would look like:

    [
        {
            "action": "added", 
            "path": [
                "listenports"
            ], 
            "type": "dict", 
            "key": "5555", 
            "value": {
                "recv_queue": 0, 
                "verified": false, 
                "service": "Unknown", 
                "proto": "tcp", 
                "remote_port": 0, 
                "pid": 1859, 
                "remote_address": "0.0.0.0", 
                "local_port": 5555, 
                "state": "LISTEN", 
                "prog": "python2.7", 
                "local_address": "127.0.0.1", 
                "send_queue": 0
            }
        }
    ]

Exclude all items starting with `listenports.53`:

    $ sec-gather-listenports | sec-diff --exclude listenports.53 listenports.state

Exclude all PID changes for all ports:

    $ sec-gather-listenports | sec-diff --exclude listenports.*.pid listenports.state

Exclude all PID and Prog changes for all ports:

    $ sec-gather-listenports | sec-diff --exclude listenports.*.pid,listenports.*.prog listenports.state

# COPYRIGHT

Copyright 2017, Ferry Boender.

Licensed under the MIT license. For more information, see the LICENSE file.

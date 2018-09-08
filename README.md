Security Tools
==============

1. [About](#about)
1. [Requirements](#requirements)
1. [Overview of tools](#overview)
1. [Gather scripts](#gather)
1. [Diffing and alerting](#alert)
1. [Reporting](#report)


## <a name="about">About</a>

These are security tools for reporting and alerting about security information
and events. The focus is on gathering and annotating authentication,
authorization and system configuration information and reporting and alerting
based on this information.

The tools are written as separate unix tools that read and write from / to
standard output. These can be combined to produce the desired result.

## <a name="overview">Overview of tools</a>

* **[sec-gather-listenports](docs/man/sec-gather-listenports.1.md)**: Output listening services / ports
* **[sec-gather-mysqlusers](docs/man/sec-gather-mysqlusers.1.md)**: Output MySQL users and privileges
* **[sec-gather-openvpnusers](docs/man/sec-gather-openvpnusers.1.md)**: Output OpenVPN client certificate status
* **[sec-gather-unixgroups](docs/man/sec-gather-unixgroups.1.md)**: Output unix groups and their members
* **[sec-gather-unixusers](docs/man/sec-gather-unixusers.1.md)**: Output unix users and their details
* **[sec-gather-portscan](docs/man/sec-gather-portscan.1.md)**: Output open ports detected through a portscan of a host
* **[sec-diff](docs/man/sec-diff.1.md)**: Output changes in `sec-gather-*` script output since last time
* **[sec-report](docs/man/sec-report.1.md)**: Generate HTML and PDF reports from gathered info
* **[sec-mail](docs/man/sec-mail.1.md)**: Send alerts and reports.

## <a name="installation">Installation</a>

sec-tools requires the Mako Python library. Debian / Ubuntu users can install
it with:

    $ sudo apt install python-mako

Clone the `sec-tools` repository and run the install Make job:

    $ git clone ...
    $ cd sec-tools
    $ sudo make install

This will install all the tools and the manual pages. 

## <a name="gather">Gather scripts</a>

The `gather` tools gather information and output json or html output. Example usage:

    sec-gather-listenports --no-local --annotate listenports-annotation.json --format json
    sec-gather-unixusers --login --format json
    sec-gather-unixgroups --not-empty --format html

The JSON output would look something like:

    {
      "listenports": {
        "8000": {
          "pid": 30925, 
          "remote_address": "0.0.0.0", 
          "recv_queue": 0, 
          "verified": false, 
          "service": "Unknown", 
          "remote_port": 0, 
          "proto": "tcp", 
          "local_port": 8000, 
          "state": "LISTEN", 
          "prog": "python2.7", 
          "local_address": "127.0.0.1", 
          "send_queue": 0
        }
      }
    }

The gather script generally provide options for additional filtering and
manual annotations of gathered information.

For more information, check out the [manual pages](docs/man).

## <a name="alert">Diffing and alerting</a>

The [sec-diff](docs/man/sec-diff.1.md) tool can be used to diff JSON output
from a `sec-gather` script with a previous run.

For example:

	$ sec-gather-listenports | sec-diff /var/cache/sec-tools/listenports.state

This will store the listening ports in
`/var/cache/sec-tools/listenports.state`. The first run, it will report
nothing. The next time it's run, a new listening port has appeared, and
`sec-diff` reports about it:

	$ sec-gather-listenports | sec-diff /var/cache/sec-tools/listenports.state

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

If nothing changed, the output will be empty.

This can be used to alert about changes in listening services, unix users or
any other `gather` script. To do so, you can use the
[sec-mail](docs/man/sec-mail.1.md) script:

	$ sec-gather-listenports | \
      sec-diff /var/cache/sec-tools/listenports | \
      mail -t security@example.org --subject "Listening services changed on $(hostname -f)"

You can exclude certain paths from being reported about. For example:

    # Exclude all items starting with 'listenports.53'
    sec-gather-listenports | sec-diff --exclude listenports.53 listenports.state

    # Exclude all PID changes for all ports.
    sec-gather-listenports | sec-diff --exclude listenports.*.pid listenports.state

    # Exclude all PID and Prog changes for all ports
    sec-gather-listenports | sec-diff --exclude listenports.*.pid,listenports.*.prog listenports.state

For more information, check out the manual pages for each tool:

* **[sec-diff](docs/man/sec-diff.1.md)**
* **[sec-mail](docs/man/sec-mail.1.md)**

## <a name="report">Reporting</a>

The [sec-report](docs/man/sec-report.1.md) tool renders a [Mako
template](http://www.makotemplates.org/) to HTML. The output is written to
stdout and can be used to generate a PDF with a tool like html2pdf. For an
example, see the [example report](example/report).

Reports can call gather scripts themselves, or can be fed JSON and other data
through ASSET parameters.

You can either write your own reports (see the [examples](examples/)) or use
a pre-made one from the [tools](tools/) directory.

For more information, check out the manual pages for each tool:

* **[sec-report](docs/man/sec-report.1.md)**

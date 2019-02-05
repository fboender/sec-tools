Security Tools
==============

## <a name="about">About</a>

These are tools for reporting and alerting about security information and
events. The focus is on gathering and annotating authentication, authorization
and system configuration information and reporting and alerting based on this
information.

Together, these tools provide means for:

* Reviewing and hardening system security.
* Reporting of security configuration problems and alerting of changes in
  configuration.
* Reporting of user privileges and alerting of changes in privileges.
* Intrusion detection.

The tools are written as separate unix tools that read and write from / to
standard output. These can be combined to produce the desired result.

Some examples of possible usage scenarios:

* Generate a report of all user permissions (unix, mysql, etc).
* Generate email alerts when a new open port is detected on a system.
* Generate email alerts when users are created, modified or deleted.


## <a name="overview">Overview of tools</a>

* **[sec-gather-listenports](docs/man/sec-gather-listenports.1.md)**: Output listening services / ports
* **[sec-gather-mysqlusers](docs/man/sec-gather-mysqlusers.1.md)**: Output MySQL users and privileges
* **[sec-gather-openvpnusers](docs/man/sec-gather-openvpnusers.1.md)**: Output OpenVPN client certificate status
* **[sec-gather-unixgroups](docs/man/sec-gather-unixgroups.1.md)**: Output unix groups and their members
* **[sec-gather-unixusers](docs/man/sec-gather-unixusers.1.md)**: Output unix users and their details
* **[sec-gather-portscan](docs/man/sec-gather-portscan.1.md)**: Output open ports detected through a portscan of a host
* **[sec-gather-misconfigs](docs/man/sec-gather-misconfigs.1.md)**: Scan for common security misconfigurations
* **[sec-diff](docs/man/sec-diff.1.md)**: Output changes in `sec-gather-*` script output since last time
* **[sec-report](docs/man/sec-report.1.md)**: Generate HTML and PDF reports from gathered info
* **[sec-mail](docs/man/sec-mail.1.md)**: Send alerts and reports.

## <a name="installation">Installation</a>

sec-tools requires **Python v3.4+**.

You must also install the required dependencies.

Clone the `sec-tools` repository and run the install:

    $ git clone ...
    $ cd sec-tools
    $ pip install -r ./requirements.txt
    $ sudo bash -c '. build.sla install'

This will install all the tools and the manual pages. 

## <a name="gather">Gather scripts</a>

The `gather` tools gather information and output JSON. Example usage:

    sec-gather-listenports --no-local --annotate listenports-annotation.json
    sec-gather-unixusers --login
    sec-gather-unixgroups --not-empty

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
manual annotations of gathered information. Reports to convert the JSON output
to HTML are provided in the `reports` directory

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

        "8888": {
          "recv_queue": 0, 
          "verified": false, 
          "service": "Unknown", 
          "remote_port": 0, 
          "proto": "tcp", 
          "pid": 3747, 
          "remote_address": "0.0.0.0", 
          "local_port": 8888, 
          "state": "LISTEN", 
          "prog": "nc", 
          "local_address": "0.0.0.0", 
          "send_queue": 0
        }

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

Reports can JSON from STDIN or files through `ASSET` params. You can either
write your own reports (see the [examples](examples/) dir) or use a pre-made
one from the [reports](src/reports/) directory.

Example usage:

    # One-off report of listening ports
    $ sudo sec-gather-listenports | sec-report sec-gather-listenports.tpl

    # Generate some host information using sec-gather- scripts and generate a
    # host report.
    $ mkdir out
    $ sudo sec-gather-listenports > out/listenports
    $ sudo sec-gather-misconfigs > out/misconfigs
    $ sudo sec-gather-mysqlusers > out/mysqlusers
    $ sec-report --title "Security report for $(hostname -f)" host_report.tpl out/* > host_report.html

For more information, check out the manual page:

* **[sec-report](docs/man/sec-report.1.md)**

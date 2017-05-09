Security Tools
==============

These are security tools for reporting and alerting about security
information. The current focus is on user authorization / authentication.

The tools are written as separate unix tools that read and write from / to
standard output. These can be combined to produce the desired result.

## Overview of tools

* `sec-gather-listenports`: Output listening services / ports
* `sec-gather-mysqlusers`: Output MySQL users and privileges
* `sec-gather-openvpnusers`: Output OpenVPN client certificate status
* `sec-gather-unixgroups`: Output unix groups and their members
* `sec-gather-unixusers`: Output unix users and their details
* `sec-diff`: Output changes in `*-gather-*` script output since last time
* `sec-report`: Generate HTML and PDF reports from gathered info
* `sec-mail`: Send alerts and reports.


## Gather scripts

The `gather` tools gather information and output json or html output. Example usage:

    ./sec-gather-listenports --no-local --annotate listenports-annotation.json --format json
    ./sec-gather-unixusers --login --format json
    ./sec-gather-unixgroups --not-empty --format html

The gather script generally provide options for additional filtering. 

### sec-gather-listenports

List listening services / ports on a system.

An optional `--annotate` flag can be passed with a JSON file as argument. The
output will be augmented with additional info about the service. Example
annotation JSON file:

    {
        "22": {
            "service": "SSH",
            "verified": true
        },
        "3306": {
            "service": "MySQL",
            "verified": true
        },
        "3973": {
            "service": "Vat JBoss",
            "verified": false
        },
        "10050": {
            "service": "Zabbix agent",
            "verified": true
        }
    }

### sec-gather-mysqlusers

List MySQL users and their connect / database privileges.

`sec-gather-mysqlusers` does not take arguments to connect to the database.
Instead, it relies on a `~/.my.cnf` to be present to connect to the database.

FIXME: Add example .my.cnf

### sec-gather-openvpnusers

Gather details about OpenVPN users. This assumes you're using EasyRSA to
manage the certificates. You should point `sec-gather-openvpnusers` to the
`index.txt` file containing the client certificates. For example:

    sec-gather-openvpnusers /data/certificates/keys/index.txt

### sec-gather-unixgroups

List unix groups and their members.

### sec-gather-unixusers

List unix users and their groups.

## Alerting / Diffing

The `sec-diff` tool can be used to diff JSON output from a `sec-gather` script
with a previous run. For example:

	$ sec-gather-listenports | sec-diff /var/cache/sec-tools/listenports

This will store the listening ports in `/var/cache/sec-tools/listenports`. The
first run, it will report nothing. The next time it's run, a new listening
port has appeared, and `sec-diff` reports about it:

	$ sec-gather-listenports | sec-diff /var/cache/sec-tools/listenports

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
any other `gather` script. To do so, you can use the `sec-mail` script:

	$ sec-gather-listenports | \
      sec-diff /var/cache/sec-tools/listenports | \
      sec-mail --to security@example.org --subject "Listening services changed on $(hostname -f)"


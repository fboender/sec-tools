#!/bin/bash

#
# This example scripts sends emails when new open ports are detected on given
# hosts.
#
# A matching cronjob could look like this:
#
#  5 0 * * * cd /data/scripts/sec-tools;./events-portscan.sh
#

NOW="$(date +'%Y-%m-%d')"
RECIPIENTS="security@megacorp.com"
DELAY=60  # Delay between scanning hosts

# Scan a host and send email if open ports on that host have changed
scan() {
  HOST=$1
  ARGS_PORTSCAN=$2
  ARGS_DIFF=$3

  OUTPUT=$(sec-gather-portscan $ARGS_PORTSCAN $HOST | sec-diff $ARGS_DIFF portscan-$HOST.state)
  if [ -n "$OUTPUT" ]; then
    echo "$OUTPUT" | /usr/bin/mail -s "Security event for $HOST: public open ports status changed" $RECIPIENTS
  fi
  sleep $DELAY
}

scan www1.megacorp.com "--ports-exclude 49155:49167"
scan www2.megacorp.com "--ports-exclude 49155:49167"
scan www3.megacorp.com "--ports-exclude 49155:49167"

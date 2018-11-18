#/bin/sh

# Run some simple tests

# Gather scripts
src/sec-gather-listenports > /dev/null
#src/sec-gather-mysqlusers > /dev/null
#src/sec-gather-openvpnusers > /dev/null
src/sec-gather-unixgroups > /dev/null
src/sec-gather-unixusers > /dev/null
src/sec-gather-unixsessions > /dev/null
src/sec-gather-misconfigs > /dev/null

# sec-diff
src/sec-gather-unixusers | src/sec-diff tmp.test
src/sec-gather-unixusers | src/sec-diff tmp.test
rm tmp.test

# Generate report
src/sec-gather-unixusers | src/sec-report sec-gather-unixusers.tpl > /dev/null

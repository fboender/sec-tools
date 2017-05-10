<%
title = "User account and Services overview ({})".format(fqdn)

unixusers = gather("./sec-gather-unixusers --login --format html")
unixgroups = gather("./sec-gather-unixgroups --not-empty --format html")
listenports = gather("./sec-gather-listenports --annotate=../example/listenports-annotate/listenports-annotate.json --format html")
mysqlusers = gather("./sec-gather-mysqlusers --no-conn-error --format html")
openvpnusers = gather("./sec-gather-openvpnusers --format html ../example/report/vpn_index.txt")

%>
<html>
    <head>
        <title>${title}</title>
        <style>
            /* Custom CSS */
            body { font-family: sans-serif; }
            h2 { margin-top: 64px; }
            p { color: #606060; }

            table { border-collapse: collapse; }
            table tr { vertical-align: top; border-bottom: 1px solid #C0C0C0; }
            table tr:last-child { border-bottom: none; }
            table tr th { text-align: left; padding: 8px; background-color: #F0F0F5; }
            table tr td { padding: 8px; }
            table tr td ul { padding-left: 20px; list-style-type: square; margin: 0px; }

            .verified { color: #008000; }
            .unverified { color: #800000; }

            /* Account statusses */
            .acc-active { color: #004000; }
            .acc-inactive { color: #A0A0A0; }
            .acc-revoked { color: #800000; }
        </style>
    </head>
    <body>
        <h1>${title}</h1>

        <h2>Unix users</h2>
        <p>Users with a standard Unix account on this machine. Unix accounts
        are generally allowed to log into services on the machine such as ssh,
        imap, etc. Users in the <b>sudo</b> group are allowed to elevate their
        privileges to root.</p>
        ${unixusers}

        <h2>Unix groups</h2>
        <p>Unix groups and the users that are a member of the group. Users in
        the <b>sudo</b> group are allowed to elevate their privileges to
        root.</p>
        ${unixgroups}

        <h2>MySQL users</h2>
        <p>MySQL users and their permissions of the MySQL server running on
        ${fqdn}.</p>
        ${mysqlusers}

        <h2>Listening services</h2>
        <p>Listening services are services that are accessible through the
        network. Services listening on <code>127.0.0.1</code> are <b>not</b>
        available from external hosts. Verified host are marked as green.
        Unverified hosts as red. Hosts can be set to 'verified' by editing the
        <code>listenports-annotation.json</code> file.</p>
        ${listenports}

        <h2>OpenVPN users</h2>
        <p>OpenVPN user certificates and their validities.</p>
        ${openvpnusers}
    </body>
</html>

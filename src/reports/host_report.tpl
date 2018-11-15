<%inherit file="master.tpl"/>

<h1>
    % if title is not None:
        ${ title }
    % else:
        Host report
    % endif
</h1>

% if "unixusers" in data:
    <%namespace name="unixusers" file="sec-gather-unixusers.tpl"/>
    ${ unixusers.results(title="Unix users", heading_offset=1) }
% endif

% if "unixgroups" in data:
    <%namespace name="unixgroups" file="sec-gather-unixgroups.tpl"/>
    ${ unixgroups.results(title="Unix groups", heading_offset=1) }
% endif

% if "mysqlusers" in data:
    <%namespace name="mysqlusers" file="sec-gather-mysqlusers.tpl"/>
    ${ mysqlusers.results(title="MySQL users", heading_offset=1) }
% endif

% if "openvpnusers" in data:
    <%namespace name="openvpnusers" file="sec-gather-openvpnusers.tpl"/>
    ${ openvpnusers.results(title="Openvpn users", heading_offset=1) }
% endif

% if "listenports" in data:
    <%namespace name="listenports" file="sec-gather-listenports.tpl"/>
    ${ listenports.results(title="Listening ports", heading_offset=1) }
% endif

% if "misconfigs" in data:
    <%namespace name="misconfigs" file="sec-gather-misconfigs.tpl"/>
    ${ misconfigs.results(title="Mis-configurations", heading_offset=1) }
% endif

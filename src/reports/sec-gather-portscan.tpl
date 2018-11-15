<%inherit file="master.tpl"/>

<%def name="results(title, heading_offset=0)">
    <h${ heading_offset + 1 }>
    % if title is not None:
        ${ title }
    % else:
        Portscan
    % endif
    </h${ heading_offset + 1 }>

    <p class="description">Port scan</p>

    <table>
        <tr>
            <th>Host</th>
            <th>Port</th>
            <th>Protocol</th>
            <th>State</th>
            <th>Reason</th>
            <th>Verified</th>
            <th>Comment</th>
        </tr>
        % for host in data["portscan"].keys():
            % for portnr in data["portscan"][host].keys():
                <%
                portdetail = data["portscan"][host][portnr]

                verified = "unverified"
                if portdetail.get("verified", False) is True:
                    verified = "verified"
                endif

                %>
                <tr class="${verified}">
                    <td>${host}</td>
                    <td>${portdetail['port']}</td>
                    <td>${portdetail['protocol']}</td>
                    <td>${portdetail['state']}</td>
                    <td>${portdetail['reason']}</td>
                    <td>${portdetail.get('verified', False)}</td>
                    <td>${portdetail.get('comment', '')}</td>
                </tr>
            % endfor
        % endfor
    </table>
</%def>

${ results(title=title) }

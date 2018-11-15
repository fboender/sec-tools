<%inherit file="master.tpl"/>

<%def name="results(title, heading_offset=0)">
    <h${ heading_offset + 1 }>
    % if title is not None:
        ${ title }
    % else:
        Listening ports
    % endif
    </h${ heading_offset + 1 }>

    <p class="description">Listening services are services that are
    accessible through the network. Services listening on 127.0.0.1 are
    not available from external hosts. Verified host are marked as
    green. Unverified hosts as red. Hosts can be set to 'verified' by
    editing the listenports-annotation.json file.</p>

    <table>
        <tr>
            <th>Protocol</th>
            <th>Local address</th>
            <th>Local port</th>
            <th>State</th>
            <th>PID</th>
            <th>Program</th>
            <th>Service</th>
            <th>Verified</th>
        </tr>
        % for portnr in sorted(data["listenports"].keys()):
            <%
            portdetail = data["listenports"][portnr]

            verified = "unverified"
            if portdetail["verified"] is True:
                verified = "verified"
            endif

            %>
            <tr class="${verified}">
                <td>${portdetail['proto']}</td>
                <td>${portdetail['local_address']}</td>
                <td>${portdetail['local_port']}</td>
                <td>${portdetail['state']}</td>
                <td>${portdetail['pid']}</td>
                <td>${portdetail['prog']}</td>
                <td>${portdetail['service']}</td>
                <td>${portdetail['verified']}</td>
            </tr>
        % endfor
    </table>
</%def>

${ results(title=title) }

<%inherit file="master.tpl"/>

<%def name="results(title, heading_offset=0)">
    <h${ heading_offset + 1 }>
    % if title is not None:
        ${ title }
    % else:
        OpenVPN certificates.
    % endif
    </h${ heading_offset + 1 }>

    <p class="description">OpenVPN users</p>

    <%
    import datetime
    today = datetime.date.today()
    %>
    <table>
        <tr>
            <th>Username</th>
            <th>Full name</th>
            <th>Status</th>
            <th>Valid until</th>
        </tr>
        % for username in sorted(data["openvpnusers"].keys()):
            <%
            userdetail = data["openvpnusers"][username]

            if userdetail["status"] == 'Valid':
                active = "acc-active"
            elif userdetail["status"] == "Expired":
                active = "acc-inactive"
            elif userdetail["status"] == "Revoked":
                active = "acc-revoked"
            endif
            %>
            <tr class="${active}">
                <td>${username}</td>
                <td>${userdetail["subject"]["name"]}</td>
                <td>${userdetail["status"]}</td>
                <td>${userdetail["valid_until"]}</td>
            </tr>
        % endfor
    </table>
</%def>

${ results(title=title) }

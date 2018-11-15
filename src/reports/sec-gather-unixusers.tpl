<%inherit file="master.tpl"/>

<%def name="results(title, heading_offset=0)">
    <h${ heading_offset + 1 }>
    % if title is not None:
        ${ title }
    % else:
        Unix users
    % endif
    </h${ heading_offset + 1 }>

    <p class="description">Unix users</p>

    <table>
        <tr>
            <th>Username</th>
            <th>Shell</th>
            <th>Homedir</th>
            <th>Groups</th>
        </tr>
        % for username in sorted(data["unixusers"].keys()):
            <%
            userdetail = data["unixusers"][username]
            %>
            <tr>
                <td>${username}</td>
                <td>${userdetail['shell']}</td>
                <td>${userdetail['homedir']}</td>
                <td>
                    <ul>
                        % for group in userdetail['groups']:
                            <li>${group}</li>
                        % endfor
                    </ul>
                </td>
            </tr>
        % endfor
    </table>
</%def>

${ results(title=title) }

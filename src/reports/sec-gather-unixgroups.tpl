<%inherit file="master.tpl"/>

<%def name="results(title, heading_offset=0)">
    <h${ heading_offset + 1 }>
    % if title is not None:
        ${ title }
    % else:
        Unix groups
    % endif
    </h${ heading_offset + 1 }>

    <p class="description">Unix groups</p>

    <table>
        <tr>
            <th>Group</th>
            <th>Members</th>
        </tr>
        % for groupname in sorted(data["unixgroups"].keys()):
            <%
            members = data["unixgroups"][groupname]
            %>
            <tr>
                <td>${groupname}</td>
                <td>
                    <ul>
                        % for username in members:
                            <li>${username}</li>
                        % endfor
                    </ul>
                </td>
            </tr>
        % endfor
    </table>
</%def>

${ results(title=title) }

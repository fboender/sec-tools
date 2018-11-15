<%inherit file="master.tpl"/>

<%def name="results(title, heading_offset=0)">
    <h${ heading_offset + 1 }>
    % if title is not None:
        ${ title }
    % else:
        MySQL users
    % endif
    </h${ heading_offset + 1 }>

    <p class="description">MySQL users and their permissions.</p>

    <table>
        <tr>
            <th>User</th>
            <th>From</th>
            <th>Database</th>
            <th>Rights</th>
        </tr>
        % for username in sorted(data["mysqlusers"].keys()):
            <%
            mysqluser = data["mysqlusers"][username]
            %>

            % if mysqluser["rights_all_dbs"] != "":
                <tr class="">
                    <td>${username}</td>
                    <td>${", ".join(mysqluser["from_hosts"])}</td>
                    <td><b>ALL</b></td>
                    <td>${mysqluser["rights_all_dbs"]}</td>
                </tr>
            % endif
            % for db_name, db_rights in mysqluser["dbs"].items():
                <tr class="">
                    <td>${username}</td>
                    <td>${", ".join(mysqluser["from_hosts"])}</td>
                    <td>${db_name}</td>
                    <td>${db_rights}</td>
                </tr>
            % endfor
        % endfor
    </table>
</%def>

${ results(title=title) }

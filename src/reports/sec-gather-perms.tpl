<%inherit file="master.tpl"/>

<%def name="results(title, heading_offset=0)">
    <h${ heading_offset + 1 }>
    % if title is not None:
        ${ title }
    % else:
        Files and dirs with dangerous permissions
    % endif
    </h${ heading_offset + 1 }>

    <p class="description">Files and dirs with dangerous permissions. These
    aren't security issues, but if they change, it might indicate a security
    breach.</p>

    <table>
        <tr>
            <th>Path</th>
            <th>Mode</th>
            <th>World-writable</th>
            <th>SetUID</th>
        </tr>
        % for file_info in data["perms"]:
            <tr class="">
                <td>${file_info["path"]}</td>
                <td><tt>${file_info["mode_hr"]}</tt></td>
                <td>
                    % if "world_writable" in file_info["trigger_modes"]:
                        <span class="failed">Yes</span>
                    % else:
                        <span class="passed">No</span>
                    % endif
                </td>
                <td>
                    % if "setuid" in file_info["trigger_modes"]:
                        <span class="failed">Yes</span>
                    % else:
                        <span class="passed">No</span>
                    % endif
                </td>
            </tr>
        % endfor
    </table>
</%def>

${ results(title=title) }

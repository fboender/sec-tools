<%inherit file="master.tpl"/>

<%def name="results(title, heading_offset=0)">
    <h${ heading_offset + 1 }>
    % if title is not None:
        ${ title }
    % else:
        Iptables
    % endif
    </h${ heading_offset + 1 }>

    <p class="description">Iptables Firewall</p>

    <h${ heading_offset + 2 }>Chain default policies</h${ heading_offset + 2 }>
    <table>
        <tr>
            <th>Table</th>
            <th>Chain</th>
            <th>Policy</th>
        </tr>
        % for table_name, chains in data["iptables"].items():
            % for chain_name in sorted(chains.keys()):
                <%
                policy = chains[chain_name]["policy"]
                _class=""

                if (chain_name == "INPUT" or chain_name == "FORWARD"):
                    if policy in ("DROP", "DENY"):
                        _class = "passed"
                    else:
                        _class = "failed"
                %>
                <tr class="${ _class }">
                    <td>${ table_name }</td>
                    <td>${ chain_name }</td>
                    <td>${ policy }</td>
                </tr>
            % endfor
        % endfor
    </table>

    <h${ heading_offset + 2 }>Chain rules</h${ heading_offset + 2 }>
    <table>
        <tr>
            <th>Table</th>
            <th>Chain</th>
            <th>State</th>
            <th>Match</th>
            <th>Interface</th>
            <th>Protocol</th>
            <th>Source addr</th>
            <th>Dest addr</th>
            <th>Dest port</th>
            <th>Jump</th>
        </tr>
        % for table_name, chains in data["iptables"].items():
            % for chain_name in sorted(chains.keys()):
                % for rule in chains[chain_name]["rules"]:
                    <%
                    _class=""

                    if (rule.get("state", "") == "INVALID" and rule.get("jump", "") == "DROP") or \
                       (rule.get("interface", "") == "lo") or \
                       (rule.get("state", "") == "RELATED,ESTABLISHED" and rule.get("jump", "") == "ACCEPT") or \
                       (rule.get("proto", "") == "icmp" and rule.get("jump", "") == "ACCEPT"):
                        _class="unimportant"
                    %>
                    <tr class="${ _class }">
                        <td>${ table_name }</td>
                        <td>${ chain_name }</td>
                        <td>${ rule.get("state", "*") }</td>
                        <td>${ rule.get("match", "*") }</td>
                        <td>${ rule.get("interface", "*") }</td>
                        <td>${ rule.get("proto", "*") }</td>
                        <td>${ rule.get("src", "*") }</td>
                        <td>${ rule.get("dest", "*") }</td>
                        <td>${ rule.get("dest_port", "*") }</td>
                        <td>${ rule.get("jump", "*") }</td>
                    </tr>
                % endfor
            % endfor
        % endfor
    </table>
</%def>

${ results(title=title) }

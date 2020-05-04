<%inherit file="master.tpl"/>

<%def name="passfailed_proto(proto)">
    % if proto.lower() not in ["tlsv1.2", "tlsv1.3"]:
        failed
    % else:
        passed
    % endif
</%def>

<%def name="passfailed_cipher(cipher)">
    % if cipher["strength"] != 'A':
        failed
    % else:
        passed
    % endif
</%def>

<%def name="results(title, heading_offset=0)">
    <h${ heading_offset + 1 }>
    % if title is not None:
        ${ title }
    % else:
        Port SSL / TLS protocol and cypher overview
    % endif
    </h${ heading_offset + 1 }>

    <p class="description"></p>

    % for host, scanresults in data["sslscan"].items():
      <h2>${host}</h2>
      <table>
        % for port, port_info in scanresults.items():
            % for proto in port_info:
                % if "warnings" in proto and proto["warnings"]:
                    <tr>
                        <th>Port</th>
                        <th>Protocol</th>
                        <th colspan=2>Warning</th>
                    </tr>
                    % for warning in proto["warnings"]:
                        <tr>
                            <td>${port}</td>
                            <td class="${passfailed_proto(proto["protocol"])}">${proto["protocol"]}</td>
                            <td colspan=2 class="failed">${ warning }</td>
                        </tr>
                    % endfor
                % endif

                <tr>
                    <th>Port</th>
                    <th>Protocol</th>
                    <th>Cipher</th>
                    <th>Strength</th>
                </tr>
                % for cipher in proto["ciphers"]:
                    <tr>
                        <td>${port}</td>
                        <td class="${passfailed_proto(proto["protocol"])}">${proto["protocol"]}</td>
                        <td class="${passfailed_cipher(cipher)}">${cipher["name"]}</td>
                        <td class="${passfailed_cipher(cipher)}">${cipher["strength"]}</td>
                    </tr>
                % endfor
            % endfor
        % endfor
      </table>
    % endfor
</%def>

${ results(title=title) }

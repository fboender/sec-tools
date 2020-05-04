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
        Port SSL / TLS protocol and cipher overview
    % endif
    </h${ heading_offset + 1 }>

    <p class="description">
        This report lists the SSL / TLS protocols and ciphers per port for one
        or more hosts. SSL / TLS are cryptographic protocols designed to
        provide communications security over a computer network. SSL was
        renamed to TLS in 1999.
    </p>

    <p class="description">
        This report tries to follow the same grading as the <a href="https://www.ssllabs.com/ssltest">Qualys SSL labs test</a>.
    </p>

    <p class="description">
        <h${ heading_offset + 2 }>Protocols</h${ heading_offset + 2 }>
        <dl>
            <dt>SSL v2.0</dt>
            <dd>SSL v2.0 is considered <b class="failed">extremely weak</b>.</dd>

            <dt>SSL v3.0</dt>
            <dd>SSL v3.0 is considered <b class="failed">extremely weak</b> and is vulnerable to the <a href="https://en.wikipedia.org/wiki/POODLE">POODLE</a> attack.</dd>

            <dt>TLS v1.0</dt>
            <dd>TLS v1.0 is considered <b class="failed">extremely weak</b> because it is vulnerable to a downgrade attack to SSL v3.0.</dd>

            <dt>TLS v1.1</dt>
            <dd>TLS v1.1 is considered <b class="failed">moderately weak</b> because it allows (and uses by default) outdated ciphers.</dd>
        </dl>

        <h${ heading_offset + 2 }>Ciphers</h${ heading_offset + 2 }>
        <dl>
            <dt>CBC</dt>
            <dd>CBC is considered <b class="failed">moderately weak</b> because it is highly likely to contain implementation problems.</dd>

            <dt>SHA</dt>
            <dd>SHA is considered <b class="failed">weak</b> because several attacks have been found feasable against it.</dd>
        </dl>
    </p>

    % for host, scan_results in data["sslscan"].items():
      <h2>${host}</h2>
      <table>
        % for port, port_info in scan_results.items():
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

<%inherit file="master.tpl"/>

<%
    import datetime
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
%>

<%def name="passfailed(header_name, header_value)">
    % if header_value is None:
        failed
    % else:
        % if header_name == "Access-Control-Allow-Origin" and header_value == "*":
            failed
        % else:
            passed
        % endif
    % endif
</%def>

<%def name="results(title, heading_offset=0)">
    <%
    headers = {
        "Content-Security-Policy": "CSP",
        "Strict-Transport-Security": "HTST",
        "X-Frame-Options": "Frame Options",
        "X-XSS-Protection": "XSS Protection",
        "X-Content-Type-Options": "Content-type options",
        "Access-Control-Allow-Origin": "CORS Origin",
        "Access-Control-Allow-Headers": "CORS Headers",
        "Access-Control-Allow-Methods": "CORS Methods",
        "Public-key-pins": "HPKP",
        "Referrer-Policy": "Referrer Policy",
        "Expect-CT": "Except CT",
        "Feature-Policy": "Feature Policy",
    }
    %>

    <h${ heading_offset + 1 }>
    % if title is not None:
        ${ title }
    % else:
        HTTP Security Headers Matrix
    % endif
    </h${ heading_offset + 1 }>

    <p class="generated-on">
    Generated ${ now }.
    </p>

    <p class="description">HTTP Security headers per URL.</p>

    <p class="description">
        <dl>
            <dt>CORS (Cross Origin Resource Sharing)</dt>
            <dd>Tell a browser to let a web application running at one origin (domain) have permission to access selected resources from a server at a different origin</dd>

            <dt>CSP (Content Security Policy)</dt>
            <dd>Mitigate and report cross site scripting attacks by telling the browser what it should and shouldn't load and execute.</dd>

            <dt>Expect-CT (Expect Certificate Transparancy)</dt>
            <dd>Opt in to reporting and/or enforcement of Certificate Transparency requirements, which prevents the use of misissued certificates for that site from going unnoticed.</dd>

            <dt>Feature Policy</dt>
            <dd>Instruct the browser about which browser features (camera, geolocation, fullscreen, etc) the web application is allowed to use.</dd>

            <dt>HPKP (HTTP Public Key Pinning)</dt>
            <dd>A security feature that tells a web client to associate a specific cryptographic public key with a certain web server to decrease the risk of MITM attacks with forged certificates.</dd>

            <dt>Referrer Policy</dt>
            <dd>Instruct the browser on which information to include in the Referrer header on subsequent requests.</dd>

            <dt>HSTS (Strict Transport Securiy)</dt>
            <dd>Tell the user's browser to always connect to the HTTPS version of the site from now on, and skip redirects from a non-secure (http) version of the site.</dd>

            <dt>Content-type options</dt>
            <dd>Instruct the browser not to guess the content type of data, but to trust the server's indication of the content type.</dd>

            <dt>Frame Options</dt>
            <dd>Tell the browser whether the current site may be loaded in a frame or iframe.</dd>

            <dt>XSS Protection</dt>
            <dd>Instruct old browsers to activate their Cross site scripting protection.</dd>

        </dl>
    </p>

    <table>
        <tr>
            <th></th>
            % for header_full, header_abbr in sorted(headers.items()):
                <th><abbr title="${ header_full }">${ header_abbr }</abbr></th>
            % endfor
        </tr>
        % for url in sorted(data["http_headers"].keys()):
            <%
            headers = data["http_headers"][url]
            %>

            <tr>
                <td><b>${url}</b></td>
                % for header_full, header_abbr in sorted(headers.items()):
                    <td class="${ passfailed(header_full, headers[header_full]) }">${str(headers[header_full]).replace(";", ";<br>")}</td>
                % endfor
            </tr>
        % endfor
    </table>
</%def>

${ results(title=title) }

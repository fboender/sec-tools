<%inherit file="master.tpl"/>

<%def name="results(title, heading_offset=0)">
    <h${ heading_offset + 1 }>
    % if title is not None:
        ${ title }
    % else:
        Misconfigurations
    % endif
    </h${ heading_offset + 1 }>

    <p class="description">This is a security scan report of common security
    (and other) misconfigurations.</p>
    <p class="description">Each scan is labeled with a Severity:</p>
    <ul>
        <li><span class="severity severity-0">0</span>: Informational, no security impact.</li>
        <li><span class="severity severity-1">1</span>: Minor</li>
        <li><span class="severity severity-2">2</span>: Low</li>
        <li><span class="severity severity-3">3</span>: Medium</li>
        <li><span class="severity severity-4">4</span>: High</li>
        <li><span class="severity severity-5">5</span>: Severe</li>
        <li><span class="severity severity-error">E</span>: Test not executed due to fatal error.</li>
    </ul>

    <h${ heading_offset + 2 }>Overview</h${ heading_offset + 2 }>
    <table>
    <tr>
        <th>Test name</th>
        <th>Passed?</th>
        <th>Severity</th>
        <th>Description</th>
    </tr>
    % for plugin_name in sorted(data["misconfigs"].keys()):
        <%
        scans = data["misconfigs"][plugin_name]
        %>
        % for test_name in sorted(scans.keys()):
            <%
            result = scans[test_name]
            passed_text = "Failed"
            passed_class="failed"
            if "error" in result:
              passed_text = "Error"
              passed_class = "error"
            elif result['passed'] is True:
              passed_text = "Passed"
              passed_class="passed"
            %>
            <tr>
                <td><a href="#${plugin_name}_${test_name}">${plugin_name}: ${test_name}</a></td>
                <td><span class="${passed_class}">${passed_text}</span></td>
                % if "error" in result:
                    <td><span class="severity severity-error">E</span></td>
                % else:
                    <td><span class="severity severity-${result['severity']}">${result['severity']}</span></td>
                % endif
                <td>${result['desc']}</td>
            </tr>
        % endfor
    % endfor
    </table>

    <h${ heading_offset + 2 }>Details</h${ heading_offset + 2 }>
    % for plugin_name in sorted(data["misconfigs"].keys()):
        <%
        scans = data["misconfigs"][plugin_name]
        %>
        <h3 class="plugin_name">${ plugin_name }</h3>
        % for test_name in sorted(scans.keys()):
            <%
            result = scans[test_name]
            passed_text = "Failed"
            passed_class="failed"
            if "error" in result:
              passed_text = "Error"
              passed_class = "error"
            elif result['passed'] is True:
              passed_text = "Passed"
              passed_class="passed"
            %>
            <table class="test_result">
              <tr class="test_name">
                <th colspan="2"><a name="${plugin_name}_${test_name}">${plugin_name}: ${test_name}</a></th>
              </tr>
              % if "error" in result:
              <tr class="error">
                <th>Fatal error:</th>
                <td>
                <p>${result['error']}</p>
                </td>
              </tr>
              % endif
              <tr class="description">
                <th>Description:</th>
                <td><p>${result['desc']}</p></td>
              </tr>
              <tr class="explanation">
                <th>Explanation:</th>
                <td><p>${result['explanation']}</p></td>
              </tr>
              <tr class="has_passed">
                <th>Passed:</th>
                <td><span class="${passed_class}">${passed_text}</span></td>
              </tr>
              <tr class="severity">
                <th>Severity:</th>
                <td>
                  % if "error" in result:
                      <span class="severity severity-error">E</span>
                  % else:
                      <span class="severity severity-${result['severity']}">${result['severity']}</span>
                  % endif
                </td>
              </tr class="">
              <tr class="">
                <th>Results:</th>
                <td>
                  <ul>
                    % for r in result['results']:
                      <li>${r}</li>
                    % endfor
                  </ul>
                </td>
              </tr>
            </table>
        % endfor
    % endfor
</%def>

${ results(title=title) }

<html>
    <head>
        <title>${title}</title>
        <style>
            /* Custom CSS */
            body { font-family: sans-serif; }
            h2 { margin-top: 64px; }
            p { color: #606060; }

            table { border-collapse: collapse; margin-bottom: 32px; }
            table tr { vertical-align: top; border-bottom: 1px solid #C0C0C0; }
            table tr:last-child { border-bottom: none; }
            table tr th { text-align: left; padding: 8px; background-color: #F0F0F5; }
            table tr td { padding: 8px; }
            table tr td ul { padding-left: 20px; list-style-type: square; margin: 0px; }
            table a { color: #000000; text-decoration-color: #AAAACC; }

            .verified { color: #008000; }
            .unverified { color: #800000; }

            table.test_result { width: 60em; }
            table.test_result .test_name { font-size: large; }

            .passed { color: #008000; }
            .failed { color: #800000; }

            span.severity { padding: 2px 5px 2px 5px; }
            .severity-0 { background-color: #6fffda; color: #000000; }
            .severity-1 { background-color: #fffe6f; color: #000000; }
            .severity-2 { background-color: #ffe31d; color: #000000; }
            .severity-3 { background-color: #ffa900; color: #000000; }
            .severity-4 { background-color: #ff5500; color: #FFFFFF; }
            .severity-5 { background-color: #900000; color: #FFFFFF; }

            /* Account statusses */
            .acc-active { color: #004000; }
            .acc-inactive { color: #A0A0A0; }
            .acc-revoked { color: #800000; }
        </style>
    </head>
    <body>
        <h1>${ title }</h1>

        <h2>Overview</h2>
        <table>
        <tr>
            <th>Test name</th>
            <th>Passed?</th>
            <th>Severity</th>
            <th>Description</th>
        </tr>
        % for plugin_name, scans in data["misconfigs"].items():
            % for test_name, result in scans.items():
                <%
                passed_text = "Failed"
                passed_class="failed"
                if result['passed'] is True:
                  passed_text = "Passed"
                  passed_class="passed"
                elif result['passed'] is None:
                  passed_text = "Error"
                  passed_class = "error"
                %>
                <tr>
                    <td><a href="#${plugin_name}_${test_name}">${plugin_name}: ${test_name}</a></td>
                    <td><span class="${passed_class}">${passed_text}</span></td>
                    <td><span class="severity severity-${result['severity']}">${result['severity']}</span></td>
                    <td>${result['desc']}</td>
                </tr>
            % endfor
        % endfor
        </table>

        <h2>Details</h2>
        % for plugin_name, scans in data["misconfigs"].items():
            <h3 class="plugin_name">${ plugin_name }</h3>
            % for test_name, result in scans.items():
                <%
                passed_text = "Failed"
                passed_class = "failed"
                if result['passed'] is True:
                  passed_text = "Passed"
                  passed_class = "passed"
                elif result['passed'] is None:
                  passed_text = "Error"
                  passed_class = "error"
                  print(passed_text)
                %>
                <table class="test_result">
                  <tr class="test_name">
                    <th colspan="2"><a name="${plugin_name}_${test_name}">${plugin_name}: ${test_name}</a></th>
                  </tr>
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
                    <td><span class="severity severity-${result['severity']}">${result['severity']}</span></td>
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

    </body>
</html>

<%inherit file="master.tpl"/>
<%
import datetime
%>

<%block name="btitle">
    % if title is UNDEFINED or title is None:
      Security scan report for ${ hostname }
    % else:
      ${ title }
    % endif
</%block>

<h1>${ self.btitle() }</h1>
<p>This is a security scan report of common security (and other)
misconfigurations for host <b>${ hostname }</b>. It was generated on ${ datetime.datetime.now().strftime("%Y-%m-%d %H:%M") }</p>
<p>Each scan is labeled with a Severity:</p>
<ul>
    <li><span class="severity severity-0">0</span>: Informational, no security impact.</li>
    <li><span class="severity severity-1">1</span>: Minor</li>
    <li><span class="severity severity-2">2</span>: Low</li>
    <li><span class="severity severity-3">3</span>: Medium</li>
    <li><span class="severity severity-4">4</span>: High</li>
    <li><span class="severity severity-5">5</span>: Severe</li>
</ul>

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

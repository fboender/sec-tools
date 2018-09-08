% SEC-REPORT(1)
% Ferry Boender
% May 2017

# NAME

sec-report – Generate reports

# SYNOPSIS

 **sec-report** [**-h**] [**--version**] [**--debug**] *REPORT* [*ASSETS* [*ASSETS*]]

# DESCRIPTION

**sec-report** is used to generate reports using the Mako templating language.
Information in JSON format (assets) can be fed into the report. The report can
also execute `sec-gather-X` tools to fetch input.

# OPTIONS

**-h**, **--help**
:   Display this help message and exit

**--version**
:   show program's version number and exit

**--debug**
:   Show debug info

**REPORT**
:   Path to Mako template file to render

**ASSET**
:   Path to JSON file to include and send to *REPORT* template

# EXAMPLES

Report templates are written in the Mako templating language. See:

    http://www.makotemplates.org/

A helper function **gather()** is passed to the template, which can be used to
execute **sec-gather-** scripts. For example, a file `report.tpl`:

    <%
    unixusers = gather("./sec-gather-unixusers --login --format html")
    %>
    <h1>Unix users</h1>
    ${unixusers}
    %>

The report would then be rendered to HTML with:

    sec-report report.tpl > report.html

**ASSETS** are JSON files that can be given on the commandline. The contents
of the JSON file is passed to the template and becomes available under the
name of the asset file, as given on the commandline:

    $ sec-gather-unixusers > local_unixusers
    $ ssh example.org sec-gather-unixusers > example_org_unixusers
    $ sec-report report.tpl local_unixusers example_org_unixusers

The template can then access these:

    % for username, userinfo in local_unixusers['unixusers'].items():
        <tr><td>${username}</td><td></td></tr>
    % endfor
    % for username, userinfo in example_org_unixusers['unixusers'].items():
        <tr><td>${username}</td><td></td></tr>
    % endfor

If a '*/*' is present in the path, it will be converted to '*\_\_*' (double
underscores).

# COPYRIGHT

Copyright 2017, Ferry Boender.

Licensed under the MIT license. For more information, see the LICENSE file.

% SEC-GATHER-PERMS(1)
% Ferry Boender
% Feb 2020

# NAME

sec-gather-perms – Output files and dirs with dangerous permissions

# SYNOPSIS

**sec-gather-perms** [**-h**] [**--version**] [**-d**] [**--annotate** *ANNOTATIONFILE*] [**--root** *ROOT*]

# DESCRIPTION

**sec-gather-perms** outputs files and dirs with dangerous permissions.
Currently that means files and directories that are world-writable or with the
setuid bit set.

# OPTIONS

**-h**, **--help**
:   Display this help message and exit

**--version**
:   show program's version number and exit

**-d** / **--debug**
:   Show debug info

# EXAMPLES

Executing:

    $ sec-gather-http-headers https://github.com/ https://gitlab.com/

The default output looks like this:

    {
        "http_headers": {
            "https://github.com/": {
                "Expect-CT": "max-age=2592000, report-uri=\"https://api.github.com/_private/browser/errors\"",
                "Feature-Policy": null,
                "Access-Control-Allow-Origin": null,
                "X-Frame-Options": "deny",
                "Referrer-Policy": "origin-when-cross-origin, strict-origin-when-cross-origin",
                "Access-Control-Allow-Headers": null,
                "X-XSS-Protection": "1; mode=block",
                "Strict-Transport-Security": "max-age=31536000; includeSubdomains; preload",
                "Public-key-pins": null,
                "Content-Security-Policy": "default-src 'none'; base-uri 'self'; block-all-mixed-content; connect-src 'self' uploads.github.com www.githubstatus.com collector.githubapp.com api.github.com www.google-analytics.com github-cloud.s3.amazonaws.com github-production-repository-file-5c1aeb.s3.amazonaws.com github-production-upload-manifest-file-7fdce7.s3.amazonaws.com github-production-user-asset-6210df.s3.amazonaws.com wss://live.github.com; font-src github.githubassets.com; form-action 'self' github.com gist.github.com; frame-ancestors 'none'; frame-src render.githubusercontent.com; img-src 'self' data: github.githubassets.com identicons.github.com collector.githubapp.com github-cloud.s3.amazonaws.com *.githubusercontent.com customer-stories-feed.github.com; manifest-src 'self'; media-src 'none'; script-src github.githubassets.com; style-src 'unsafe-inline' github.githubassets.com",
                "X-Content-Type-Options": "nosniff",
                "Access-Control-Allow-Methods": null
            },
            "https://gitlab.com/": {
                "Expect-CT": null,
                "Feature-Policy": null,
                "Access-Control-Allow-Origin": null,
                "X-Frame-Options": null,
                "Referrer-Policy": null,
                "Access-Control-Allow-Headers": null,
                "X-XSS-Protection": "1; mode=block",
                "Strict-Transport-Security": "max-age=31536000; includeSubdomains",
                "Public-key-pins": null,
                "Content-Security-Policy": "frame-ancestors 'self' https://gitlab.lookbookhq.com https://learn.gitlab.com;",
                "X-Content-Type-Options": "nosniff",
                "Access-Control-Allow-Methods": null
            }
        }
    }

You can use the `reports/sec-gather-http-headers.tpl` report to generate a
HTML matrix overview of URLs and their security headers:

    $ sec-gather-http-headers https://github.com/ https://gitlab.com/ | sec-report reports/sec-gather-http-headers.tpl > header_matrix.html

# COPYRIGHT

Copyright 2017-2019, Ferry Boender.

Licensed under the MIT license. For more information, see the LICENSE file.

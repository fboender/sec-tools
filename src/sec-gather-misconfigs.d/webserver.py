#!/usr/bin/env python

import re
import urllib2
import tools


default_urls = [
    "http://127.0.0.1/",
    "https://127.0.0.1/"
]

request_cache = {}


def _urlopen_cache(url):
    """
    Cache output of urlllib.urlopen.
    """
    if url in request_cache:
        return request_cache[url]
    else:
        req = urllib2.urlopen(url)
        request_cache[url] = req
        return req


def _has_header(urls, header_name, result):
    """
    Check all urls in `urls` for the presence of a certain header and update
    result.
    """
    for url in urls:
        try:
            req = _urlopen_cache(url)
            headers = req.info()
            if header_name.lower() in headers:
                result.add_result("URL {} sent header '{}: {}'".format(url, header_name, headers[header_name]))
            else:
                result.add_result("URL {} did not send header '{}'".format(url, header_name))
                result.passed(False)
        except urllib2.URLError as err:
            result.add_result("Error retrieving {}: {}".format(url, tools.plain_err(err)))

    return result


def version_in_header(urls=None):
    if urls is None:
        urls = default_urls

    result = Result(
        desc="Web server exposes version in 'Server' header.",
        explanation="Exposing a service's version makes it easier to mount attacks against it.",
        severity=1,
        passed=True
    )

    for url in urls:
        try:
            req = _urlopen_cache(url)
            headers = req.info()
            if 'server' in headers:
                result.add_result("URL {} sent header 'Server: {}'".format(url, headers['server']))
                match = re.match(r'.*[0-9]+\..*', headers['server'].lower())
                if match:
                    result.passed(False)
        except urllib2.URLError as err:
            result.add_result("Error retrieving {}: {}".format(url, tools.plain_err(err)))

    return result


def x_frame_options_header(urls=None):
    if urls is None:
        urls = default_urls

    result = Result(
        desc="Web server doesn't specify X-Frame-Options header",
        explanation="X-Frame-Options header can be used to indicate whether or not a browser should be allowed to render a page in a frame.",
        severity=3,
        passed=True
    )

    return _has_header(urls, 'X-Frame-Options', result)


def content_security_policy_header(urls=None):
    if urls is None:
        urls = default_urls

    result = Result(
        desc="Web server doesn't specify Content-Security-Policy header",
        explanation="Content-Security-Policy adds an added layer of security that helps to detect and mitigate certain types of attacks, including Cross Site Scripting (XSS) and data injection attacks.",
        severity=3,
        passed=True
    )

    return _has_header(urls, 'Content-Security-Policy', result)


def strict_transport_security_header(urls=None):
    if urls is None:
        urls = default_urls

    result = Result(
        desc="Web server doesn't specify Strict-Transport-Security header",
        explanation="The strict-transport-security header is a security enhancement that restricts web browsers to access web servers solely over HTTPS. This ensures the connection cannot be establish through an insecure HTTP connection which could be susceptible to attacks.",
        severity=4,
        passed=True
    )

    return _has_header(urls, 'Strict-Transport-Security', result)


def x_content_type_options_header(urls=None):
    if urls is None:
        urls = default_urls

    result = Result(
        desc="Web server doesn't specify X-Content-Type-Options header",
        explanation="The x-content-type header prevents Internet Explorer and Google Chrome from sniffing a response away from the declared content-type. This helps reduce the danger of drive-by downloads and helps treat the content the right way.",
        severity=2,
        passed=True
    )

    return _has_header(urls, 'X-Content-Type-Options', result)

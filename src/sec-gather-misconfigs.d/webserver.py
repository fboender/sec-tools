#!/usr/bin/env python

import re
import ssl
import sys
import urllib.request
import urllib.error


default_urls = [
    "http://127.0.0.1/",
    "https://127.0.0.1/"
]

request_cache = {}


def _url(url, validate_ssl=True, timeout=4):
    if sys.version_info >= (2, 7, 9):
        # Python v2.7.9+ has create_default_context()
        ctx = ssl.create_default_context()
        if validate_ssl is False:
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
        return urllib.request.urlopen(url, context=ctx, timeout=timeout)
    else:
        # Python < v2.7.9 doesn't have create_default_context, but it's okay
        # because it doesn't validate SSL either, which is what we're trying to
        # turn off with the SSL context here.
        return urllib.request.urlopen(url, timeout=timeout)


def _urlopen_cache(url):
    """
    Cache output of urlllib.urlopen. Does not validate SSL.
    """
    if url in request_cache:
        return request_cache[url]
    else:
        req = _url(url, validate_ssl=False, timeout=4)
        request_cache[url] = req
        return req


def _has_header(urls, header_name, result, present=True):
    """
    Check all urls in `urls` for the presence of a certain header and update
    result. If `present` is True, the header should be present. Otherwise, the
    header should be absent.
    """
    for url in urls:
        try:
            req = _urlopen_cache(url)
        except Exception as err:
            raise Exception("{}: {}".format(url, err))
        headers = req.info()
        if header_name.lower() in headers:
            result.add_result("URL {} sent header '{}: {}'".format(url, header_name, headers[header_name]))
            if present is False:
                result.passed(False)
        else:
            result.add_result("URL {} did not send header '{}'".format(url, header_name))
            if present is True:
                result.passed(False)

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
        req = _urlopen_cache(url)
        headers = req.info()
        if 'server' in headers:
            result.add_result("URL {} sent header 'Server: {}'".format(url, headers['server']))
            match = re.match(r'.*[0-9]+\..*', headers['server'].lower())
            if match:
                result.passed(False)

    return result


def powered_by_header(urls=None):
    if urls is None:
        urls = default_urls

    result = Result(
        desc="Web server exposes (X-)Powered-By header",
        explanation="Exposing a service's version makes it easier to mount attacks against it.",
        severity=2,
        passed=True
    )

    _has_header(urls, 'X-Powered-By', result, present=False)
    _has_header(urls, 'Powered-By', result, present=False)
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


def strict_transport_security_header(urls=None):
    if urls is None:
        urls = default_urls

    # Filter out non-https urls
    urls = [
        url for url in urls
        if url.lower().startswith('https')
    ]

    result = Result(
        desc="Web server doesn't specify Strict-Transport-Security header",
        explanation="If a website accepts a connection through HTTP and redirects to HTTPS, visitors may initially communicate with the non-encrypted version of the site before being redirected. This creates an opportunity for a man-in-the-middle attack. The redirect could be exploited to direct visitors to a malicious site instead of the secure version of the original site. The HTTP Strict Transport Security header informs the browser that it should never load a site using HTTP and should automatically convert all attempts to access the site using HTTP to HTTPS requests instead.",
        severity=3,
        passed=True
    )

    return _has_header(urls, 'Strict-Transport-Security', result)


def redirect_to_https(urls=None):
    if urls is None:
        urls = default_urls

    # Filter out https urls
    urls = [
        url for url in urls
        if not url.lower().startswith('https')
    ]

    result = Result(
        desc="Web server does not redirect to https",
        explanation="Non-secure HTTP urls should redirect to a secure version.",
        severity=3,
        passed=False
    )

    class NoRedirection(urllib.request.HTTPErrorProcessor):
        def http_response(self, request, response):
            return response
        https_response = http_response

    opener = urllib.request.build_opener(NoRedirection)

    for url in urls:
        req = urllib.request.Request(url)
        resp = opener.open(req)
        headers = resp.info()

        if 'location' in headers and 'https' in headers['location']:
            result.passed(True)
            result.add_result("{} sent 'location' header: {}".format(url, headers['location']))
        elif re.search('.*refresh.*https', s):
            result.passed(True)
            result.add_result("{} includes <meta> refresh".format(url))

    return result

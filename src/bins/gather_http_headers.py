import sys
import argparse
import ssl
import urllib.request
import urllib.error
import json

import binlink
import common


headers = set([
    "Content-Security-Policy",
    "Strict-Transport-Security",
    "X-Frame-Options",
    "X-XSS-Protection",
    "X-Content-Type-Options",
    "Access-Control-Allow-Origin",
    "Access-Control-Allow-Headers",
    "Access-Control-Allow-Methods",
    "Public-key-pins",
    "Referrer-Policy",
    "Expect-CT",
    "Feature-Policy",
])


def get_url_headers(url):
    ctx = ssl.create_default_context()
    # Turn off SSL validation, because we don't care for headers
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    response = urllib.request.urlopen(url, context=ctx, timeout=4)

    result = {}
    for header in headers:
        result[header] = response.getheader(header)
    return result


def gather(urls):
    results = {}
    for url in urls:
        results[url] = get_url_headers(url)

    return results


@binlink.register("sec-gather-http-headers")
def cmdline(version):
    parser = argparse.ArgumentParser(description='Scan for http security headers on URLs')
    common.arg_add_defaults(parser, version=version)
    parser.add_argument('urls',
                        metavar='urls',
                        type=str,
                        nargs='+',
                        help='Target URLs to scan')
    args = parser.parse_args()
    common.configure_logger(args.debug)

    results = gather(args.urls)
    sys.stdout.write(json.dumps({"http_headers": results}, indent=4))

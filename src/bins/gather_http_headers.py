import sys
import argparse
import ssl
import json
import requests

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
    r = requests.get(url, headers={"User-Agent": "curl/7.58.0"})

    result = {}
    for header in headers:
        result[header] = r.headers.get(header)

    r = requests.options(url, headers={"User-Agent": "curl/7.58.0"})
    for header in headers:
        if header not in result:
            result[header] = r.headers.get(header)

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

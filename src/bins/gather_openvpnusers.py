import sys
import argparse
import json
import logging
import datetime

import binlink
import common


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, datetime.date):
        serial = obj.isoformat()
        return serial
    raise TypeError("{} is not serializable".format(type(obj)))


def parse_subject(subject):
    fields = {}
    for field in subject.split('/'):
        if field != "":
            key, value = field.split("=", 1)
            fields[key] = value
    return fields


def ts_to_datetime(ts):
    if ts == "":
        return ""

    dom = int(ts[0:2].lstrip('0'))
    month = int(ts[2:4].lstrip('0'))
    year = 2000 + int(ts[4:6])
    return(datetime.date(year, month, dom))


def gather(easyrsa_index):
    results = {}
    for line in open(easyrsa_index, 'r').read().splitlines():
        logging.debug(line)
        fields = line.split("\t")
        user = {
            "status": status_fields[fields[0]],
            "valid_until": ts_to_datetime(fields[1]),
            "revoke_ts": ts_to_datetime(fields[2]),
            "serialnr": fields[3],
            "filename": fields[4],
            "subject": parse_subject(fields[5]),
        }
        username = user['subject']['CN']
        results[username] = user

    return results


status_fields = {
    "V": "Valid",
    "R": "Revoked",
    "E": "Expired",
}


@binlink.register("sec-gather-openvpnusers")
def cmdline(version):
    parser = argparse.ArgumentParser(description='Gather unix users')
    common.arg_add_defaults(parser, version=version, annotate=False)
    parser.add_argument('easyrsa_index',
                        metavar='EASYRSA_INDEX',
                        type=str,
                        help='Path to the EasyRSA index.txt')
    args = parser.parse_args()
    common.configure_logger(args.debug)

    results = gather(args.easyrsa_index)
    sys.stdout.write(json.dumps({"openvpnusers": results}, indent=4, default=json_serial))

import os
import sys
import argparse
import logging
import subprocess
import json
from xml.etree import ElementTree as etree

import binlink
import morestd
import common


# -Pn = No host discovery, just assume its online, even if it doesn't respond to ping.
# -oX - = output to XML on stdout
nmap_opts = "-Pn -oX - --script +ssl-enum-ciphers "


def xml_hosts(node_root):
    node_hosts = node_root.findall("host")
    if node_hosts is not None:
        for node_host in node_hosts:
            yield node_host


def xml_host_ports(node_host):
    node_ports = node_host.find("ports")
    if node_ports is not None:
        for node_port in node_ports.findall("port"):
            yield node_port


def xml_port_protos(node_port):
    node_script = node_port.find("script")
    if node_script is not None:
        node_protos = node_script.findall("table")
        if node_protos is not None:
            for node_proto in node_protos:
                yield node_proto


def run_nmap(ip, port, nmap_extra_opts=""):
    """
    Scan <hostname|ip>:port and return XML results in nmap format.

    `ip` is a string containing an IP or hostname, `port` is a string
    containing the range of ports to scan in nmap commandline argument format
    (e.g. "U:53,111,137,T:21-25,80,139,8080,S:9")
    """
    # Build a list of command options
    cmd_opts = [
        "nmap",
        nmap_opts,
        nmap_extra_opts,
        "-p",
        str(port)
    ]
    cmd_opts.append(ip)

    # Execute command
    cmd = " ".join(cmd_opts)
    logging.info("Executing: {}".format(cmd))
    p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    if p.returncode > 0:
        raise Exception("'{}' return exitcode {}. Stderr: {}".format(cmd, p.returncode, stderr))
    else:
        return stdout


def xml_proto(node_table):
    proto = {
        "protocol": node_table.attrib.get("key", "MISSING_PROTOCOL"),
        "ciphers": [],
        "warnings": [],
    }

    for table in node_table.findall("table"):
        table_key = table.attrib.get("key")
        if table_key == "warnings":
            for elem in table.findall("elem"):
                proto["warnings"].append(elem.text)
        elif table_key == "ciphers":
            for cipher_table in table.findall("table"):
                cipher = {}
                for elem in cipher_table.findall("elem"):
                    elem_key = elem.attrib.get("key")
                    elem_value = elem.text
                    cipher[elem_key] = elem_value
                proto["ciphers"].append(cipher)

    return proto


def scan_ip(ip, ports, nmap_extra_opts=""):
    """
    Scan a host or IP's ports for SSL / TLS protocols and ciphers. Returns a
    list of supported protocols, cyphers and security warnings about the
    cyphers per port
    """

    all_port_ssl_details = {}

    for port in ports:
        port_ssl_details = all_port_ssl_details.setdefault(port, [])

        res = run_nmap(ip, port, nmap_extra_opts=nmap_extra_opts)
    #    res = b'''<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE nmaprun>\n<?xml-stylesheet href="file:///usr/bin/../share/nmap/nmap.xsl" type="text/xsl"?>\n<!-- Nmap 7.60 scan initiated Fri Jul 26 08:42:40 2019 as: nmap -Pn -oX - -&#45;script +ssl-enum-ciphers ahldev01.flusso.nl -->\n<nmaprun scanner="nmap" args="nmap -Pn -oX - -&#45;script +ssl-enum-ciphers ahldev01.flusso.nl" start="1564123360" startstr="Fri Jul 26 08:42:40 2019" version="7.60" xmloutputversion="1.04">\n<scaninfo type="connect" protocol="tcp" numservices="1000" services="1,3-4,6-7,9,13,17,19-26,30,32-33,37,42-43,49,53,70,79-85,88-90,99-100,106,109-111,113,119,125,135,139,143-144,146,161,163,179,199,211-212,222,254-256,259,264,280,301,306,311,340,366,389,406-407,416-417,425,427,443-445,458,464-465,481,497,500,512-515,524,541,543-545,548,554-555,563,587,593,616-617,625,631,636,646,648,666-668,683,687,691,700,705,711,714,720,722,726,749,765,777,783,787,800-801,808,843,873,880,888,898,900-903,911-912,981,987,990,992-993,995,999-1002,1007,1009-1011,1021-1100,1102,1104-1108,1110-1114,1117,1119,1121-1124,1126,1130-1132,1137-1138,1141,1145,1147-1149,1151-1152,1154,1163-1166,1169,1174-1175,1183,1185-1187,1192,1198-1199,1201,1213,1216-1218,1233-1234,1236,1244,1247-1248,1259,1271-1272,1277,1287,1296,1300-1301,1309-1311,1322,1328,1334,1352,1417,1433-1434,1443,1455,1461,1494,1500-1501,1503,1521,1524,1533,1556,1580,1583,1594,1600,1641,1658,1666,1687-1688,1700,1717-1721,1723,1755,1761,1782-1783,1801,1805,1812,1839-1840,1862-1864,1875,1900,1914,1935,1947,1971-1972,1974,1984,1998-2010,2013,2020-2022,2030,2033-2035,2038,2040-2043,2045-2049,2065,2068,2099-2100,2103,2105-2107,2111,2119,2121,2126,2135,2144,2160-2161,2170,2179,2190-2191,2196,2200,2222,2251,2260,2288,2301,2323,2366,2381-2383,2393-2394,2399,2401,2492,2500,2522,2525,2557,2601-2602,2604-2605,2607-2608,2638,2701-2702,2710,2717-2718,2725,2800,2809,2811,2869,2875,2909-2910,2920,2967-2968,2998,3000-3001,3003,3005-3007,3011,3013,3017,3030-3031,3052,3071,3077,3128,3168,3211,3221,3260-3261,3268-3269,3283,3300-3301,3306,3322-3325,3333,3351,3367,3369-3372,3389-3390,3404,3476,3493,3517,3527,3546,3551,3580,3659,3689-3690,3703,3737,3766,3784,3800-3801,3809,3814,3826-3828,3851,3869,3871,3878,3880,3889,3905,3914,3918,3920,3945,3971,3986,3995,3998,4000-4006,4045,4111,4125-4126,4129,4224,4242,4279,4321,4343,4443-4446,4449,4550,4567,4662,4848,4899-4900,4998,5000-5004,5009,5030,5033,5050-5051,5054,5060-5061,5080,5087,5100-5102,5120,5190,5200,5214,5221-5222,5225-5226,5269,5280,5298,5357,5405,5414,5431-5432,5440,5500,5510,5544,5550,5555,5560,5566,5631,5633,5666,5678-5679,5718,5730,5800-5802,5810-5811,5815,5822,5825,5850,5859,5862,5877,5900-5904,5906-5907,5910-5911,5915,5922,5925,5950,5952,5959-5963,5987-5989,5998-6007,6009,6025,6059,6100-6101,6106,6112,6123,6129,6156,6346,6389,6502,6510,6543,6547,6565-6567,6580,6646,6666-6669,6689,6692,6699,6779,6788-6789,6792,6839,6881,6901,6969,7000-7002,7004,7007,7019,7025,7070,7100,7103,7106,7200-7201,7402,7435,7443,7496,7512,7625,7627,7676,7741,7777-7778,7800,7911,7920-7921,7937-7938,7999-8002,8007-8011,8021-8022,8031,8042,8045,8080-8090,8093,8099-8100,8180-8181,8192-8194,8200,8222,8254,8290-8292,8300,8333,8383,8400,8402,8443,8500,8600,8649,8651-8652,8654,8701,8800,8873,8888,8899,8994,9000-9003,9009-9011,9040,9050,9071,9080-9081,9090-9091,9099-9103,9110-9111,9200,9207,9220,9290,9415,9418,9485,9500,9502-9503,9535,9575,9593-9595,9618,9666,9876-9878,9898,9900,9917,9929,9943-9944,9968,9998-10004,10009-10010,10012,10024-10025,10082,10180,10215,10243,10566,10616-10617,10621,10626,10628-10629,10778,11110-11111,11967,12000,12174,12265,12345,13456,13722,13782-13783,14000,14238,14441-14442,15000,15002-15004,15660,15742,16000-16001,16012,16016,16018,16080,16113,16992-16993,17877,17988,18040,18101,18988,19101,19283,19315,19350,19780,19801,19842,20000,20005,20031,20221-20222,20828,21571,22939,23502,24444,24800,25734-25735,26214,27000,27352-27353,27355-27356,27715,28201,30000,30718,30951,31038,31337,32768-32785,33354,33899,34571-34573,35500,38292,40193,40911,41511,42510,44176,44442-44443,44501,45100,48080,49152-49161,49163,49165,49167,49175-49176,49400,49999-50003,50006,50300,50389,50500,50636,50800,51103,51493,52673,52822,52848,52869,54045,54328,55055-55056,55555,55600,56737-56738,57294,57797,58080,60020,60443,61532,61900,62078,63331,64623,64680,65000,65129,65389"/>\n<verbose level="0"/>\n<debugging level="0"/>\n<host starttime="1564123360" endtime="1564123389"><status state="up" reason="user-set" reason_ttl="0"/>\n<address addr="88.198.141.188" addrtype="ipv4"/>\n<hostnames>\n<hostname name="ahldev01.flusso.nl" type="user"/>\n<hostname name="ahldev01.flusso.nl" type="PTR"/>\n</hostnames>\n<ports><extraports state="closed" count="997">\n<extrareasons reason="conn-refused" count="997"/>\n</extraports>\n<port protocol="tcp" portid="22"><state state="open" reason="syn-ack" reason_ttl="0"/><service name="ssh" method="table" conf="3"/></port>\n<port protocol="tcp" portid="80"><state state="open" reason="syn-ack" reason_ttl="0"/><service name="http" method="table" conf="3"/></port>\n<port protocol="tcp" portid="443"><state state="open" reason="syn-ack" reason_ttl="0"/><service name="https" method="table" conf="3"/><script id="ssl-enum-ciphers" output="&#xa;  SSLv3: &#xa;    ciphers: &#xa;      TLS_DHE_RSA_WITH_3DES_EDE_CBC_SHA (dh 2048) - C&#xa;      TLS_DHE_RSA_WITH_AES_128_CBC_SHA (dh 2048) - A&#xa;      TLS_DHE_RSA_WITH_AES_256_CBC_SHA (dh 2048) - A&#xa;      TLS_DHE_RSA_WITH_CAMELLIA_128_CBC_SHA (dh 2048) - A&#xa;      TLS_DHE_RSA_WITH_CAMELLIA_256_CBC_SHA (dh 2048) - A&#xa;      TLS_ECDHE_RSA_WITH_3DES_EDE_CBC_SHA (secp256r1) - C&#xa;      TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA (secp256r1) - A&#xa;      TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA (secp256r1) - A&#xa;      TLS_ECDHE_RSA_WITH_RC4_128_SHA (secp256r1) - C&#xa;      TLS_RSA_WITH_3DES_EDE_CBC_SHA (rsa 2048) - C&#xa;      TLS_RSA_WITH_AES_128_CBC_SHA (rsa 2048) - A&#xa;      TLS_RSA_WITH_AES_256_CBC_SHA (rsa 2048) - A&#xa;      TLS_RSA_WITH_CAMELLIA_128_CBC_SHA (rsa 2048) - A&#xa;      TLS_RSA_WITH_CAMELLIA_256_CBC_SHA (rsa 2048) - A&#xa;      TLS_RSA_WITH_RC4_128_SHA (rsa 2048) - C&#xa;    compressors: &#xa;      NULL&#xa;    cipher preference: client&#xa;    warnings: &#xa;      64-bit block cipher 3DES vulnerable to SWEET32 attack&#xa;      Broken cipher RC4 is deprecated by RFC 7465&#xa;      CBC-mode cipher in SSLv3 (CVE-2014-3566)&#xa;  TLSv1.0: &#xa;    ciphers: &#xa;      TLS_DHE_RSA_WITH_3DES_EDE_CBC_SHA (dh 2048) - C&#xa;      TLS_DHE_RSA_WITH_AES_128_CBC_SHA (dh 2048) - A&#xa;      TLS_DHE_RSA_WITH_AES_256_CBC_SHA (dh 2048) - A&#xa;      TLS_DHE_RSA_WITH_CAMELLIA_128_CBC_SHA (dh 2048) - A&#xa;      TLS_DHE_RSA_WITH_CAMELLIA_256_CBC_SHA (dh 2048) - A&#xa;      TLS_ECDHE_RSA_WITH_3DES_EDE_CBC_SHA (secp256k1) - C&#xa;      TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA (secp256k1) - A&#xa;      TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA (secp256k1) - A&#xa;      TLS_ECDHE_RSA_WITH_RC4_128_SHA (secp256k1) - C&#xa;      TLS_RSA_WITH_3DES_EDE_CBC_SHA (rsa 2048) - C&#xa;      TLS_RSA_WITH_AES_128_CBC_SHA (rsa 2048) - A&#xa;      TLS_RSA_WITH_AES_256_CBC_SHA (rsa 2048) - A&#xa;      TLS_RSA_WITH_CAMELLIA_128_CBC_SHA (rsa 2048) - A&#xa;      TLS_RSA_WITH_CAMELLIA_256_CBC_SHA (rsa 2048) - A&#xa;      TLS_RSA_WITH_RC4_128_SHA (rsa 2048) - C&#xa;    compressors: &#xa;      NULL&#xa;    cipher preference: client&#xa;    warnings: &#xa;      64-bit block cipher 3DES vulnerable to SWEET32 attack&#xa;      Broken cipher RC4 is deprecated by RFC 7465&#xa;  TLSv1.1: &#xa;    ciphers: &#xa;      TLS_DHE_RSA_WITH_3DES_EDE_CBC_SHA (dh 2048) - C&#xa;      TLS_DHE_RSA_WITH_AES_128_CBC_SHA (dh 2048) - A&#xa;      TLS_DHE_RSA_WITH_AES_256_CBC_SHA (dh 2048) - A&#xa;      TLS_DHE_RSA_WITH_CAMELLIA_128_CBC_SHA (dh 2048) - A&#xa;      TLS_DHE_RSA_WITH_CAMELLIA_256_CBC_SHA (dh 2048) - A&#xa;      TLS_ECDHE_RSA_WITH_3DES_EDE_CBC_SHA (secp256k1) - C&#xa;      TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA (secp256k1) - A&#xa;      TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA (secp256k1) - A&#xa;      TLS_ECDHE_RSA_WITH_RC4_128_SHA (secp256k1) - C&#xa;      TLS_RSA_WITH_3DES_EDE_CBC_SHA (rsa 2048) - C&#xa;      TLS_RSA_WITH_AES_128_CBC_SHA (rsa 2048) - A&#xa;      TLS_RSA_WITH_AES_256_CBC_SHA (rsa 2048) - A&#xa;      TLS_RSA_WITH_CAMELLIA_128_CBC_SHA (rsa 2048) - A&#xa;      TLS_RSA_WITH_CAMELLIA_256_CBC_SHA (rsa 2048) - A&#xa;      TLS_RSA_WITH_RC4_128_SHA (rsa 2048) - C&#xa;    compressors: &#xa;      NULL&#xa;    cipher preference: client&#xa;    warnings: &#xa;      64-bit block cipher 3DES vulnerable to SWEET32 attack&#xa;      Broken cipher RC4 is deprecated by RFC 7465&#xa;  TLSv1.2: &#xa;    ciphers: &#xa;      TLS_DHE_RSA_WITH_3DES_EDE_CBC_SHA (dh 2048) - C&#xa;      TLS_DHE_RSA_WITH_AES_128_CBC_SHA (dh 2048) - A&#xa;      TLS_DHE_RSA_WITH_AES_128_CBC_SHA256 (dh 2048) - A&#xa;      TLS_DHE_RSA_WITH_AES_128_GCM_SHA256 (dh 2048) - A&#xa;      TLS_DHE_RSA_WITH_AES_256_CBC_SHA (dh 2048) - A&#xa;      TLS_DHE_RSA_WITH_AES_256_CBC_SHA256 (dh 2048) - A&#xa;      TLS_DHE_RSA_WITH_AES_256_GCM_SHA384 (dh 2048) - A&#xa;      TLS_DHE_RSA_WITH_CAMELLIA_128_CBC_SHA (dh 2048) - A&#xa;      TLS_DHE_RSA_WITH_CAMELLIA_256_CBC_SHA (dh 2048) - A&#xa;      TLS_ECDHE_RSA_WITH_3DES_EDE_CBC_SHA (secp256k1) - C&#xa;      TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA (secp256k1) - A&#xa;      TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256 (secp256k1) - A&#xa;      TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256 (secp256k1) - A&#xa;      TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA (secp256k1) - A&#xa;      TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA384 (secp256k1) - A&#xa;      TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384 (secp256k1) - A&#xa;      TLS_ECDHE_RSA_WITH_RC4_128_SHA (secp256k1) - C&#xa;      TLS_RSA_WITH_3DES_EDE_CBC_SHA (rsa 2048) - C&#xa;      TLS_RSA_WITH_AES_128_CBC_SHA (rsa 2048) - A&#xa;      TLS_RSA_WITH_AES_128_CBC_SHA256 (rsa 2048) - A&#xa;      TLS_RSA_WITH_AES_128_GCM_SHA256 (rsa 2048) - A&#xa;      TLS_RSA_WITH_AES_256_CBC_SHA (rsa 2048) - A&#xa;      TLS_RSA_WITH_AES_256_CBC_SHA256 (rsa 2048) - A&#xa;      TLS_RSA_WITH_AES_256_GCM_SHA384 (rsa 2048) - A&#xa;      TLS_RSA_WITH_CAMELLIA_128_CBC_SHA (rsa 2048) - A&#xa;      TLS_RSA_WITH_CAMELLIA_256_CBC_SHA (rsa 2048) - A&#xa;      TLS_RSA_WITH_RC4_128_SHA (rsa 2048) - C&#xa;    compressors: &#xa;      NULL&#xa;    cipher preference: client&#xa;    warnings: &#xa;      64-bit block cipher 3DES vulnerable to SWEET32 attack&#xa;      Broken cipher RC4 is deprecated by RFC 7465&#xa;  least strength: C"><table key="SSLv3">\n<table key="ciphers">\n<table>\n<elem key="name">TLS_DHE_RSA_WITH_3DES_EDE_CBC_SHA</elem>\n<elem key="kex_info">dh 2048</elem>\n<elem key="strength">C</elem>\n</table>\n<table>\n<elem key="name">TLS_DHE_RSA_WITH_AES_128_CBC_SHA</elem>\n<elem key="kex_info">dh 2048</elem>\n<elem key="strength">A</elem>\n</table>\n<table>\n<elem key="name">TLS_DHE_RSA_WITH_AES_256_CBC_SHA</elem>\n<elem key="kex_info">dh 2048</elem>\n<elem key="strength">A</elem>\n</table>\n<table>\n<elem key="name">TLS_DHE_RSA_WITH_CAMELLIA_128_CBC_SHA</elem>\n<elem key="kex_info">dh 2048</elem>\n<elem key="strength">A</elem>\n</table>\n<table>\n<elem key="name">TLS_DHE_RSA_WITH_CAMELLIA_256_CBC_SHA</elem>\n<elem key="kex_info">dh 2048</elem>\n<elem key="strength">A</elem>\n</table>\n<table>\n<elem key="name">TLS_ECDHE_RSA_WITH_3DES_EDE_CBC_SHA</elem>\n<elem key="kex_info">secp256r1</elem>\n<elem key="strength">C</elem>\n</table>\n<table>\n<elem key="name">TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA</elem>\n<elem key="kex_info">secp256r1</elem>\n<elem key="strength">A</elem>\n</table>\n<table>\n<elem key="name">TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA</elem>\n<elem key="kex_info">secp256r1</elem>\n<elem key="strength">A</elem>\n</table>\n<table>\n<elem key="name">TLS_ECDHE_RSA_WITH_RC4_128_SHA</elem>\n<elem key="kex_info">secp256r1</elem>\n<elem key="strength">C</elem>\n</table>\n<table>\n<elem key="name">TLS_RSA_WITH_3DES_EDE_CBC_SHA</elem>\n<elem key="kex_info">rsa 2048</elem>\n<elem key="strength">C</elem>\n</table>\n<table>\n<elem key="name">TLS_RSA_WITH_AES_128_CBC_SHA</elem>\n<elem key="kex_info">rsa 2048</elem>\n<elem key="strength">A</elem>\n</table>\n<table>\n<elem key="name">TLS_RSA_WITH_AES_256_CBC_SHA</elem>\n<elem key="kex_info">rsa 2048</elem>\n<elem key="strength">A</elem>\n</table>\n<table>\n<elem key="name">TLS_RSA_WITH_CAMELLIA_128_CBC_SHA</elem>\n<elem key="kex_info">rsa 2048</elem>\n<elem key="strength">A</elem>\n</table>\n<table>\n<elem key="name">TLS_RSA_WITH_CAMELLIA_256_CBC_SHA</elem>\n<elem key="kex_info">rsa 2048</elem>\n<elem key="strength">A</elem>\n</table>\n<table>\n<elem key="name">TLS_RSA_WITH_RC4_128_SHA</elem>\n<elem key="kex_info">rsa 2048</elem>\n<elem key="strength">C</elem>\n</table>\n</table>\n<table key="compressors">\n<elem>NULL</elem>\n</table>\n<elem key="cipher preference">client</elem>\n<table key="warnings">\n<elem>64-bit block cipher 3DES vulnerable to SWEET32 attack</elem>\n<elem>Broken cipher RC4 is deprecated by RFC 7465</elem>\n<elem>CBC-mode cipher in SSLv3 (CVE-2014-3566)</elem>\n</table>\n</table>\n<table key="TLSv1.0">\n<table key="ciphers">\n<table>\n<elem key="name">TLS_DHE_RSA_WITH_3DES_EDE_CBC_SHA</elem>\n<elem key="kex_info">dh 2048</elem>\n<elem key="strength">C</elem>\n</table>\n<table>\n<elem key="name">TLS_DHE_RSA_WITH_AES_128_CBC_SHA</elem>\n<elem key="kex_info">dh 2048</elem>\n<elem key="strength">A</elem>\n</table>\n<table>\n<elem key="name">TLS_DHE_RSA_WITH_AES_256_CBC_SHA</elem>\n<elem key="kex_info">dh 2048</elem>\n<elem key="strength">A</elem>\n</table>\n<table>\n<elem key="name">TLS_DHE_RSA_WITH_CAMELLIA_128_CBC_SHA</elem>\n<elem key="kex_info">dh 2048</elem>\n<elem key="strength">A</elem>\n</table>\n<table>\n<elem key="name">TLS_DHE_RSA_WITH_CAMELLIA_256_CBC_SHA</elem>\n<elem key="kex_info">dh 2048</elem>\n<elem key="strength">A</elem>\n</table>\n<table>\n<elem key="name">TLS_ECDHE_RSA_WITH_3DES_EDE_CBC_SHA</elem>\n<elem key="kex_info">secp256k1</elem>\n<elem key="strength">C</elem>\n</table>\n<table>\n<elem key="name">TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA</elem>\n<elem key="kex_info">secp256k1</elem>\n<elem key="strength">A</elem>\n</table>\n<table>\n<elem key="name">TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA</elem>\n<elem key="kex_info">secp256k1</elem>\n<elem key="strength">A</elem>\n</table>\n<table>\n<elem key="name">TLS_ECDHE_RSA_WITH_RC4_128_SHA</elem>\n<elem key="kex_info">secp256k1</elem>\n<elem key="strength">C</elem>\n</table>\n<table>\n<elem key="name">TLS_RSA_WITH_3DES_EDE_CBC_SHA</elem>\n<elem key="kex_info">rsa 2048</elem>\n<elem key="strength">C</elem>\n</table>\n<table>\n<elem key="name">TLS_RSA_WITH_AES_128_CBC_SHA</elem>\n<elem key="kex_info">rsa 2048</elem>\n<elem key="strength">A</elem>\n</table>\n<table>\n<elem key="name">TLS_RSA_WITH_AES_256_CBC_SHA</elem>\n<elem key="kex_info">rsa 2048</elem>\n<elem key="strength">A</elem>\n</table>\n<table>\n<elem key="name">TLS_RSA_WITH_CAMELLIA_128_CBC_SHA</elem>\n<elem key="kex_info">rsa 2048</elem>\n<elem key="strength">A</elem>\n</table>\n<table>\n<elem key="name">TLS_RSA_WITH_CAMELLIA_256_CBC_SHA</elem>\n<elem key="kex_info">rsa 2048</elem>\n<elem key="strength">A</elem>\n</table>\n<table>\n<elem key="name">TLS_RSA_WITH_RC4_128_SHA</elem>\n<elem key="kex_info">rsa 2048</elem>\n<elem key="strength">C</elem>\n</table>\n</table>\n<table key="compressors">\n<elem>NULL</elem>\n</table>\n<elem key="cipher preference">client</elem>\n<table key="warnings">\n<elem>64-bit block cipher 3DES vulnerable to SWEET32 attack</elem>\n<elem>Broken cipher RC4 is deprecated by RFC 7465</elem>\n</table>\n</table>\n<table key="TLSv1.1">\n<table key="ciphers">\n<table>\n<elem key="name">TLS_DHE_RSA_WITH_3DES_EDE_CBC_SHA</elem>\n<elem key="kex_info">dh 2048</elem>\n<elem key="strength">C</elem>\n</table>\n<table>\n<elem key="name">TLS_DHE_RSA_WITH_AES_128_CBC_SHA</elem>\n<elem key="kex_info">dh 2048</elem>\n<elem key="strength">A</elem>\n</table>\n<table>\n<elem key="name">TLS_DHE_RSA_WITH_AES_256_CBC_SHA</elem>\n<elem key="kex_info">dh 2048</elem>\n<elem key="strength">A</elem>\n</table>\n<table>\n<elem key="name">TLS_DHE_RSA_WITH_CAMELLIA_128_CBC_SHA</elem>\n<elem key="kex_info">dh 2048</elem>\n<elem key="strength">A</elem>\n</table>\n<table>\n<elem key="name">TLS_DHE_RSA_WITH_CAMELLIA_256_CBC_SHA</elem>\n<elem key="kex_info">dh 2048</elem>\n<elem key="strength">A</elem>\n</table>\n<table>\n<elem key="name">TLS_ECDHE_RSA_WITH_3DES_EDE_CBC_SHA</elem>\n<elem key="kex_info">secp256k1</elem>\n<elem key="strength">C</elem>\n</table>\n<table>\n<elem key="name">TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA</elem>\n<elem key="kex_info">secp256k1</elem>\n<elem key="strength">A</elem>\n</table>\n<table>\n<elem key="name">TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA</elem>\n<elem key="kex_info">secp256k1</elem>\n<elem key="strength">A</elem>\n</table>\n<table>\n<elem key="name">TLS_ECDHE_RSA_WITH_RC4_128_SHA</elem>\n<elem key="kex_info">secp256k1</elem>\n<elem key="strength">C</elem>\n</table>\n<table>\n<elem key="name">TLS_RSA_WITH_3DES_EDE_CBC_SHA</elem>\n<elem key="kex_info">rsa 2048</elem>\n<elem key="strength">C</elem>\n</table>\n<table>\n<elem key="name">TLS_RSA_WITH_AES_128_CBC_SHA</elem>\n<elem key="kex_info">rsa 2048</elem>\n<elem key="strength">A</elem>\n</table>\n<table>\n<elem key="name">TLS_RSA_WITH_AES_256_CBC_SHA</elem>\n<elem key="kex_info">rsa 2048</elem>\n<elem key="strength">A</elem>\n</table>\n<table>\n<elem key="name">TLS_RSA_WITH_CAMELLIA_128_CBC_SHA</elem>\n<elem key="kex_info">rsa 2048</elem>\n<elem key="strength">A</elem>\n</table>\n<table>\n<elem key="name">TLS_RSA_WITH_CAMELLIA_256_CBC_SHA</elem>\n<elem key="kex_info">rsa 2048</elem>\n<elem key="strength">A</elem>\n</table>\n<table>\n<elem key="name">TLS_RSA_WITH_RC4_128_SHA</elem>\n<elem key="kex_info">rsa 2048</elem>\n<elem key="strength">C</elem>\n</table>\n</table>\n<table key="compressors">\n<elem>NULL</elem>\n</table>\n<elem key="cipher preference">client</elem>\n<table key="warnings">\n<elem>64-bit block cipher 3DES vulnerable to SWEET32 attack</elem>\n<elem>Broken cipher RC4 is deprecated by RFC 7465</elem>\n</table>\n</table>\n<table key="TLSv1.2">\n<table key="ciphers">\n<table>\n<elem key="name">TLS_DHE_RSA_WITH_3DES_EDE_CBC_SHA</elem>\n<elem key="kex_info">dh 2048</elem>\n<elem key="strength">C</elem>\n</table>\n<table>\n<elem key="name">TLS_DHE_RSA_WITH_AES_128_CBC_SHA</elem>\n<elem key="kex_info">dh 2048</elem>\n<elem key="strength">A</elem>\n</table>\n<table>\n<elem key="name">TLS_DHE_RSA_WITH_AES_128_CBC_SHA256</elem>\n<elem key="kex_info">dh 2048</elem>\n<elem key="strength">A</elem>\n</table>\n<table>\n<elem key="name">TLS_DHE_RSA_WITH_AES_128_GCM_SHA256</elem>\n<elem key="kex_info">dh 2048</elem>\n<elem key="strength">A</elem>\n</table>\n<table>\n<elem key="name">TLS_DHE_RSA_WITH_AES_256_CBC_SHA</elem>\n<elem key="kex_info">dh 2048</elem>\n<elem key="strength">A</elem>\n</table>\n<table>\n<elem key="name">TLS_DHE_RSA_WITH_AES_256_CBC_SHA256</elem>\n<elem key="kex_info">dh 2048</elem>\n<elem key="strength">A</elem>\n</table>\n<table>\n<elem key="name">TLS_DHE_RSA_WITH_AES_256_GCM_SHA384</elem>\n<elem key="kex_info">dh 2048</elem>\n<elem key="strength">A</elem>\n</table>\n<table>\n<elem key="name">TLS_DHE_RSA_WITH_CAMELLIA_128_CBC_SHA</elem>\n<elem key="kex_info">dh 2048</elem>\n<elem key="strength">A</elem>\n</table>\n<table>\n<elem key="name">TLS_DHE_RSA_WITH_CAMELLIA_256_CBC_SHA</elem>\n<elem key="kex_info">dh 2048</elem>\n<elem key="strength">A</elem>\n</table>\n<table>\n<elem key="name">TLS_ECDHE_RSA_WITH_3DES_EDE_CBC_SHA</elem>\n<elem key="kex_info">secp256k1</elem>\n<elem key="strength">C</elem>\n</table>\n<table>\n<elem key="name">TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA</elem>\n<elem key="kex_info">secp256k1</elem>\n<elem key="strength">A</elem>\n</table>\n<table>\n<elem key="name">TLS_ECDHE_RSA_WITH_AES_128_CBC_SHA256</elem>\n<elem key="kex_info">secp256k1</elem>\n<elem key="strength">A</elem>\n</table>\n<table>\n<elem key="name">TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256</elem>\n<elem key="kex_info">secp256k1</elem>\n<elem key="strength">A</elem>\n</table>\n<table>\n<elem key="name">TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA</elem>\n<elem key="kex_info">secp256k1</elem>\n<elem key="strength">A</elem>\n</table>\n<table>\n<elem key="name">TLS_ECDHE_RSA_WITH_AES_256_CBC_SHA384</elem>\n<elem key="kex_info">secp256k1</elem>\n<elem key="strength">A</elem>\n</table>\n<table>\n<elem key="name">TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384</elem>\n<elem key="kex_info">secp256k1</elem>\n<elem key="strength">A</elem>\n</table>\n<table>\n<elem key="name">TLS_ECDHE_RSA_WITH_RC4_128_SHA</elem>\n<elem key="kex_info">secp256k1</elem>\n<elem key="strength">C</elem>\n</table>\n<table>\n<elem key="name">TLS_RSA_WITH_3DES_EDE_CBC_SHA</elem>\n<elem key="kex_info">rsa 2048</elem>\n<elem key="strength">C</elem>\n</table>\n<table>\n<elem key="name">TLS_RSA_WITH_AES_128_CBC_SHA</elem>\n<elem key="kex_info">rsa 2048</elem>\n<elem key="strength">A</elem>\n</table>\n<table>\n<elem key="name">TLS_RSA_WITH_AES_128_CBC_SHA256</elem>\n<elem key="kex_info">rsa 2048</elem>\n<elem key="strength">A</elem>\n</table>\n<table>\n<elem key="name">TLS_RSA_WITH_AES_128_GCM_SHA256</elem>\n<elem key="kex_info">rsa 2048</elem>\n<elem key="strength">A</elem>\n</table>\n<table>\n<elem key="name">TLS_RSA_WITH_AES_256_CBC_SHA</elem>\n<elem key="kex_info">rsa 2048</elem>\n<elem key="strength">A</elem>\n</table>\n<table>\n<elem key="name">TLS_RSA_WITH_AES_256_CBC_SHA256</elem>\n<elem key="kex_info">rsa 2048</elem>\n<elem key="strength">A</elem>\n</table>\n<table>\n<elem key="name">TLS_RSA_WITH_AES_256_GCM_SHA384</elem>\n<elem key="kex_info">rsa 2048</elem>\n<elem key="strength">A</elem>\n</table>\n<table>\n<elem key="name">TLS_RSA_WITH_CAMELLIA_128_CBC_SHA</elem>\n<elem key="kex_info">rsa 2048</elem>\n<elem key="strength">A</elem>\n</table>\n<table>\n<elem key="name">TLS_RSA_WITH_CAMELLIA_256_CBC_SHA</elem>\n<elem key="kex_info">rsa 2048</elem>\n<elem key="strength">A</elem>\n</table>\n<table>\n<elem key="name">TLS_RSA_WITH_RC4_128_SHA</elem>\n<elem key="kex_info">rsa 2048</elem>\n<elem key="strength">C</elem>\n</table>\n</table>\n<table key="compressors">\n<elem>NULL</elem>\n</table>\n<elem key="cipher preference">client</elem>\n<table key="warnings">\n<elem>64-bit block cipher 3DES vulnerable to SWEET32 attack</elem>\n<elem>Broken cipher RC4 is deprecated by RFC 7465</elem>\n</table>\n</table>\n<elem key="least strength">C</elem>\n</script></port>\n</ports>\n<times srtt="36852" rttvar="964" to="100000"/>\n</host>\n<runstats><finished time="1564123389" timestr="Fri Jul 26 08:43:09 2019" elapsed="28.52" summary="Nmap done at Fri Jul 26 08:43:09 2019; 1 IP address (1 host up) scanned in 28.52 seconds" exit="success"/><hosts up="1" down="0" total="1"/>\n</runstats>\n</nmaprun>\n'''

        logging.debug("nmap XML output: {}".format(res))
        xml = etree.XML(res)
        node_root = xml
        node_hosts = node_root.findall("host")

        for host in xml_hosts(node_root):
            for port in xml_host_ports(host):
                for port_proto in xml_port_protos(port):
                    port_ssl_details.append(xml_proto(port_proto))

    return all_port_ssl_details


def gather(targets, ports, annotate=None):
    annotations = {}
    if annotate is not None:
        annotations = json.load(open(annotate, 'r'))

    results = {}
    for target in targets:
        result_hosts = scan_ip(target, ports=ports)
        results.update(result_hosts)

        if target in annotations:
            morestd.data.deepupdate(results[target], annotations[target])

    return results


@binlink.register("sec-gather-sslscan")
def cmdline(version):
    parser = argparse.ArgumentParser(description='Scan for open ports on machine')
    common.arg_add_defaults(parser, version=version, annotate=True)
    parser.add_argument('--ports',
                        dest="ports",
                        type=str,
                        default=[443],
                        help="Port(s) to scan (nmap format)")
    parser.add_argument('targets',
                        metavar='target',
                        type=str,
                        nargs='+',
                        help='Target(s) to scan')
    args = parser.parse_args()
    common.configure_logger(args.debug)

    if args.targets is None:
        sys.stderr.write("Please specify one or more targets\n")
        sys.exit(1)

    results = gather(args.targets, args.ports, args.annotate)
    sys.stdout.write(json.dumps({"portprotos": results}, indent=4))

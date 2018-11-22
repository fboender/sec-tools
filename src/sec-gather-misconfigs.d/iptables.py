import tools
import common


def input_policy_drop():
    result = Result(
        desc="Default policy for INPUT rule is not DROP or DENY",
        explanation="The default INPUT policy should be to drop "
                    "traffic, and explicitly whitelist traffic that is "
                    "allowed.",
        severity=5,
        passed=False
    )

    output = tools.cmd('iptables-save')['stdout']
    iptables = common.IptablesParser(output).parse()

    if iptables["filter"]["INPUT"]["policy"] in ("DROP", "DENY"):
        result.passed(True)
        result.add_result("filter:INPUT default policy is DROP or DENY")

    return result


def forward_policy_drop():
    result = Result(
        desc="Default policy for FORWARD rule is not DROP or DENY",
        explanation="The default FORWARD policy should be to drop "
                    "traffic, and explicitly whitelist traffic that is "
                    "allowed to be forwarded.",
        severity=4,
        passed=False
    )

    output = tools.cmd('iptables-save')['stdout']
    iptables = common.IptablesParser(output).parse()

    if iptables["filter"]["FORWARD"]["policy"] in ("DROP", "DENY"):
        result.passed(True)
        result.add_result("filter:FORWARD default policy is DROP or DENY")

    return result

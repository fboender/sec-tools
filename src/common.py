"""
Functionality that's common or shared amongst multiple tools.
"""

class IptablesParser:
    """
    Parse the output of `iptables-save` and return as Python data structure.
    """
    def __init__(self, iptables):
        self.iptables = iptables
        self.parsed = {}
        self._cur_table = None
        self._cur_chain = None

    def parse(self):
        for line in [line.strip() for line in self.iptables.splitlines()]:
            if line.startswith('#'):
                continue
            elif line.startswith('*'):
                self._parse_line_table(line)
            elif line.startswith(':'):
                self._parse_line_chain(line)
            elif line.startswith('-A '):
                self._parse_line_rule(line)
        return self.parsed

    def _parse_line_table(self, line):
        table_name = line[1:]
        self._cur_table = self.parsed.setdefault(table_name, {})

    def _parse_line_chain(self, line):
        line_parts = line.split(' ', 2)[0:2]
        chain_name = line_parts[0][1:]
        chain_policy = line_parts[1]

        self._cur_chain = {
            "policy": chain_policy,
            "rules": []
        }
        self._cur_table.setdefault(chain_name, self._cur_chain)

    def _parse_line_rule(self, line):
        tokens = line.split()
        cur_rule = {}
        cur_not = "{}"
        while tokens:
            token = tokens.pop(0)
            if token == "!":
                cur_not = "NOT {}"
            elif token == "-A":
                cur_rule["chain"] = cur_not.format(tokens.pop(0))
                cur_not = "{}"
            elif token == '-i':
                cur_rule["interface"] = cur_not.format(tokens.pop(0))
                cur_not = "{}"
            elif token == '-m':
                cur_rule["match"] = cur_not.format(tokens.pop(0))
                cur_not = "{}"
            elif token == '--state':
                cur_rule["state"] = cur_not.format(tokens.pop(0))
                cur_not = "{}"
            elif token == '-p':
                cur_rule["proto"] = cur_not.format(tokens.pop(0))
                cur_not = "{}"
            elif token == '--dst-type':
                cur_rule["dst_type"] = cur_not.format(tokens.pop(0))
                cur_not = "{}"
            elif token == "-s":
                cur_rule["src"] = cur_not.format(tokens.pop(0))
                cur_not = "{}"
            elif token == "-d":
                cur_rule["dest"] = cur_not.format(tokens.pop(0))
                cur_not = "{}"
            elif token == "--dport":
                cur_rule["dest_port"] = cur_not.format(tokens.pop(0))
                cur_not = "{}"
            elif token == "-j":
                cur_rule["jump"] = cur_not.format(tokens.pop(0))
                cur_not = "{}"
        self._cur_table[cur_rule["chain"]]["rules"].append(cur_rule)


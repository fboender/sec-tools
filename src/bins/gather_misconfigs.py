import sys
import argparse
import logging
import json
import os
import imp
import inspect
import ast
import fnmatch
import textwrap

import binlink
import tools
import common
import morestd
import misconfig_scanners


class Result:
    def __init__(self, desc, explanation, severity, passed=False):
        self.desc = desc
        self.explanation = self._normalize_explanation(explanation)
        self.severity = severity
        self.has_passed = passed
        self.results = []
        self.error = None
        self.scanner_name = None
        self.test_name = None

        assert(severity >= 0 and severity <= 5)

    def _normalize_explanation(self, explanation):
        return textwrap.dedent(explanation).strip().replace("\n", " ")

    def passed(self, passed=True):
        self.has_passed = passed

    def add_result(self, result):
        self.results.append(result)

    def set_error(self, error):
        self.error = error

    def set_scanner_name(self, scanner_name):
        self.scanner_name = scanner_name

    def set_test_name(self, test_name):
        self.test_name = test_name

    def to_dict(self):
        res = {
            self.scanner_name: {
                self.test_name: {
                    "desc": self.desc,
                    "explanation": self.explanation,
                    "severity": self.severity,
                    "passed": self.has_passed,
                    "results": self.results,
                }
            }
        }

        if self.error is not None:
            res[self.scanner_name][self.test_name]['error'] = self.error

        return res


def load_scanners(debug=False):
    """
    Go through all the modules in the `misconfig_scanners` package and find all
    functions in them that implement a scanner.
    """
    scanners = {}

    for module_name, module in inspect.getmembers(misconfig_scanners, inspect.ismodule):
        # Monkey-patch the Result class into the module namespace. This is ugly.
        module.Result = Result

        for func_name, func_cb in inspect.getmembers(module, inspect.isfunction):
            if not func_name.startswith('_'):
                logging.info("Found scan {}:{}".format(module_name, func_name))
                scanners.setdefault(module_name, []).append(func_cb)

    return scanners


def gather(config, skip_passed, limit, debug):
    scanners = load_scanners(debug=debug)

    results = {}
    for scanner_name in scanners.keys():
        for scanner_cb in scanners[scanner_name]:
            test_name = scanner_cb.__name__
            full_name = '{}:{}'.format(scanner_name, test_name)

            # Skip tests if not in limit. Can use wildcards such as 'net:*'
            if limit is not None:
                for match in limit:
                    if fnmatch.fnmatch(full_name, match):
                        # Test name found
                        break
                else:
                    # Test name not found
                    logging.debug("Skipping test '{}' due to limit".format(full_name))
                    continue

            # Apply test configuration
            test_config = {}
            if scanner_name in config:
                if '_all' in config[scanner_name]:
                    test_config.update(config[scanner_name]['_all'])
                if test_name in config[scanner_name]:
                    test_config.update(config[scanner_name][test_name])

            # Execute test
            logging.info("Executing test {}:{}".format(scanner_name, test_name))
            logging.debug("{}:{} config: {}".format(scanner_name, test_name, test_config))
            try:
                result = scanner_cb(**test_config)
                assert isinstance(result, Result)
                result.set_scanner_name(scanner_name)
                result.set_test_name(test_name)

                # Update all results with this result
                if result.has_passed is False or skip_passed is False:
                    morestd.data.deepupdate(results, result.to_dict())
            except Exception as err:
                sys.stderr.write("Error executing test '{}:{}': {}: {}\n".format(scanner_name, test_name, type(err), err))
                if debug is True:
                    logging.exception(err)

                # Create Error result.
                result = Result(desc="", explanation="", severity=0, passed=None)
                result.set_scanner_name(scanner_name)
                result.set_test_name(test_name)
                result.set_error(tools.plain_err(err))
                morestd.data.deepupdate(results, result.to_dict())

    return results


@binlink.register("sec-gather-misconfigs")
def cmdline(version):
    parser = argparse.ArgumentParser(description='Gather misconfigurations')
    common.arg_add_defaults(parser, version=version, annotate=False)
    parser.add_argument('--skip-passed',
                        dest='skip_passed',
                        action='store_true',
                        default=False,
                        help="Don't include passed tests")
    parser.add_argument('--config',
                        dest='config',
                        action='store',
                        type=str,
                        default=None,
                        help='Configuration file for tests')
    parser.add_argument('--limit',
                        dest='limit',
                        action='store',
                        type=str,
                        default=None,
                        help='Limit which tests are executed')
    args = parser.parse_args()
    common.configure_logger(args.debug)

    # Parse limit
    if args.limit is not None:
        args.limit = args.limit.split(',')

    # Read configuration
    config = {}
    if args.config is not None:
        logging.info("Reading config {}".format(args.config))
        config = ast.literal_eval(open(args.config, 'r').read())

    # Run tests
    results = gather(config=config,
                     skip_passed=args.skip_passed,
                     limit=args.limit,
                     debug=args.debug)
    sys.stdout.write(json.dumps({"misconfigs": results}, indent=4))

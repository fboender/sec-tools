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


class Result:
    def __init__(self, desc, explanation, severity, passed=False):
        self.desc = desc
        self.explanation = self._normalize_explanation(explanation)
        self.severity = severity
        self.has_passed = passed
        self.results = []
        self.error = None
        self.plugin_name = None
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

    def set_plugin_name(self, plugin_name):
        self.plugin_name = plugin_name

    def set_test_name(self, test_name):
        self.test_name = test_name

    def to_dict(self):
        res = {
            self.plugin_name: {
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
            res[self.plugin_name][self.test_name]['error'] = self.error

        return res


def load_plugins(debug=False):
    plugins = {}
    plugin_dir = os.path.join(tools.abs_real_dir(sys.argv[0]),
                              'sec-gather-misconfigs.d')
    logging.info("Loading plugins from {}".format(plugin_dir))
    for fname in os.listdir(plugin_dir):
        fname_parts = os.path.splitext(fname)
        plugin_name = fname_parts[0]
        if fname_parts[1] == ".py":
            # Load and execute Python code
            logging.info("Loading plugin {}".format(plugin_name))
            path = os.path.join(plugin_dir, fname)
            try:
                module = imp.load_source(plugin_name, path)
                module.Result = Result
            except Exception as err:
                logging.error("Couldn't import plugin '{}': {}".format(plugin_name, err))
                if debug is True:
                    logging.exception(err)
                raise

            for func_name, func_cb in inspect.getmembers(module, inspect.isfunction):
                if not func_name.startswith('_'):
                    logging.info("Found scan {}:{}".format(plugin_name, func_name))
                    plugins.setdefault(plugin_name, []).append(func_cb)
        else:
            logging.info("Skipping {}".format(fname))

    return plugins


def gather(config, skip_passed, limit, debug):
    plugins = load_plugins(debug=debug)

    results = {}
    for plugin_name in plugins.keys():
        for plugin_cb in plugins[plugin_name]:
            test_name = plugin_cb.__name__
            full_name = '{}:{}'.format(plugin_name, test_name)

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
            if plugin_name in config:
                if '_all' in config[plugin_name]:
                    test_config.update(config[plugin_name]['_all'])
                if test_name in config[plugin_name]:
                    test_config.update(config[plugin_name][test_name])

            # Execute test
            logging.info("Executing test {}:{}".format(plugin_name, test_name))
            logging.debug("{}:{} config: {}".format(plugin_name, test_name, test_config))
            try:
                result = plugin_cb(**test_config)
                assert isinstance(result, Result)
                result.set_plugin_name(plugin_name)
                result.set_test_name(test_name)

                # Update all results with this result
                if result.has_passed is False or skip_passed is False:
                    morestd.data.deepupdate(results, result.to_dict())
            except Exception as err:
                sys.stderr.write("Error executing test '{}:{}': {}: {}\n".format(plugin_name, test_name, type(err), err))
                if debug is True:
                    logging.exception(err)

                # Create Error result.
                result = Result(desc="", explanation="", severity=0, passed=None)
                result.set_plugin_name(plugin_name)
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
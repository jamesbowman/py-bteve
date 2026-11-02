"""Run an EVE application with a connector selected on the command line."""

import argparse
import importlib
import sys


def run(app, minimal=False, argv=None):
    """Initialize EVE, call app(gd), finish pending commands, and close it.

    Connector modules expose add_arguments(parser) and EVE(**options), whose
    instances provide init(minimal=False), finish(), and close(). Unknown CLI
    arguments are left in sys.argv for the application, preserving argv[0].
    """
    selector = argparse.ArgumentParser(add_help=False, allow_abbrev=False)
    selector.add_argument("-c", "--connector", default="cspidriver")
    selected, _ = selector.parse_known_args(argv)
    module_name = "connectors." + selected.connector
    try:
        connector = importlib.import_module(module_name)
    except ModuleNotFoundError as exc:
        if exc.name == module_name:
            selector.error("Unknown connector: " + selected.connector)
        selector.error("Connector '{}' requires missing module '{}'".format(
            selected.connector, exc.name))

    parser = argparse.ArgumentParser(description="EVE application", parents=[selector],
                                     allow_abbrev=False)
    parser.add_argument("--minimal", action="store_true", default=minimal,
                        help="Boot EVE without loading the display configuration from flash")
    connector.add_arguments(parser)
    args, remaining = parser.parse_known_args(argv)
    options = vars(args)
    options.pop("connector")
    minimal = options.pop("minimal")

    original_argv = sys.argv
    sys.argv = original_argv[:1] + remaining
    try:
        gd = connector.EVE(**options)
        try:
            gd.init(minimal=minimal)
            result = app(gd)
            gd.finish()
            return result
        finally:
            gd.close()
    finally:
        sys.argv = original_argv

import sys
import os
from getopt import getopt
import json
import logging

import yaml
import jinja2


logger = logging.getLogger(__name__)


def main():
    options, arguments = getopt(
        sys.argv[1:],
        "hve",
        ["help", "version", "yaml=", "json=", "environment"]
    )

    # look for quickly terminating options
    for option, _ in options:
        if option in ["-h", "--help"]:
            print_help()
            return os.EX_OK
        elif option in ["-v", "--version"]:
            print_version()
            return os.EX_OK

    # fail early if no template was specified
    if len(arguments) < 1:
        logger.error("No template file was specified.")
        print_usage()
        return os.EX_USAGE

    # if only one argument is given use STDOUT
    if len(arguments) == 1:
        arguments.append("-")

    # we don't need more than 2 arguments
    if len(arguments) > 2:
        given_arguments = ", ".join(['"'+a+'"' for a in arguments])
        logger.error(
            f"We don't support more than two arguments: {given_arguments}"
        )
        return os.EX_USAGE

    # load all data sources specified on the commandline
    try:
        loaded_data = [parse_input_options(*o) for o in options]
    except FileNotFoundError as e:
        logger.error(e)
        return os.EX_NOINPUT

    # if no data was given use --environment
    if len(loaded_data) == 0:
        loaded_data = [parse_input_options("--environment", "")]

    # combine every input
    collated_data = {}
    for data in loaded_data:
        collated_data.update(data)

    # create template
    with open_file(arguments[0]) as template_stream:
        template = jinja2.Template(template_stream.read())
        template.filename = arguments[0]

    # and render to output
    with open_file(arguments[1], "w") as output:
        template.stream(collated_data).dump(output)
        output.write("\n")  # does the template eat this or the dump call?

    return os.EX_OK


def print_usage():
    print("""Usage:
  tpl [options] <template_file>
  tpl --help
  tpl --version""", file=sys.stderr)


def print_help():
    print_usage()
    print("""
Options:
  -e, --environment    Use all environment variables as data
  --json=<file>        Load JSON data from a file or STDIN
  --yaml=<file>        Load YAML data from a file or STDIN""", file=sys.stderr)


def print_version():
    # Although help and usage appear on STDERR, the version goes to STDOUT.
    # This is the same way that `less` does it under macOS, even though thats
    # probably not a good reason.
    from .__version__ import __version__
    print(f"tpl - {__version__}")


def parse_input_options(type, file):
    if type in ["-e", "--environment"]:
        return os.environ

    parsers = {
        "--yaml": load_yaml_stream,
        "--json": load_json_stream
    }

    return parsers[type](open_file(file))


def open_file(path, mode="r"):
    if path == "-":
        return {"r": sys.stdin, "w": sys.stdout}[mode]
    return open(path, mode)


def load_yaml_stream(stream):
    with stream:
        return yaml.safe_load(stream)


def load_json_stream(stream):
    with stream:
        return json.load(stream)

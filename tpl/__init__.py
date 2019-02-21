import sys
import os
from getopt import getopt
import json
import logging

import yaml
import jinja2


logger = logging.getLogger(__name__)


def main(*args):
    options, arguments = getopt(
        list(args[1:]),
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
            "We don't support more than two arguments: {}".format(given_arguments)
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
        collated_data = merge_data(collated_data, data)

    # set up Jinja2 environment
    j_env = jinja2.Environment(
        extensions=['jinja2.ext.do', 'jinja2.ext.loopcontrols'],
        keep_trailing_newline=True,
    )

    # create template
    with open_file(arguments[0]) as template_stream:
        template = j_env.from_string(template_stream.read())
        template.filename = arguments[0]

    # and render to output
    with open_file(arguments[1], "w") as output:
        template.stream(collated_data).dump(output)

    return os.EX_OK


def print_usage():
    print("""Usage:
  tpl [options] <template_file>
  tpl --help
  tpl --version""", file=sys.stderr)


def print_help():
    print_usage()
    jinja_version = jinja2.__version__
    if "dev" in jinja_version:
        jinja_version = "dev"
    help_text = """

tpl uses the Jinja2 templating engine to render it's output. You can find the
documentation for template designers at:
    http://jinja.pocoo.org/docs/{jinja_version}/templates/

If you provide multiple data sources they will be merged together. If a key is
present in more than one source the value of the source that was specified
last will be used. Nested objects will be merged with the same algorithm.

Options:
  -e, --environment    Use all environment variables as data
  --json=<file>        Load JSON data from a file or STDIN
  --yaml=<file>        Load YAML data from a file or STDIN"""
    print(help_text.format(jinja_version=jinja_version), file=sys.stderr)


def print_version():
    # Although help and usage appear on STDERR, the version goes to STDOUT.
    # This is the same way that `less` does it under macOS, even though thats
    # probably not a good reason.
    from .__version__ import __version__
    print("tpl - {}".format(__version__))


def merge_data(old: dict, new, array_key="_array_data", scalar_key="_scalar_data"):
    """Merge the data from the different sources.

    If the new value is a list it's elements will get appended to the list in
    _array_data.

    If the new value is a scalar (anything not a list or dict) it will replace
    the value in _scalar_data.

    if the new value is a dict it's elements will get merged with the elements
    already present. This also means that sub dicts in both values will get
    merged.
    """
    if type(new) == list:
        # if the new value is a list append it to the list element
        old[array_key] = old.get(array_key, []) + new
        return old

    if type(new) != dict:
        # if the new value is not a dict use it as a scalar
        old[scalar_key] = new
        return old

    return recursive_dict_merge(old, new)


def recursive_dict_merge(old: dict, new: dict):
    for key, value in new.items():
        if key not in old:
            old[key] = value
        elif type(old[key]) == dict and type(value) == dict:
            recursive_dict_merge(old[key], value)
        else:
            old[key] = value

    return old


def parse_input_options(type, file):
    if type in ["-e", "--environment"]:
        # os.environ is of type environ, but if we check the type in our
        # merge functions this has to be a dict
        return dict(os.environ)

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

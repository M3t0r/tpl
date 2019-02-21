import unittest.mock


import tpl


def indent(text, prefix):
    return "\n".join([prefix + line for line in text.splitlines()])


def test_current_help_in_readme(capsys):
    with unittest.mock.patch("jinja2.__version__", "latest"):
        tpl.print_help()
    output = capsys.readouterr()
    with open("./README.rst", "r") as readme:
        assert indent(output.err, " " * 4) in readme.read()

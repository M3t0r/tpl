import unittest.mock


import tpl


def test_current_help_in_readme(capsys):
    with unittest.mock.patch("jinja2.__version__", "latest"):
        tpl.print_help()
    output = capsys.readouterr()
    with open("./README.md", "r") as readme:
        assert output.err in readme.read()

from . import cli


def test_usage_and_error_without_arguments(cli):
    p = cli()
    assert p.returncode == 64  # EX_USAGE
    assert p.stderr.startswith("No template")
    assert "Usage" in p.stderr


def test_help_on_h(cli):
    p = cli("-h")
    assert p.returncode == 0
    assert "Usage:" in p.stderr
    assert "Options:" in p.stderr


def test_help_on_help(cli):
    p = cli("--help")
    assert p.returncode == 0
    assert "Usage:" in p.stderr
    assert "Options:" in p.stderr


def test_version_on_v(cli):
    p = cli("-v")
    assert p.returncode == 0
    assert "tpl - " in p.stdout


def test_version_on_version(cli):
    p = cli("--version")
    assert p.returncode == 0
    assert "tpl - " in p.stdout


def test_current_help_in_readme(cli):
    p = """Usage:
  tpl [options] <template_file>
  tpl --help
  tpl --version

Options:
  -e, --environment    Use all environment variables as data
  --json=<file>        Load JSON data from a file or STDIN
  --yaml=<file>        Load YAML data from a file or STDIN

Documentation:
  Jinja2               http://jinja.pocoo.org/docs/latest/
"""

    with open("./README.md", "r") as readme:
        assert p in readme.read()

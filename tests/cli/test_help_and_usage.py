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

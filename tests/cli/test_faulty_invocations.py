from . import cli


# For common exit codes see `man 3 sysexits`


def test_key_does_not_exist(cli):
    p = cli(
        cli.path_for_content("{{FOO}}"),
        env={}
    )
    assert p.stdout == ""


def test_corrupt_yaml(cli):
    p = cli(
        "--yaml", cli.path_for_content('{"FOO": "not properly closed'),
        cli.path_for_content("{{FOO}}")
    )
    assert p.returncode == 1


def test_corrupt_json(cli):
    p = cli(
        "--json", cli.path_for_content('{"FOO": "not properly closed'),
        cli.path_for_content("{{FOO}}")
    )
    assert p.returncode == 1

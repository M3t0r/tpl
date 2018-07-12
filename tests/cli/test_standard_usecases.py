from . import cli


def test_source_environment(cli):
    p = cli("-e", cli.path_for_content("{{FOO}}"), env={"FOO": "bar"})
    assert p.stdout == "bar\n"


def test_unicode_var(cli):
    p = cli("-e", cli.path_for_content("{{FOO}}"), env={"FOO": "🐍"})
    assert p.stdout == "🐍\n"


def test_shadowing_json_env(cli):
    p = cli(
        "--json", cli.path_for_json({"FOO": "json"}),
        "-e",
        cli.path_for_content("{{FOO}}"),
        env={"FOO": "env"}
    )
    assert p.stdout == "env\n"


def test_shadowing_yaml_env(cli):
    p = cli(
        "--yaml", cli.path_for_yaml({"FOO": "yaml"}),
        "-e",
        cli.path_for_content("{{FOO}}"),
        env={"FOO": "env"}
    )
    assert p.stdout == "env\n"


def test_yaml_flow_style(cli):
    p = cli(
        "--yaml", cli.path_for_content('{"FOO": "yaml"}'),
        cli.path_for_content("{{FOO}}")
    )
    assert p.stdout == "yaml\n"


def test_environment_by_default(cli):
    p = cli(
        cli.path_for_content("{{FOO}}"),
        env={"FOO": "bar"}
    )
    assert p.stdout == "bar\n"

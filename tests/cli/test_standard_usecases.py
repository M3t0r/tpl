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


def test_sub_dict_shadowing(cli):
    p = cli(
        "--json", cli.path_for_json({"FOO": {"BAR": "first"}}),
        "--json", cli.path_for_json({"FOO": {"BAR": "second"}}),
        cli.path_for_content("{{FOO['BAR']}}")
    )
    assert p.stdout == "second\n"


def test_sub_dict_merging(cli):
    p = cli(
        "--json", cli.path_for_json({"merge": {"FOO": "foo"}}),
        "--json", cli.path_for_json({"merge": {"BAR": "bar"}}),
        cli.path_for_content("{{merge['FOO']}}{{merge['BAR']}}")
    )
    assert p.stdout == "foobar\n"


def test_second_sub_dict_shadowing(cli):
    p = cli(
        "--json", cli.path_for_json({"merge": {"deeper": {"overwritten": "foo"}}}),
        "--json", cli.path_for_json({"merge": {"deeper": {"overwritten": "bar"}}}),
        cli.path_for_content("{{merge.deeper.overwritten}}")
    )
    assert p.stdout == "bar\n"


def test_second_sub_dict_merging(cli):
    p = cli(
        "--json", cli.path_for_json({"merge": {"deeper": {"FOO": "foo"}}}),
        "--json", cli.path_for_json({"merge": {"deeper": {"BAR": "bar"}}}),
        cli.path_for_content("{{merge.deeper.FOO}}{{merge.deeper.BAR}}")
    )
    assert p.stdout == "foobar\n"


def test_shadowing_of_dict(cli):
    p = cli(
        "--json", cli.path_for_json({"merge": {"foo": "bar"}}),
        "--json", cli.path_for_json({"merge": 'bar'}),
        cli.path_for_content("{{merge}}")
    )
    assert p.stdout == "bar\n"

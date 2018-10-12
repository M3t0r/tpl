from . import cli


def test_source_environment(cli):
    p = cli("-e", cli.path_for_content("{{FOO}}"), env={"FOO": "bar"})
    assert p.stdout == "bar"


def test_unicode_var(cli):
    p = cli("-e", cli.path_for_content("{{FOO}}"), env={"FOO": "🐍"})
    assert p.stdout == "🐍"


def test_shadowing_json_env(cli):
    p = cli(
        "--json", cli.path_for_json({"FOO": "json"}),
        "-e",
        cli.path_for_content("{{FOO}}"),
        env={"FOO": "env"}
    )
    assert p.stdout == "env"


def test_shadowing_yaml_env(cli):
    p = cli(
        "--yaml", cli.path_for_yaml({"FOO": "yaml"}),
        "-e",
        cli.path_for_content("{{FOO}}"),
        env={"FOO": "env"}
    )
    assert p.stdout == "env"


def test_yaml_flow_style(cli):
    p = cli(
        "--yaml", cli.path_for_content('{"FOO": "yaml"}'),
        cli.path_for_content("{{FOO}}")
    )
    assert p.stdout == "yaml"


def test_environment_by_default(cli):
    p = cli(
        cli.path_for_content("{{FOO}}"),
        env={"FOO": "bar"}
    )
    assert p.stdout == "bar"


def test_sub_dict_shadowing(cli):
    p = cli(
        "--json", cli.path_for_json({"FOO": {"BAR": "first"}}),
        "--json", cli.path_for_json({"FOO": {"BAR": "second"}}),
        cli.path_for_content("{{FOO['BAR']}}")
    )
    assert p.stdout == "second"


def test_sub_dict_merging(cli):
    p = cli(
        "--json", cli.path_for_json({"merge": {"FOO": "foo"}}),
        "--json", cli.path_for_json({"merge": {"BAR": "bar"}}),
        cli.path_for_content("{{merge['FOO']}}{{merge['BAR']}}")
    )
    assert p.stdout == "foobar"


def test_second_sub_dict_shadowing(cli):
    p = cli(
        "--json", cli.path_for_json({"merge": {"deeper": {"overwritten": "foo"}}}),
        "--json", cli.path_for_json({"merge": {"deeper": {"overwritten": "bar"}}}),
        cli.path_for_content("{{merge.deeper.overwritten}}")
    )
    assert p.stdout == "bar"


def test_second_sub_dict_merging(cli):
    p = cli(
        "--json", cli.path_for_json({"merge": {"deeper": {"FOO": "foo"}}}),
        "--json", cli.path_for_json({"merge": {"deeper": {"BAR": "bar"}}}),
        cli.path_for_content("{{merge.deeper.FOO}}{{merge.deeper.BAR}}")
    )
    assert p.stdout == "foobar"


def test_shadowing_of_dict(cli):
    p = cli(
        "--json", cli.path_for_json({"merge": {"foo": "bar"}}),
        "--json", cli.path_for_json({"merge": 'bar'}),
        cli.path_for_content("{{merge}}")
    )
    assert p.stdout == "bar"


def test_keep_no_newline_at_end(cli):
    p = cli(cli.path_for_content("{{FOO}}"), env={"FOO": "bar"})
    assert p.stdout == "bar"


def test_keep_one_newline_at_end(cli):
    p = cli(cli.path_for_content("{{FOO}}\n"), env={"FOO": "bar"})
    assert p.stdout == "bar\n"


def test_keep_two_newlines_at_end(cli):
    p = cli(cli.path_for_content("{{FOO}}\n\n"), env={"FOO": "bar"})
    assert p.stdout == "bar\n\n"


def test_keep_one_newline_at_beginning(cli):
    p = cli(cli.path_for_content("\n{{FOO}}"), env={"FOO": "bar"})
    assert p.stdout == "\nbar"


def test_keep_two_newlines_at_beginning(cli):
    p = cli(cli.path_for_content("\n\n{{FOO}}"), env={"FOO": "bar"})
    assert p.stdout == "\n\nbar"

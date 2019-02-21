from . import cli


def test_do_statement(cli):
    p = cli(cli.path_for_content("{% do {}.update({'k': 'v'}) %}"))
    assert p.stdout == ""
    assert p.stderr == ""
    assert p.returncode == 0


def test_continue_statement(cli):
    p = cli(
        "--json", cli.path_for_json({'data': [0, 0, 0, 0]}),
        cli.path_for_content("""
            {%- for v in data -%}
                {% if loop.index % 2 %}{% continue %}{% endif %}
                {{- v -}}
            {%- endfor -%}
        """)
    )
    assert p.stdout == "00"
    assert p.stderr == ""
    assert p.returncode == 0


def test_continue_statement(cli):
    p = cli(
        "--json", cli.path_for_json({'data': [0, 0, 0, 0]}),
        cli.path_for_content("""
            {%- for v in data -%}
                {{- v -}}
                {% break %}
            {%- endfor -%}
        """)
    )
    assert p.stdout == "0"
    assert p.stderr == ""
    assert p.returncode == 0

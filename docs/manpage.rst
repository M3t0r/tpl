.. _tpl:

:program:`tpl`: render templates with data from various sources
===============================================================

Synopsis
--------

.. program:: tpl

| :program:`tpl` [:ref:`options <options>`] <:option:`template_file`> [:option:`output_file`]
| :program:`tpl` :option:`-h` | :option:`--help`
| :program:`tpl` :option:`-v` | :option:`--version`


Description
-----------

:program:`tpl` renders a `Jinja2 <https://palletsprojects.com/p/jinja/>`_
template file with data aggregated from one or more data sources specified via
options and writes the result to :option:`output_file`. It is meant to be
easily composable with other unix tools like :program:`xargs`, :program:`curl`,
and :program:`jq`.

.. option:: template_file

    The template file that will be rendered. A :option:`template_file` of
    "``-``" stands for ``STDIN``.

.. option:: output_file

    The file that the rendered template will be written to. If an error occurs
    during templating the output might end up with incomplete and broken data.
    When a file with the same name already exists it will be overwritten
    without notice. If ommitted this argument defaults to "``-``" which stands
    for ``STDOUT``.


.. _options:

Options
-------

The order of data source options is important. See the :ref:`data-merging`
section for more information.

.. option:: -h, --help

    Print a help message to ``STDERR`` and exit successfully.

.. option:: -v, --version

    Write the version number to ``STDOUT`` and exit successfully.

.. option:: -e, --environment

    Load environmant variables as key-value pairs into the context. This allows
    you to access, for example, `$PATH` with ``{{ PATH }}``.

    If no other data source option was specified this option is used by
    default. Templates can only access the environment if no other data sources
    were specified or this flag is used. This is to prohibit leaking of secrets
    from the environment.

.. option:: --json <file>

    Load data from a JSON file into the context. Unlike :program:`jq`,
    :program:`tpl` does not support multiple JSON objects separated by
    whitespaces. Internally this uses Python's :py:func:`json.load`.

.. option:: --yaml <file>

    Load data from a YAML file into the context. The YAML file can only contain
    one document. If the parser encounters a second document :program:`tpl`
    will abort with an error. This data source uses the
    `PyYAML library <https://pyyaml.org/wiki/PyYAMLDocumentation>`_.


.. _data-merging:

Data Merging
------------

If you provide multiple data sources they will be merged together to provide a
context for the Jinja2 engine. If a key is present in more than one source the
value of the source that was specified last will be used. Nested objects will
be merged with the same algorithm.

.. only:: html

    See :py:meth:`tpl.merge_data` and it's source code for the algorithm.

Special treatment is given to root objects of every data source when merging:
If the root object is a list, it's elements will be added to the end of
``_array_data``. If the root object is a a scalar value, like a string,
boolean, or number, it's value will be stored in ``_scalar_data``. When one of
these special behaviours is triggered the already assembled context is not
cleared of previously defined key-value pairs:

.. code-block:: bash

    $ tpl \
    >     --json <(echo '"the answer"') \
    >     --json <(echo '{"foo":"bar"}') \
    >     --json <(echo "42") \
    >     <(echo 'scalar: {{ _scalar_data }}, foo: {{ foo }}')
    scalar: 42, foo: bar
    # and not scalar: 42, foo:

.. only:: html

    This behaviour is only applied to values at the root:

    .. code-block:: bash

        $ tpl \
        >     --json <(echo '{"spam":"egg"}') \
        >     --json <(echo '{"spam":{"sub":"marine"}}') \
        >     --json <(echo '{"spam":"ham"}') \
        >     <(echo '{{ spam }}')
        ham
        # and not {'sub': 'marine', '_scalar_data': 'ham'}


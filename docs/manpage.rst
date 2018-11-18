.. _tpl:

tpl: render templates with data from various sources
====================================================

Synopsis
--------

.. program:: tpl

| :program:`tpl` [:ref:`options <options>`] <:option:`template_file`> [:option:`output_file`]
| :program:`tpl` :option:`-h` | :option:`--help`
| :program:`tpl` :option:`-v` | :option:`--version`


Description
-----------

:program:`tpl` renders a `Jinja2 <https://palletsprojects.com/p/jinja/>`_ template file with data aggregated from one or more
data sources specified via options and writes the result to
:option:`output_file`.

.. option:: template_file

    The template file that will be rendered. A :option:`template_file` of
    "``-``" stands for ``STDIN``.

.. option:: output_file

    The file that the rendered template will be written to. If an error occurs
    during templating this file might end up with incomplete and broken data.
    When a file with the same name already exists it will be overwritten
    without notice. If ommitted this argument defaults to "``-``" which stands
    for ``STDOUT``.


.. _options:

Options
-------

The order of data source options is important. See :ref:`data-merging` for more
information.

.. option:: -h, --help

    Print a help message to ``STDERR`` and exit successfully.

.. option:: -v, --version

    Write the version number to ``STDOUT`` and exit successfully.

.. option:: -e, --environment

.. option:: --json <file>

.. option:: --yaml <file>


.. _data-merging:

Data Merging
------------

See :py:meth:`tpl.merge_data` for an explanation.

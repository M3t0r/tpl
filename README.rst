`tpl`: render templates with data from various sources
===============================================================

.. image:: https://github.com/M3t0r/tpl/actions/workflows/tests.yaml/badge.svg
    :target: https://github.com/M3t0r/tpl/actions/workflows/tests.yaml
    :alt: GitHub Actions build badge

.. image:: https://img.shields.io/pypi/v/tpl.svg
    :target: https://pypi.python.org/pypi/tpl/
    :alt: 

.. image:: https://readthedocs.org/projects/tpl/badge/
    :target: https://readthedocs.org/projects/tpl/
    :alt: Documentation Status

You want to fill data into a template file?

.. code:: bash

    tpl --yaml data.yaml template.file > rendered.file

You have everything already set up in your environment and now you just want to
POST it somewhere?

.. code:: bash

    tpl structure.json \
      | curl \
          -X POST \
          -H "Content-Type: application/json" \
          -d@- \
          httpbin.org/anything

You want to fill in a template in your CD pipeline and have access to docker?

.. code:: bash

    echo "My go-to editor is {{VISUAL}} on {{OS}}" \
      | docker run --rm -i -e "VISUAL" -e "OS=$(uname)" m3t0r/tpl -

Installation
------------

``pip install tpl``, ``docker pull M3t0r/tpl`` or ``make install`` 

Input sources
-------------

`tpl` supports multiple sources:
 * YAML files (``--yaml <file>``)
 * JSON files (``--json <file>``)
 * environment variables (``--environment``)

You can specify multiple sources at once, but if a key is present in more than
one then it's value will be taken from the latter source. This can be useful if
you have default values that you want to always be present:

.. code:: bash

    tpl \
      --yaml defaults.yaml \
      --json <(curl -H "Content-Type: application/json" now.httpbin.org) \
      template.jinja2 > results.html

Usage
-----
.. code::

    Usage:
      tpl [options] <template_file>
      tpl --help
      tpl --version
    
    
    tpl uses the Jinja2 templating engine to render it's output. You can find the
    documentation for template designers at:
        http://jinja.pocoo.org/docs/latest/templates/
    
    If you provide multiple data sources they will be merged together. If a key is
    present in more than one source the value of the source that was specified
    last will be used. Nested objects will be merged with the same algorithm.
    
    Options:
      -e, --environment    Use all environment variables as data
      --json=<file>        Load JSON data from a file or STDIN
      --yaml=<file>        Load YAML data from a file or STDIN


#!/usr/bin/env python3
from os import popen


from setuptools import setup


with open("./README.md") as readme:
    readme_text = readme.read()

with popen("git describe --tags --dirty | sed 's/^v//'", "r") as git_output:
    git_version_string = git_output.readline()[:-1]  # truncate the \n

    # update version file
    with open("tpl/__version__.py", "w") as v:
        v.write(
            "__version__ = '{version_string}'\n".format(
                version_string=git_version_string
            )
        )


setup(
    name='tpl',
    version=git_version_string,
    author='Simon Lutz Brüggen',
    description="Render templates with data from various sources",
    long_description=readme_text,
    install_requires=["pyyaml", "jinja2"],
    entry_points={
        'console_scripts': ["tpl=tpl:main"]
    },
    packages=["tpl"]
)

#!/usr/bin/env python3
from os import popen


from setuptools import setup


with open("./README.rst") as readme:
    readme_text = readme.read()

with popen(
        "git describe --tags --dirty --match 'v*' "
        "| sed -e 's/^v//' -e 's/-/_/g' -e 's/_/+/1' -e 's/_/./g'",
        "r"
) as git_output:
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
    url="https://github.com/m3t0r/tpl",
    long_description=readme_text,
    python_requires=">3.5",
    install_requires=["pyyaml>=3.13", "jinja2>=2.10"],
    entry_points={
        'console_scripts': ["tpl=tpl.__main__:_argv_wrapper"]
    },
    packages=["tpl"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Operating System :: Unix",
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
    ]
)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys
from os import path

from setuptools import find_packages, setup

CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON = (3, 7)


# This check and everything above must remain compatible with Python 2.7.
if CURRENT_PYTHON < REQUIRED_PYTHON:
    required_version = "{}.{}".format(*REQUIRED_PYTHON)
    current_version = "{}.{}".format(*CURRENT_PYTHON)
    sys.stderr.write(
        "This version of CrowdStrike Client requires Python {0},"
        " but you're trying to install it on Python {1}.\n".format(
            required_version, current_version
        )
    )
    sys.exit(1)


# Package meta-data.
REQUIRES_PYTHON = ">=3.7"

REQUIRED = ["requests", "pydantic"]

EXTRAS = {
    # 'fancy feature': ['fancy'],
}

# this directory
here = path.abspath(path.dirname(__file__))


# read the __version__.py into about variable
def add_default(match):
    attr_name, attr_value = match.groups()
    return ((attr_name, attr_value.strip("\"'")),)


re_meta = re.compile(r"^__(\w+?)__\s*=\s*(.*)")
parts = {re_meta: add_default}

about = {}

version_file = path.join(here, "crowdstrike_client", "__version__.py")
with open(version_file, encoding="utf-8") as f_obj:
    for line in f_obj:
        for pattern, handler in parts.items():
            m = pattern.match(line.strip())
            if m:
                about.update(handler(m))


# read the contents of your README file
with open(path.join(here, "README.rst"), encoding="utf-8") as f:
    long_description = f.read()


setup(
    name=about["title"],
    version=about["version"],
    description=about["description"],
    long_description=long_description,
    long_description_content_type="text/x-rst",
    author=about["author"],
    author_email=about["author_email"],
    url=about["url"],
    packages=find_packages(exclude=["tests", "*.tests", "*.tests.*", "tests.*"]),
    # PEP-561: https://www.python.org/dev/peps/pep-0561/
    package_data={about["title"]: ["py.typed"]},
    python_requires=REQUIRES_PYTHON,
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    license=about["license"],
    zip_safe=False,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)",  # noqa
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
    ],
)

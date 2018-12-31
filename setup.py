#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# GitAuthors - A simple tool that prints a quick summary of a repo's authors.
#
# Ansgar Grunseid
# grunseid.com
# grunseid@gmail.com
#
# License: MIT
#

import os
import sys
from os.path import dirname, join as pjoin
from setuptools import setup, find_packages, Command
from setuptools.command.test import test as TestCommand

from gitauthors.__version__ import __version__ as VERSION


class Publish(Command):
    """Publish to PyPI with twine."""
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        os.system('python setup.py sdist bdist_wheel')

        sdist = 'dist/gitauthors-%s.tar.gz' % VERSION
        wheel = 'dist/gitauthors-%s-py2.py3-none-any.whl' % VERSION
        rc = os.system('twine upload "%s" "%s"' % (sdist, wheel))

        sys.exit(rc)


setup(
    name='gitauthors',
    license='MIT',
    version=VERSION,
    author='Ansgar Grunseid',
    author_email='grunseid@gmail.com',
    url='https://github.com/gruns/gitauthors',
    description=(
        'Inspect variables, expressions, and program execution with a '
        'single, simple function call.'),
    long_description=(
        'Information and documentation can be found at '
        'https://github.com/gruns/gitauthors.'),
    platforms=['any'],
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'Development Status :: 4 - Beta',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Programming Language :: Python :: Implementation :: CPython',
    ],
    entry_points={
        'console_scripts': ['gitauthors=gitauthors.cli:main'],
    },
    tests_require=[
        'flake8',
    ],
    install_requires=[
        'docopt>=0.6.2',
        'dulwich>=0.19.6',
    ],
    cmdclass={
        'publish': Publish,
    },
)

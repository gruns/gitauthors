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


"""GitAuthors - Get a quick summary of a repo's authors.

Usage:
  gitauthors <repository-URL>
  gitauthors -h | --help
  gitauthors --version

Options:
  -h --help     Show this screen.
  --version     Show version.

Examples:
  gitauthors https://github.com/gruns/gitauthors
"""


from docopt import docopt

from gitauthors import collateGitAuthors, formatGitAuthors
try:  # Local import.
    from __version__ import __version__ as VERSION
except ImportError:  # System import.
    from gitauthors.__version__ import __version__ as VERSION


def main():
    args = docopt(__doc__, version=VERSION)  # Raises SystemExit.
    url = args.get('<repository-URL>')

    authorsByNumCommits = collateGitAuthors(url)
    output = formatGitAuthors(authorsByNumCommits)

    print(output)


if __name__ == '__main__':
    main()

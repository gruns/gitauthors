#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

#
# GitAuthors - A simple tool that prints a useful summary of a repo's authors.
#
# Ansgar Grunseid
# grunseid.com
# grunseid@gmail.com
#
# License: MIT
#

"""GitAuthors

Usage:
  gitauthors <repositoryUrl>
  gitauthors -h | --help
  gitauthors --version

Options:
  -h --help     Show this screen.
  --version     Show version.

Examples:
  gitauthors https://github.com/gruns/gitauthors
"""

import os
import sys
import shutil
from tempfile import mkdtemp
from io import BytesIO, StringIO
from contextlib import contextmanager

from docopt import docopt
from dulwich import porcelain
try:
    from icecream import ic
except ImportError:
    ic = lambda *a: None if not a else (a[0] if len(a) == 1 else a)

from __version__ import __version__ as VERSION


# MonkeyPatch a silent fetch() into dulwich.porcelain until
#
#   https://github.com/dulwich/dulwich/pull/643
#
# is merged.
_fetch = porcelain.fetch
def silentFetch(*args, **kwargs):
    kwargs['errstream'] = BytesIO()
    return _fetch(*args, **kwargs)
porcelain.fetch = silentFetch


@contextmanager
def temporaryDirectory():
    tmp = mkdtemp()
    try:
        yield tmp
    finally:
        shutil.rmtree(tmp, ignore_errors=True)  # Can still raise.


class GitLogProcessor():
    def __init__(self):
        self._dateLine = None
        self._authorLine = None
        self.authors = {}  # email -> (name, numCommits, latestCommitDate).

    def processCommit(self):
        if not self._authorLine or not self._dateLine:
            return

        # Author: Some Name <email@address.com>
        authorLine = self._authorLine.rstrip('>')
        name, email = [s.strip() for s in authorLine.rsplit('<', 1)]

        # Date:   Wed Nov 16 2011 14:09:22 -0500
        dateOnlyNoTime = '%s %s, %s' % tuple(self._dateLine.split()[1:4])

        _, numCommits, _ = self.authors.get(email, (None, 0, None))
        numCommits += 1

        self.authors[email] = (name, numCommits, dateOnlyNoTime)

    def write(self, line):
        line = line.strip()
        if line.startswith('Author: '):
            self._authorLine = line.split('Author: ', 1)[-1].strip()
        elif line.startswith('Date:   '):
            self._dateLine = line.split('Date:   ', 1)[-1].strip()
            self.processCommit()


def getRepositoryAuthors(path):
    authors = {}

    log = GitLogProcessor()
    porcelain.log(path, outstream=log, reverse=True)

    authors = list(log.authors.items())
    byNumCommits = sorted(authors, key=lambda author: author[1][1])[::-1]

    return byNumCommits


def gitauthors(repoUrl):
    lines = []

    with temporaryDirectory() as repo:
        with open(os.devnull, 'wb') as devnull:
            porcelain.clone(repoUrl, repo, errstream=devnull)

        authors = getRepositoryAuthors(repo)

        longestNameLen = max(len(t[0]) for _, t in authors)
        longestEmailLen = max(len(email) for email, _ in authors)
        longestCommitsLen = max(len(str(t[1])) for _, t in authors)

        fmt = '{0:%i}  {1:<%i}  {2:>%i} %%s last on {3}'
        fmt = fmt % (longestNameLen, longestEmailLen, longestCommitsLen)
        for email, (name, numCommits, latestCommitDate) in authors:
            tmp = fmt % ('commit, ' if numCommits == 1 else 'commits,')
            lines.append(tmp.format(name, email, numCommits, latestCommitDate))

    return os.linesep.join(lines)


def main():
    args = docopt(__doc__, version=VERSION)  # Raises SystemExit.
    url = args.get('<repositoryUrl>')

    out = gitauthors(url)

    print(out)


if __name__ == '__main__':
    main()

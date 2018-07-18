#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

#
# GitAuthors - A simple tool that prints an author summary of a git repo.
#
# Ansgar Grunseid
# grunseid.com
# grunseid@gmail.com
#
# License: MIT
#

import os
import sys
import shutil
from io import StringIO
from tempfile import mkdtemp
from contextlib import contextmanager

from furl import furl
from dulwich import porcelain


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
    with temporaryDirectory() as repo:
        with open(os.devnull, 'wb') as devnull:
            porcelain.clone(repoUrl, repo, errstream=devnull)

        authors = getRepositoryAuthors(repo)

        longestNameLen = max(len(t[0]) for _, t in authors)
        longestEmailLen = max(len(email) for email, _ in authors)
        longestCommitsLen = max(len(str(t[1])) for _, t in authors)

        fmt = '{0:%i}  {1:<%i}  {2:>%i} commits, last on {3}'
        fmt = fmt % (longestNameLen, longestEmailLen, longestCommitsLen)
        for email, (name, numCommits, latestCommitDate) in authors:
            print(fmt.format(name, email, numCommits, latestCommitDate))

        return authors


if __name__ == '__main__':
    url = sys.argv[-1]
    gitauthors(url)

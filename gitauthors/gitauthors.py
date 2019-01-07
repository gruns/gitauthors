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
import shutil
from io import BytesIO
from tempfile import mkdtemp
from time import gmtime, strftime
from contextlib import contextmanager

from dulwich import porcelain
try:
    from icecream import ic
except ImportError:  # Graceful fallback if IceCream isn't installed.
    ic = lambda *a: None if not a else (a[0] if len(a) == 1 else a)


def utf8(s):
    if hasattr(s, 'decode'):  # Python 2.
        return s.decode('utf8')
    return s  # Python 3.


@contextmanager
def temporaryDirectory():
    tmp = mkdtemp()
    try:
        yield tmp
    finally:
        shutil.rmtree(tmp, ignore_errors=True)  # Can still raise.


def getRepositoryAuthorsByNumberOfCommits(path):
    authors = {}  # email -> (name, numCommits, latestCommitDate).

    with porcelain.open_repo_closing(path) as repo:
        for entry in repo.get_walker():
            commit = entry.commit
            author = utf8(commit.author)

            date = gmtime(commit.author_time)
            name, email = [s.strip(' <>') for s in author.rsplit(' ', 1)]

            _, numCommits, _ = authors.get(email, ('ignored', 0, 'ignored'))
            numCommits += 1

            authors[email] = (name, numCommits, date)

    items = [
        (email, name, numCommits, date)
        for email, (name, numCommits, date) in authors.items()]
    authorsByNumCommits = sorted(items, key=lambda author: author[2])[::-1]

    # List of (email, name, numCommits, latestCommitDate) tuples.
    return authorsByNumCommits


def formatGitAuthors(authorsByNumCommits):
    lines = []

    longestNameLen = max(len(name) for _, name, _, _ in authorsByNumCommits)
    longestEmailLen = max(len(email) for email, _, _, _ in authorsByNumCommits)
    longestCommitsLen = max(
        len(str(numCommits)) for _, _, numCommits, _ in authorsByNumCommits)

    t = (longestNameLen, longestEmailLen, longestCommitsLen)
    fmt = u'{0:%i}  {1:<%i}  {2:>%i} %%s latest on {3}' % t
    for email, name, numCommits, latestCommitDate in authorsByNumCommits:
        datestr = utf8(strftime('%b %d, %Y', latestCommitDate))
        line = fmt % (u' commit,' if numCommits == 1 else u'commits,')
        lines.append(line.format(name, email, numCommits, datestr))

    return os.linesep.join(lines)


def collateGitAuthors(repoUrl):
    with temporaryDirectory() as repoPath:
        with open(os.devnull, 'wb') as devnull:
            porcelain.clone(repoUrl, repoPath, errstream=devnull)

        authors = getRepositoryAuthorsByNumberOfCommits(repoPath)

    return authors

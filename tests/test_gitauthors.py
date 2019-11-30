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


import shutil
import tempfile
import unittest
from os.path import join as pjoin


import gitauthors
from dulwich.repo import Repo
try:
    from icecream import ic
except ImportError:  # Graceful fallback if IceCream isn't installed.
    ic = lambda *a: None if not a else (a[0] if len(a) == 1 else a)


class TestGitAuthors(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.repo = Repo.init(self.dir)

        self.gorl = (u'Gorl', u'gorl@aol.com')
        self.sprap = (u'Sprap Spoops', u'spoops@gmail.com')

        fmt = '%s <%s>'
        self._commit('one', fmt % self.gorl)
        self._commit('two', fmt % self.sprap)
        self._commit('three', fmt % self.gorl)
        self._commit('four', fmt % self.gorl)

    def tearDown(self):
        shutil.rmtree(self.dir)

    def test_api(self):
        authors = gitauthors.api.getRepositoryAuthorsByNumberOfCommits(self.dir)
        assert len(authors) == 2

        email, name, numCommits, _ = authors[0]
        assert (name, email) == self.gorl and numCommits == 3

        email, name, numCommits, _ = authors[1]
        assert (name, email) == self.sprap and numCommits == 1

    def _commit(self, fname, author):
        with open(pjoin(self.dir, fname), 'w') as f:
            f.write('lolsup')

        self.repo.stage([fname])
        self.repo.do_commit(fname, committer=author, author=author)

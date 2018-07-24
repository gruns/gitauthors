# GitAuthors

GitAuthors is simple tool that prints a useful summary of a repo's authors:
name, email, number of commits, and last commit date.

Once, installed, it's available via the `gitauthors` command.


### Usage

To use `gitauthors`, just provide it the URL of a respository and let it go to
work. `gitauthors` will, in turn

  1. Checkout the repository to a temporary directory.
  2. Parse the repository's log history.
  3. Collate a list of authors and their commits.
  4. Output a nice, formatted summary of the repository's authors.

```
$ gitauthors https://github.com/gruns/gitauthors
grun             grunseid@gmail.com              2 commits, last on Jul 20, 2018
Ansgar Grunseid  gruns@users.noreply.github.com  1 commits, last on Jul 17, 2018
```

That's it. Simple.


### Installation

Installing GitAuthors with pip is easy.

```
$ pip install gitauthors
```
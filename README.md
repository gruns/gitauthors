<h1>
  <div align="center">
    <img src="https://raw.githubusercontent.com/gruns/gitauthors/master/logo.svg" width="300px" alt="GitAuthors">
  </div>
  GitAuthors
</h1>


GitAuthors is simple tool that prints a quick summary of a repository's authors,
as collated by commits. Summary output includes each author's name, email,
number of commits, and date of last commit.

Once, installed, GitAuthors is available via the `gitauthors` command.


### Usage

To use, provide `gitauthors` the URL of a respository and let it go to
work. `gitauthors` will, in turn:

  1. Check out the repository into a temporary directory.
  2. Parse the repository's log history.
  3. Collate a list of the repository's authors and their commits.
  4. Output a nicely formatted summary of the repository's authors.

Like

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
<div align="center">
  <img src="logo.svg" width="300px" height="200px" alt="GitAuthors">
</div>

# GitAuthors

GitAuthors is simple tool that prints a quick summary of a repository's authors,
as collated by commits. Summary output includes each author's name, email,
number of commits, and date of last commit.

Once installed, GitAuthors is available via the `gitauthors` command.


### Usage

To use, provide `gitauthors` the URL of a respository and let it go to
work. `gitauthors` will, in turn:

  1. Check out the repository into a temporary directory.
  2. Parse the repository's log history.
  3. Collate a list of the repository's authors and their commits.
  4. Output a nicely formatted summary of the repository's authors and their
     commits.
  5. Clean up after itself and delete the temporary directory.

Example:

```
$ gitauthors https://github.com/gruns/gitauthors
Ansgar Grunseid  grunseid@gmail.com              16 commits, latest on Aug 06, 2018
Ansgar Grunseid  gruns@users.noreply.github.com   1  commit, latest on Jul 17, 2018
```

That's it. Simple.


Of course `gitauthors` can also be imported and used programmatically, too.

```python
>>> from gitauthors import collateGitAuthors, formatGitAuthors
>>>
>>> authors = collateGitAuthors('https://github.com/gruns/gitauthors')
>>> authors[0]
('grunseid@gmail.com', 'grun', 46, time.struct_time(tm_year=2018, tm_mon=7, tm_mday=18, tm_hour=7, tm_min=8, tm_sec=14, tm_wday=2, tm_yday=199, tm_isdst=0))
>>>
>>> formatted = formatGitAuthors(authors)
>>> print(formatted)
grun             grunseid@gmail.com              46 commits, latest on Jul 18, 2018
Ansgar Grunseid  gruns@users.noreply.github.com   1  commit, latest on Jul 18, 2018
```


### Installation

Installing GitAuthors with pip is easy.

```
$ pip install gitauthors
```
# Clean Markdown GitHub Action

This action prints looks for Markdown files in your repository, and for each one:

- Adds or updates a [table of contents](https://pypi.org/project/md-toc/)
- Formats the file with [prettier](https://prettier.io)

In addition, it also updates your project’s `README.md` with a table of contents.

It updates the PR in which the action ran with one commit per file that it changes.

To include a table of contents in a markdown file, do this:

```md
Table of Contents

<!-- TOC -->
<!-- TOC -->

# Title

Stuff

## Header 1

And

## Header 2

Things
```

The table of contents will be inserted between the two `<!-- TOC -->` placeholders.

To include an index of all markdown files in the directory in your `README.md`, mark off a section with this placeholder: `<!--- Index -->`, similar to `<!-- TOC -->` from above.

## Inputs

### `gh_token`

The GitHub token used to authenticate with GitHub to push changes to a PR.

**Required**

### `commit_message`

The commit message to use when commiting fixes.

**Required**

## Example Usage

```yml
- name: Clean markdown
  uses: gps/clean-markdown@master
  with:
    gh_token: ${{ secrets.GITHUB_TOKEN }}
    commit_message: Fix formatting
```

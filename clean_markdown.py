#!/usr/bin/env python3

import github3
import glob
import md_toc
import os
import subprocess
from pprint import pprint


def run_proc(cmd):
    return subprocess.run(cmd, shell=True, check=True, text=True).stdout


def find_all_markdown_files():
    return sorted([f for f in glob.glob("**/*.md", recursive=True) if f.lower() != "readme.md"])


def main():
    md_files = find_all_markdown_files()

    print("Found markdown files:", md_files)

    updated_files = []

    for md_file in md_files:
        toc = md_toc.build_toc(md_file, keep_header_levels=6, parser="github")
        with open(md_file) as fin:
            original_contents = fin.read()
        md_toc.write_string_on_file_between_markers(md_file, toc, "<!-- TOC -->")
        run_proc(
            f"/opt/clean_markdown/node_modules/prettier/bin-prettier.js --write {md_file}"
        )
        with open(md_file) as fin:
            new_contents = fin.read()
        if original_contents != new_contents:
            updated_files.append((md_file, new_contents))

    indent_per_level = "    "
    index = ""
    seen = set([""])

    for md_file in md_files:
        loc = os.path.split(md_file)[0]
        if loc not in seen:
            indent = indent_per_level * (len(loc.split(os.sep)) - 1)
            index += indent + "- "
            index += f"[{os.path.split(loc)[-1]}]({loc})"
            index += "\n"
            seen.add(loc)
        fn = os.path.split(md_file)[-1]
        index += indent_per_level * (len(md_file.split(os.sep)) - 1)
        index += "- "
        index += f"[{fn}]({md_file})"
        index += "\n"

    with open("README.md") as fin:
        original_readme = fin.read()
    md_toc.write_string_on_file_between_markers("README.md", index, "<!--- Index -->")
    run_proc(
        f"/opt/clean_markdown/node_modules/prettier/bin-prettier.js --write README.md"
    )
    with open("README.md") as fin:
        new_readme = fin.read()
    if original_readme != new_readme:
        updated_files.append(("README.md", new_readme))

    github = github3.login(token=os.environ["INPUT_GH_TOKEN"])
    env_repo = os.environ["GITHUB_REPOSITORY"]
    owner = env_repo.split("/")[0]
    repo = env_repo.split("/")[1]
    repository = github.repository(owner, repo)
    branch_name = os.environ["GITHUB_HEAD_REF"]
    commit_message = os.environ["INPUT_COMMIT_MESSAGE"]
    print("Updated files:")
    pprint(updated_files)
    for t in updated_files:
        print("Pushing:", t[0])
        repository.file_contents("/" + t[0], ref=branch_name).update(
            commit_message, t[1].encode("utf-8"), branch=branch_name
        )


if __name__ == "__main__":
    main()

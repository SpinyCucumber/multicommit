from git import Repo, Head

import re
import sys

SUFFIX_PATTERN = re.compile(r"^(?P<root>(?:[a-zA-Z-_/])*)_(?:(?:[A-Z])+_)*(?:[A-Z])+")

def multicommit(repo: Repo, args: list[str]):
    # Forward arguments to commit command
    repo.git.commit(*args)
    # If active branch is "subbranch", cherry-pick commit onto parent branch as well
    active_branch = repo.active_branch
    match = SUFFIX_PATTERN.match(active_branch.path)
    if match:
        root_branch = Head(repo, match.groupdict()["root"])
        root_branch.checkout()
        repo.git._call_process("cherry-pick", active_branch.path)
        active_branch.checkout()

def main():
    repo = Repo(search_parent_directories=True)
    multicommit(repo, sys.argv[1:])
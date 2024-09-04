from git import Repo, Head

import re
import os

SUFFIX_PATTERN = re.compile(r"^(?P<root>(?:[a-zA-Z-_/])*)_(?:(?:[A-Z])+_)*(?:[A-Z])+")

def main():
    # Assume current working dir is a repo
    repo = Repo(os.getcwd())
    # Commit!
    repo.index.commit("Test message")
    # If active branch is "subbranch", cherry-pick commit onto parent branch as well
    active_branch = repo.active_branch
    match = SUFFIX_PATTERN.match(active_branch.path)
    if match:
        root_branch = Head(repo, match.groupdict()["root"])
        root_branch.checkout()
        repo.git.__getattr__("cherry-pick")(active_branch.path)
        active_branch.checkout()
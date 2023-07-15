import contextlib
from pathlib import Path

from src.su6_plugin_svelte_check.find_project_root import find_project_root

try:
    chdir = contextlib.chdir
except AttributeError:
    from contextlib_chdir import chdir


def test_find_project_root_node_modules():
    with chdir("./pytest_examples/no_issues"):
        path, reason = find_project_root(tuple(), "")
        assert path.exists() and str(path.resolve()) == str(Path("../").resolve())
        assert reason == "node_modules"


def test_find_project_root_git():
    path, reason = find_project_root(("src", "./pytest_examples/no_issues"))

    assert path.exists() and str(path.resolve()) == str(Path("./").resolve())
    assert reason == ".git directory"

def test_find_project_root_notfound():
    path, reason = find_project_root(("src", "../"))

    assert path.exists() and str(path.resolve()) == str(Path("/").resolve())
    assert reason == "file system root"

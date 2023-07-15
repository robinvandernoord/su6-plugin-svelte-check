import contextlib

from su6 import app
from typer.testing import CliRunner
from plumbum import local

try:
    chdir = contextlib.chdir
except AttributeError:
    from contextlib_chdir import chdir

runner = CliRunner(mix_stderr=False)


def prepare_env():
    local["npm"]("install", "svelte-check")


def test_no_issues():
    with chdir("./pytest_examples"):
        prepare_env()

        result = runner.invoke(app, ["svelte-check", "--tsconfig", "./tsconfig-no_issues.json"])
        print(result.stdout, result.stderr)
        assert result.exit_code == 0


def test_issues():
    with chdir("./pytest_examples"):
        prepare_env()

        result = runner.invoke(app, ["svelte-check", "--tsconfig", "./tsconfig-issues.json"])
        print(result.stdout, result.stderr)
        assert result.exit_code == 1


def test_warnings():
    with chdir("./pytest_examples"):
        prepare_env()

        result = runner.invoke(app, ["svelte-check", "--tsconfig", "./tsconfig-warnings.json"])
        print(result.stdout, result.stderr)
        assert result.exit_code == 0

        result = runner.invoke(app, ["svelte-check", "--tsconfig", "./tsconfig-warnings.json", "--strict"])
        print(result.stdout, result.stderr)
        assert result.exit_code == 1

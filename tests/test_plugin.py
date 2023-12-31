import shutil
from pathlib import Path

from plumbum import local
from su6 import app
from typer.testing import CliRunner

from src.su6_plugin_svelte_check.helpers import chdir

runner = CliRunner(mix_stderr=False)


def prepare_env():
    local["npm"]("install", "svelte-check")


def test_install():
    # install_svelte_check

    target_dir = Path("pytest_examples/node_modules")

    if target_dir.exists():
        shutil.rmtree(target_dir)

    result = runner.invoke(app, ["install-svelte-check", "--target-dir", "./pytest_examples"])

    assert not Path("node_modules").exists()
    assert Path("pytest_examples/node_modules/svelte-check/bin/svelte-check").exists()

    assert result.exit_code == 0

    result = runner.invoke(app, ["install-svelte-check", "--target-dir", "./non/existent/folder"])

    assert result.exit_code == 1


def test_no_issues():
    with chdir("./pytest_examples"):
        prepare_env()

        result = runner.invoke(app, ["svelte-check", "--target", "./no_issues"])
        print(result.stdout, result.stderr)
        assert result.exit_code == 0


def test_issues():
    with chdir("./pytest_examples"):
        prepare_env()

        result = runner.invoke(app, ["svelte-check", "--target", "./issues"])
        print(result.stdout, result.stderr)
        assert result.exit_code == 1


def test_warnings():
    with chdir("./pytest_examples"):
        prepare_env()

        result = runner.invoke(app, ["svelte-check", "--target", "./warnings"])
        print(result.stdout, result.stderr)
        assert result.exit_code == 0

        result = runner.invoke(app, ["svelte-check", "--target", "./warnings", "--strict"])
        print(result.stdout, result.stderr)
        assert result.exit_code == 1


def test_custom_tsconfig():
    with chdir("./pytest_examples"):
        prepare_env()

        result = runner.invoke(app, ["svelte-check", "--target", ".", "--tsconfig", "custom_tsconfig.json", "--no-strict"])
        print(result.stdout, result.stderr)
        assert result.exit_code == 0

        result = runner.invoke(app, ["svelte-check", "--tsconfig", "custom_tsconfig.json", "--strict"])
        print(result.stdout, result.stderr)
        assert result.exit_code == 1

"""
This module contains an example of both methods of adding commands to su6.
"""
from pathlib import Path

from su6.plugins import PluginConfig, register, run_tool

from .helpers import chdir, find_project_root


@register
class SvelteCheckPluginConfig(PluginConfig):
    """
    Config without state, loads [tool.su6.demo] from pyproject.toml into self.
    """

    strict: bool = False
    tsconfig: str = "./tsconfig.json"


config = SvelteCheckPluginConfig()


@register
def install_svelte_check(target_dir: str = None) -> int:
    """
    Install the svelte-check tool using npm.
    """
    target_dir = target_dir or "./"

    with chdir(target_dir):
        return run_tool("npm", "install", "svelte-check")


@register(add_to_all=True)
def svelte_check(strict: bool = None, tsconfig: str = None, node_modules: str = None) -> int:
    """
    Run the svelte-check tool.
    """
    config.update(strict=strict, tsconfig=tsconfig)
    # svelte-check --tsconfig ./tsconfig.json --threshold error

    node_modules = node_modules or "node_modules"
    root, _ = find_project_root((node_modules,))
    executable = str(root / "node_modules/svelte-check/bin/svelte-check")

    args = []
    if config.strict:
        args.append("--fail-on-warnings")
    else:
        args.extend(["--threshold", "error"])

    if Path(config.tsconfig).exists():
        args.extend(["--tsconfig", config.tsconfig])

    return run_tool(executable, *args)

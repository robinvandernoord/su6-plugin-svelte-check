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

    target: str = "."
    node_modules: str = "./node_modules"

    strict: bool = False
    tsconfig: str = "./tsconfig.json"


config = SvelteCheckPluginConfig()


@register
def install_svelte_check(target_dir: str = None) -> int:
    """
    Install the svelte-check tool using npm.
    """
    config.update(target=target_dir)

    with chdir(config.target):
        return run_tool("npm", "install", "svelte-check")


@register(add_to_all=True)
def svelte_check(target: str = None, strict: bool = None, tsconfig: str = None, node_modules: str = None) -> int:
    """
    Run the svelte-check tool.
    """
    config.update(strict=strict, tsconfig=tsconfig, target=target, node_modules=node_modules)
    # svelte-check --tsconfig ./tsconfig.json --threshold error

    root, _ = find_project_root((config.node_modules,))
    executable = str(root / "node_modules/svelte-check/bin/svelte-check")

    args = ["--workspace", config.target]
    if config.strict:
        args.append("--fail-on-warnings")
    else:
        args.extend(["--threshold", "error"])

    if Path(config.tsconfig).exists():
        args.extend(["--tsconfig", config.tsconfig])

    return run_tool(executable, *args)

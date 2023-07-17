"""
This module contains an example of both methods of adding commands to su6.
"""
from pathlib import Path

from su6.plugins import PluginConfig, register, run_tool

from .find_project_root import find_project_root


@register
class SvelteCheckPluginConfig(PluginConfig):
    """
    Config without state, loads [tool.su6.demo] from pyproject.toml into self.
    """

    strict: bool = False
    tsconfig: str = "./tsconfig.json"


config = SvelteCheckPluginConfig()


@register(add_to_all=True)
def svelte_check(strict: bool = None, tsconfig: str = None) -> int:
    """
    Register a top-level command.

    @register works without ()
    """
    config.update(strict=strict, tsconfig=tsconfig)
    # svelte-check --tsconfig ./tsconfig.json --threshold error
    root, _ = find_project_root(("node_modules",))
    executable = str(root / "node_modules/svelte-check/bin/svelte-check")

    args = []
    if config.strict:
        args.append("--fail-on-warnings")
    else:
        args.extend(["--threshold", "error"])

    if Path(config.tsconfig).exists():
        args.extend(["--tsconfig", config.tsconfig])

    return run_tool(executable, *args)

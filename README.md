# su6-plugin-svelte-check

Plugin for [su6](https://github.com/trialandsuccess/su6) that adds `svelte-check` functionality.

## Installation
```bash
pip install su6-plugin-svelte-check
# or
pip install su6[svelte-check]
```

## Usage

```bash
# optionally, if svelte-check isn't installed yet:
su6 install-svelte-check

su6 svelte-check
```

### pyproject.toml
(all keys are optional, and also usable as flags to `svelte-check` (e.g. `--strict` or `--target ./path/to/files`))
```toml
[tool.su6.prettier]
target = "./path/to/svelte/files"
node_modules = "./path/to/node_modules"

strict = true | false
tsconfig = "./path/to/tsconfig.json"
```


## License

`su6-plugin-svelte-check` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.

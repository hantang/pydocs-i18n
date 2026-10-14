# MkDocs<sup>※</sup> static i18n plugin

*The plugin that helps you support multiple language versions of your site / documentation.*

Fork of [ultrabug/mkdocs-static-i18n](https://github.com/ultrabug/mkdocs-static-i18n),
extended to **properdocs** with the **materialx** theme.

## Compatibility

| Engine | Theme | Extra |
| --- | --- | --- |
| `mkdocs<=1.6.1` | `mkdocs-material<9.7.2` | `[material]` |
| `properdocs>=1.6.5` | `mkdocs-materialx>=10.0.0` | `[materialx]` |

> [!WARNING]
>
> **Install only one theme per environment.** 
> `mkdocs-material` and `mkdocs-materialx` ship the same `material/` package and 
> both register the theme names `material` and `materialx`, so
> whichever is installed last silently overwrites the other.

```shell
pip install "mkdocs-static-i18n[material] @ git+https://github.com/hantang/pydocs-i18n"
pip install "mkdocs-static-i18n[materialx] @ git+https://github.com/hantang/pydocs-i18n"
```

The plugin configuration is identical on both engines; only the theme and the `search` options differ.

## :warning: material vs materialx

Both distributions install into the very same `material/` package directory, so they cannot
coexist. When both are installed you will see:

- `mkdocs + material` renders **exactly** like `properdocs + materialx` (both use the same `material.templates`),
- the **search box disappears** — the installed `partials/header.html` renders it only when the
  search plugin is registered under its own name (`material/search` vs `materialx/search`).

Keep one theme per virtualenv:

```shell
python -m venv .venv            && .venv/bin/pip install -e ".[material]"
python -m venv .venv-properdocs && .venv-properdocs/bin/pip install -e ".[materialx]"
```

## Development

The project is managed with [`hatch`](https://hatch.pypa.io/1.9/install/#gui-installer).
Tests and lint:

```shell
hatch run test:test
hatch run style:check
```

Serve the documentation — one environment per engine, never both in one:

```shell
hatch run doc:serve      # mkdocs + mkdocs-material
hatch run doc2:serve     # properdocs + mkdocs-materialx
```

Without `hatch`:

```shell
python -m venv .venv            && .venv/bin/pip install -e ".[material]"
python -m venv .venv-properdocs && .venv-properdocs/bin/pip install -e ".[materialx]"

.venv/bin/mkdocs serve
.venv-properdocs/bin/properdocs serve
```

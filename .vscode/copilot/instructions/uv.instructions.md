---
applyTo: '**'
---

**PEP8/257/484 • Python 3.13 • uv • pyproject.toml**

1. **Versões**
   `uv python install|list|uninstall <versão>`

2. **Venv**
   `uv venv` [activate|remove|list]

3. **Pacotes**
   `uv pip install|uninstall|list`
   `uv pip compile -o <lock> <requirements.txt>`
   `uv pip sync <lock>`

4. **Projeto**
   `uv init [nome]`
   `uv add|remove [--dev] <pacote>`
   `uv lock`
   `uv run -- <comando>`

5. **Utilitários**
   `uv self update`
   `uv doctor`
   `uvx <ferramenta> [args]`

6. **Ruff**
   Rust lint+fmt (Flake8+isort+Black)
   `ruff check [path] [--fix|--watch]`
   `ruff format [path] [--check]`
   config em [ruff.toml](./ruff.toml) ou em `[tool.ruff.lint]` & `[tool.ruff.format]` no [pyproject.toml](./pyproject.toml)

7. **Docs**
   • [uv](https://docs.astral.sh/uv/)
   • [ruff](https://docs.astral.sh/ruff/)

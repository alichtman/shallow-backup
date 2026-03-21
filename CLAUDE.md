# CLAUDE.md — shallow-backup

## Project Overview

**shallow-backup** is a CLI backup tool for macOS and Linux that backs up dotfiles, app configs, installed packages, and fonts — with git integration and secret detection. Written in Python 3, developed with 3.12.

## Quick Reference

Commands sourced from `docs/development-guide.md` and verified against `Pipfile` / `setup.py`. All commands below run inside `pipenv shell` or prefixed with `pipenv run`.

```bash
# Dev environment setup (docs/development-guide.md)
pipenv shell
pipenv install --dev

# Run from source
python3 -m shallow_backup

# Install as editable package
pip install -e .

# Run tests
pytest

# Run tests with coverage (note: some tests may fail with coverage — see docs/development-guide.md)
py.test --cov --cov-report html:code_coverage

# Interactive mode
shallow-backup

# Full backup
shallow-backup --backup-all

# Dry run
shallow-backup --dry-run
```

## Architecture

### Entry Point

`shallow_backup/__main__.py` — Click-based CLI. All flags map to backup/reinstall operations or config management. Entry point registered in `setup.py` as `shallow-backup=shallow_backup.__main__:cli`.

### Module Map

```
shallow_backup/
├── __main__.py        # CLI entry point (Click command)
├── backup.py          # backup_dotfiles(), backup_configs(), backup_packages(), backup_fonts()
├── reinstall.py       # reinstall_dots_sb(), reinstall_configs_sb(), reinstall_packages_sb(), reinstall_fonts_sb()
├── config.py          # JSON config file management (load, write, defaults)
├── git_wrapper.py     # Git init, commit, push, trufflehog hook installation
├── utils.py           # Shell commands, file ops, path helpers, condition evaluation
├── prompts.py         # Interactive menus (inquirer-based)
├── printing.py        # Colored terminal output helpers
├── constants.py       # ProjInfo class (version, author, URLs, ASCII logo)
├── compatibility.py   # OS-specific paths (macOS vs Linux)
└── upgrade.py         # Config version compatibility checking
```

### Key Flows

**Backup:** CLI args or interactive menu → create/verify backup dir → run selected backup functions → git add/commit/push with trufflehog pre-commit hook.

**Reinstall:** Read backup dir → evaluate per-file reinstall conditions → copy files back to original locations. Absolute paths stored with `:` prefix in config.

**Dotfile backup** uses multiprocessing for parallel file copying. Supports conditional backup/reinstall via bash expressions in config (`backup_condition` / `reinstall_condition`).

### Config File

JSON config at `$SHALLOW_BACKUP_CONFIG_DIR/shallow-backup.json`, falling back to `$XDG_CONFIG_HOME/shallow-backup.json`, then `~/.config/shallow-backup.json`.

Key fields: `backup_path`, `dotfiles` (with optional conditions), `config_mapping`, `root-gitignore`, `dotfiles-gitignore`.

### Dependencies

- `click` — CLI framework
- `inquirer` — interactive prompts
- `colorama` — colored output
- `gitpython` — git operations
- `trufflehog` — secret detection (pre-commit hook, required)

## Code Style

- **Indentation:** Tabs (width 4). PRs with indentation changes will not be merged.
- **Formatter:** Black (enforced via GitHub Actions)
- **Style:** PEP8 generally, but readability > strict compliance
- **Files:** Must end with a newline

## Testing

Tests live in `tests/`. They use temp directories under `~/SHALLOW-BACKUP-TEST-DIRECTORY` and clean up after themselves. All existing tests must pass before PRs are opened.

## Output Directory Structure

```
<backup_path>/
├── dotfiles/       # Home-relative and absolute-path dotfiles
├── configs/        # App configs (VSCode, Sublime, Terminal.app)
├── packages/       # Package lists (brew, pip, npm, cargo, gem, etc.)
└── fonts/          # .ttf and .otf files
```

## Color Conventions

- **Red:** Errors, dangerous actions
- **Green:** Prompts
- **Yellow:** Git operations
- **Blue:** Status messages

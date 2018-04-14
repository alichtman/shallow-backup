# shallow-backup

`shallow-backup` is designed to make it incredibly simple for developers to document their Mac configurations.

![GIF demo](img/demo_faster.gif)

`shallow-backup` makes copies of your `dotfiles` and `fonts`, and documents your package manager install lists in `.txt` format.

#### Example Use Case
---

Instead of backing up your `brew` / `npm` / `pip` / `whatever package manager` library in a system image, which may occupy GBs of space, use `shallow-backup` to create lists of the packages installed, which takes up minimal space and can be easily distributed, saved, or transported.

#### Usage
---

```
Usage: shallow-backup.py [OPTIONS]

  Easily create text documentation of installed applications, dotfiles, and
  more.

Options:
  -complete        Backup everything.
  -dotfiles        Create backup of dotfiles.
  -fonts           Create backup of installed fonts.
  -installs        Create backup of installs.
  -old_path        Decline setting new backup directory path.
  --new_path TEXT  Input a new backup directory path.
  -delete_config   Remove config file.
  -v               Display version and author information and exit.
  -help, -h        Show this message and exit.
```

**Example Commands**

+ `$ shallow-backup` -- Launch interactive backup process.
+ `$ shallow-backup -old_path -complete` -- Complete backup to path stored in `.shallow-backup`.
+ `$ shallow-backup -new_path backup_dir_to_be_created -fonts` -- Back up fonts in `backup_dir_to_be_created` directory.

**Output Structure**

```
backup_directory
├── dotfiles
│   ├── bashrc.txt
│   ├── pypirc.txt
│   ├── ssh
│   │   └── known_hosts
│   ├── vim
│   └── zshrc.txt
├── fonts
│   ├── AllerDisplay.ttf
│   ├── Aller_Bd.ttf
│   ├── Aller_BdIt.ttf
│   ├── Aller_It.ttf
│      .........
│   ├── Ubuntu\ Mono\ derivative\ Powerline\ Bold\ Italic.ttf
│   ├── Ubuntu\ Mono\ derivative\ Powerline\ Bold.ttf
│   ├── Ubuntu\ Mono\ derivative\ Powerline\ Italic.ttf
│   ├── Ubuntu\ Mono\ derivative\ Powerline.ttf
│   └── installed_fonts.txt
└── installs
    ├── applications_list.txt
    ├── brew_cask_list.txt
    ├── brew_list.txt
    ├── gem_list.txt
    ├── npm_list.txt
    └── pip_list.txt

5 directories, 214 files
```

**Reinstalling is easy!**

Just run `$ package_manager install package_manager_list.txt`.

For example, `$ brew install brew_list.txt` would reinstall all brew packages listed in `brew_list.txt`.

**What can I back up?**
---

**Dotfiles**

Copies the following files into a nested `dotfiles` directory.

1. `.pypirc`
1. `.ssh `
1. `.vim`
1. `.zshrc`

**Package Manager Install Lists**

Creates install lists for the following package managers in a nested `installs` directory.

1. `brew`
1. `brew cask`
1. `npm`
1. `gem`
1. `pip`
1. System `Applications` directory

**Fonts**

Copy all fonts from `~/Library/Fonts` into a nested `fonts` directory.

**Installation Options**
---

1. Install with [`pip`](https://pypi.org/project/shallow-backup/)
    + `$ pip install shallow-backup`
    + `$ shallow-backup`

2. Download the `shallow-backup` binary from Releases tab.

**How to Contribute**
---

1. Clone repo and create a new branch: `$ git checkout https://github.com/alichtman/shallow-backup -b name_for_new_branch`.
2. Make changes and test
3. Submit Pull Request with comprehensive description of changes

# shallow-backup

`shallow-backup` is designed to make it incredibly simple for developers to document their Mac configurations.

**TODO: INSERT DEMO HERE**

`shallow-backup` makes copies of your `dotfiles`, package and application install lists, and font lists in `.txt` format.

#### Example Use Case
---

Instead of backing up your `brew` / `npm` / `pip` / `whatever package manager` library in a system image, which may occupy GBs of space, use `shallow-backup` to create lists of the packages installed, which takes up minimal space and can be easily distributed, saved, or transported.

#### Usage
---

```
Usage: shallow-backup.py [OPTIONS]

  Easily create text documentation of installed applications, dotfiles, and more.

Options:
  -complete  Backup everything.
  -dotfiles  Create backup folder of dotfiles.
  -installs  Create backup text files of app install lists.
  -v         Display version and author information and exit.
  -help, -h  Show this message and exit.
```

**Reinstalling is easy!**

Just run `$ package_manager install package_manager_list.txt`.

For example, `$ brew install brew_list.txt` would reinstall all brew packages listed in `brew_list.txt`.

**What can I back up?**
---

**dotfiles**

Copies the following files into a nested `dotfiles` directory.

1. `.pypirc`
1. `.ssh `
1. `.vim`
1. `.zshrc`

**installs**

Creates install lists for the following package managers in a nested `installs` directory.

1. `brew`
1. `brew cask`
1. `npm`
1. `gem`
1. `pip`
1. System `Applications` directory

**fonts**

Creates a list of fonts from `~/Library/Fonts` in a nested `fonts` directory.

**Installation Options**
---

1. Install with [`pip`](https://pypi.org/project/shallowBackup/)
    + `$ pip install shallowBackup`
    + `$ shallowBackup`

2. Download the `shallowBackup` binary from Releases tab.

**How to Contribute**
---

1. Clone repo and create a new branch: `$ git checkout https://github.com/alichtman/shallowBackup -b name_for_new_branch`.
2. Make changes and test
3. Submit Pull Request with comprehensive description of changes

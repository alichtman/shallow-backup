# shallow-backup

`shallow-backup` is a CLI designed to make documenting Mac configurations incredibly simple.

**INSERT DEMO HERE**

`shallow-backup` gets up-to-date copies of your `dotfiles` and gathers package and application install lists in text files.

**Remember to back up these output directories!**

To reinstall applications from the lists created, just run `$ package_manager install package_manager_list.txt`, where `package-manager` is a variable defined by the user. Additionally, you will get up-to-date versions of the packages when you reinstall. Reinstalling is as easy as `$ brew install brew_list.txt`.

#### Example Use Case

Instead of backing up your brew/npm/pip/etc library in a system image, which may occupy GBs of space, use `shallow-backup` to create lists of the packages installed, which will occupy only KBs and can be transported much more easily.

#### Usage

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

**dotfiles**

Creates copies of the following files in a nested `dotfiles` directory.

1. `.pypirc`
1. `.ssh `
1. `.vim`
1. `.zshrc`

**installs**

Documents install lists in text files in a nested `installs` directory.

1. `brew`
1. `brew cask`
1. `npm`
1. `gem`
1. `pip`
1. System `Applications` directory

#### Installation

1. Pip (Coming soon!)
2. Github Releases (Coming soon!)
3. Homebrew (Coming soon!)

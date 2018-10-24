# shallow-backup

[![Downloads](http://pepy.tech/badge/shallow-backup)](http://pepy.tech/count/shallow-backup)
[![Build Status](https://travis-ci.com/alichtman/shallow-backup.svg?branch=master)](https://travis-ci.com/alichtman/shallow-backup)

`shallow-backup` lets you easily create lightweight backups of installed packages, applications, fonts and dotfiles, and automatically push them to a remote Git repository.

![GIF demo](img/demo_faster.gif)

Contents
========

 * [Installation](#installation)
 * [Usage](#usage)
 * [What can I back up?](#what-can-i-back-up)
 * [Customization](#customization)
 * [Use Cases](#use-cases)
 * [Output Structure](#output-structure)
 * [Inspiration](#inspiration)
 * [Want to contribute?](#want-to-contribute)

### Installation
---

1. Install with [`pip3`](https://pypi.org/project/shallow-backup/)
    + `$ pip3 install shallow-backup`
    + `$ shallow-backup`

2. Download the `shallow-backup` binary from Releases tab.

### Usage
---

To start the interactive program, simply run `$ shallow-backup`.

`shallow-backup` was built with scripting in mind. Every feature that's supported in the interactive program is supported with command line args.

```shell
Usage: shallow_backup.py [OPTIONS]

  Easily back up installed packages, dotfiles, and more. 
  You can edit which dotfiles are backed up in ~/.shallow-backup.

Options:
  --add <CHOICE TEXT>...  Add path (relative to home dir) to be backed up. Arg
                          format: [dots, configs, other] <PATH>
  --rm <CHOICE TEXT>...   Remove path (relative to home dir) from config. Arg
                          format: [dots, configs, other] <PATH>
  -show                   Show config file.
  -complete               Back up everything.
  -dotfiles               Back up dotfiles.
  -configs                Back up app config files.
  -fonts                  Back up installed fonts.
  -packages               Back up package libraries and installed
                          applications.
  -old_path               Skip setting new back up directory path.
  --new_path TEXT         Input a new back up directory path.
  --remote TEXT           Input a URL for a git repository.
  -reinstall_packages     Reinstall packages from package lists.
  -reinstall_configs      Reinstall configs from configs backup.
  -delete_config          Remove config file.
  -v                      Display version and author information and exit.
  -destroy_backup         Removes the backup directory and its content.
  -help, -h, --help       Show this message and exit.
```

### What can I back up?
---

By default, `shallow-backup` backs these up.

1. `dotfiles` and `dotfolders`.
    * `.bashrc`
    * `.bash_profile`
    * `.gitconfig`
    * `.pypirc`
    * `.shallow-backup`
    * `.ssh/`
    * `.vim/`
    * `.zshrc`

2. Development Related App Preferences
    * Atom
    * Sublime Text 2/3
    * Terminal.app
    * JetBrains IDEs
    * VS Code (Coming soon!)

3. Installed Packages
    * `Atom` Packages (`apm`)
    * `brew` and `cask`
    * `cargo`
    * `gem`
    * `pip`
    * `npm`
    * `macports`
    * `Sublime Text 2/3` Packages
    * `~/Applications/` directory (macOS only)

4. User installed `fonts`.

### Customization

If you'd like to modify which files are backed up, you have to edit the `~/.shallow-backup` file.

1. You can open this up in a regular text editor and make your changes.
2. You can use the `--add SECTION PATH` or `--rm SECTION PATH` args to modify the config file.


#### Use Cases
---

1. Reduce your backup size by compressing all package manager libraries to simple `.txt` files.
2. Easily back up your dotfiles.
3. Back up all user installed `.ttf` and `.otf` fonts from `Fontbook`.
4. Back up application preferences of Terminal and Sublime.

#### Output Structure
---

```shell
backup_dir/
├── configs
│   ├── plist
│   │   └── com.apple.Terminal.plist
│   ├── sublime_2
│   │   └── ...
│   └── sublime_3
│       └── ...
├── dotfiles
│   ├── .bash_profile
│   ├── .bashrc
│   ├── .gitconfig
│   ├── .pypirc
│   ├── .shallow-backup
│   ├── .ssh/
│   │   └── known_hosts
│   ├── .vim/
│   └── .zshrc
├── fonts
│   ├── AllerDisplay.ttf
│   ├── Aller_Bd.ttf
│   ├── Aller_BdIt.ttf
│   ├── Aller_It.ttf
│   ├── ...
│   ├── Ubuntu Mono derivative Powerline Bold Italic.ttf
│   ├── Ubuntu Mono derivative Powerline Bold.ttf
│   ├── Ubuntu Mono derivative Powerline Italic.ttf
│   └── Ubuntu Mono derivative Powerline.ttf
└── packages
    ├── apm_list.txt
    ├── brew-cask_list.txt
    ├── brew_list.txt
    ├── cargo_list.txt
    ├── gem_list.txt
    ├── installed_apps_list.txt
    ├── npm_list.txt
    ├── macports_list.txt
    ├── pip_list.txt
    └── sublime3_list.txt
```

### Inspiration
---

I back up system images of my MacBook Pro to an external SSD multiple times every week, and it always takes way too long. I wanted to speed this up, so I took a look at what was actually being backed up. I saw that my `brew`, `npm`, and `pip` libraries took up a ton more space than I imagined.

*And that's totally unnecessary.* When you back something up, you do it with the intention of being able to get back to that exact state at some point in the future. The minimum you need in order to recreate those package libraries later is just a list of the packages that are installed with each package manager. If you have these lists, restoring your system package installs is easy: `$ pip install -r pip_list.txt`, for example. 

I cut down my backup size by almost `10GB` by replacing my `pip`, `brew`, `brew cask` and `npm` libraries with simple text files. I also cut down the back up time significantly since many fewer files were being copied.

Once I'd built that functionality, I wanted to have a single backup utility for files and folders often used by developers, so I added the ability to backup `dotfiles` and `fonts`. (Note: Because just having a list of installed fonts or a list of dotfiles that exist isn't very useful, `shallow-backup` creates copies of all dotfiles and user installed fonts.)

### Want to Contribute?
---

Check out `CONTRIBUTING.md`

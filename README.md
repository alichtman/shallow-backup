# shallow-backup

`shallow-backup` lets you easily create lightweight backups of installed packages, applications, fonts and dotfiles.

![GIF demo](img/demo_faster.gif)

Contents
========

 * [Featured On](#featured-on)
 * [What can I back up?](#what-can-i-back-up)
 * [Installation](#installation)
 * [Usage](#usage)
    * [Example Commands](#example-commands)
    * [Use Cases](#use-cases)
    * [Output Structure](#output-structure)
 * [Inspiration](#inspiration)
 * [What's Next?](#whats-next)
 * [How to Contribute](#how-to-contribute)

### Featured On
---

`shallow-backup` is featured on these lists!

* [awesome-mac](https://github.com/jaywcjlove/awesome-mac)
* [open-source-mac-os-apps](https://github.com/serhii-londar/open-source-mac-os-apps)
* [tools-osx](https://github.com/morgant/tools-osx)

### What can I back up?
---

1. All `dotfiles` and `dotfolders`.
    * macOS System Preferences
    * Sublime Text Settings
    * Atom Settings
    * `.bashrc`.
    * etc.

2. Package Manager and Application `installs`.
    * `apm`
    * `brew`
    * `brew cask`
    * `gem`
    * `pip`
    * `npm`
    * `macports`
    * Sublime Text 2 and 3 packages
    * macOS `~/Applications/` directory

3. User installed `fonts`.

### Installation
---

1. Install with [`pip`](https://pypi.org/project/shallow-backup/)
    + `$ pip install shallow-backup`
    + `$ sudo shallow-backup`

2. Download the `shallow-backup` binary from Releases tab.

### Usage
---

```shell
Usage: shallow_backup.py [OPTIONS]

  Easily back up installed packages, dotfiles, and more.

Options:
  -complete        Back up everything.
  -dotfiles        Back up dotfiles.
  -fonts           Back up installed fonts.
  -packages        Back up package libraries and installed applications.
  -old_path        Skip setting new back up directory path.
  --new_path TEXT  Input a new back up directory path.
  -reinstall       Reinstall packages from package lists.
  -delete_config   Remove config file.
  -v               Display version and author information and exit.
  -help, -h        Show this message and exit.
```

NOTE: `shallow-backup` works best when it's populating an empty directory.

#### Example Commands
---

```shell
$ shallow-backup # Launch interactive CLI backup process
$ shallow-backup -old_path -complete # Make complete backup using same path as in config file
$ shallow-backup -new_path new_backup_dir -fonts # Back up fonts using path: `/new_backup_dir/`
```

#### Use Cases
---

1. Reduce your backup size by compressing all package manager libraries to `.txt` files.
2. Easily back up your dotfiles, Sublime Text settings and Atom config.
3. Back up all user installed `.ttf` and `.otf` fonts from `Fontbook`.

#### Output Structure
---

```shell
backup_dir/
├── dotfiles
│   ├── .bashrc
│   ├── .pypirc
│   ├── ...
│   ├── .ssh/
│   │   └── known_hosts
│   ├── .vim/
│   └── .zshrc
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
└── installs
    ├── apm_list.txt
    ├── brew-cask_list.txt
    ├── brew_list.txt
    ├── gem_list.txt
    ├── installed_apps_list.txt
    ├── macports_list.txt
    ├── npm_list.txt
    └── pip_list.txt

5 directories, 214 files
```

### Inspiration
---

I back up system images of my MacBook Pro to an external SSD multiple times every week, and it always takes way too long. I wanted to speed this up, so I took a look at *what was actually being backed up*. I saw that my `brew`, `npm`, and `pip` libraries took up way more memory than I imagined.

*And it's totally unnecessary!* All you need to "back up" your package installs is a list of the installed packages from each package manager. If you have these lists, restoring your system package installs is easy: `$ pip install -r pip_list.txt`, for example. Additionally, you have the added bonus of always installing up-to-date packages after an OS wipe and reinstall.

I could now safely cut down my backup size by almost `10GB` by replacing my `pip`, `brew`, `brew cask` and `npm` install libraries with simple text files, which cuts down the back up time significantly.

Once I'd built that functionality, I wanted to have a single backup utility for files and folders often used by developers, so I added the ability to backup `dotfiles` and `fonts`. (Note: Because just having a list of installed fonts or a list of dotfiles that exist isn't very useful, `shallow-backup` creates copies of all dotfiles and user installed fonts.)


### What's Next?
---

1. MacOS GUI.
2. More optimization.

### How to Contribute
---

1. Clone repo and create a new branch: `$ git checkout https://github.com/alichtman/shallow-backup -b name_for_new_branch`.
2. Make changes and test
3. Submit Pull Request with comprehensive description of changes

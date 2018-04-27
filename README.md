# shallow-backup

`shallow-backup` lets you easily create lightweight backups of installed packages, applications, fonts and dotfiles.

![GIF demo](img/demo_faster.gif)

### Featured On
---

`shallow-backup` is featured on these lists!

* [awesome-mac](https://github.com/jaywcjlove/awesome-mac)
* [open-source-mac-os-apps](https://github.com/serhii-londar/open-source-mac-os-apps)
* [tools-osx](https://github.com/morgant/tools-osx)

### Inspiration
---

I back up system images of my MacBook Pro to an external SSD multiple times every week, and it always takes way too long. I wanted to speed this up, so I took a look at *what was actually being backed up*. I saw that my `brew`, `npm`, and `pip` libraries took up way more memory than I imagined.

*And it's totally unnecessary!* All you need to "back up" your package installs is a list of the installed packages from each package manager. If you have these lists, restoring your system package installs is easy: `$ pip install -r pip_list.txt`, for example. Additionally, you have the added bonus of always installing up-to-date packages after an OS wipe and reinstall.

I could now safely cut down my backup size by almost `10GB` by replacing my `pip`, `brew`, `brew cask` and `npm` install libraries with simple text files, which cuts down the back up time significantly.

Once I'd built that functionality, I wanted to have a single backup utility for files and folders often used by developers, so I added the ability to backup `dotfiles` and `fonts`. (Note: Because just having a list of installed fonts or a list of dotfiles that exist isn't very useful, `shallow-backup` creates copies of all dotfiles and user installed fonts.)

### Usage
---

```shell
Usage: shallow_backup.py [OPTIONS]

  Easily create text documentation of installed applications, dotfiles, and
  more.

Options:
  -complete        Back up everything.
  -dotfiles        Back up dotfiles.
  -fonts           Back up installed fonts.
  -installs        Back up package and application installs.
  -old_path        Skip setting new back up directory path.
  --new_path TEXT  Input a new back up directory path.
  -delete_config   Remove config file.
  -v               Display version and author information and exit.
  -h, -help        Show this message and exit.
```

#### Use Cases

1. Reduce your system image size by using `shallow-backup` to compress `x package manager's` library.
2. Easily back up your dotfiles.
3. Back up the `.ttf` and `.otf` fonts you've imported to `Fontbook`.

#### Example Commands

```shell
$ sudo shallow-backup # Launch interactive backup process
$ sudo shallow-backup -old_path -complete # Make complete backup using same path as in config file
$ sudo shallow-backup -new_path new_backup_dir -fonts # Back up fonts using path: `/new_backup_dir/`
```

#### Output Structure

```shell
backup_dir/
├── dotfiles
│   ├── bashrc.txt
│   ├── pypirc.txt
│   ├── ...
│   ├── ssh
│   │   └── known_hosts
│   ├── vim
│   └── zshrc.txt
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
    ├── applications_list.txt
    ├── brew_cask_list.txt
    ├── ...
    ├── gem_list.txt
    ├── npm_list.txt
    └── pip_list.txt

5 directories, 214 files
```

### What can I back up?
---

1. All `dotfiles` and `dotfolders`.

2. Package Manager and Application `installs`.
    * `brew`
    * `brew cask`
    * `gem`
    * `pip`
    * `npm`
    * `macports`
    * macOS `~/Applications/` directory

3. User installed `fonts`.

### Installation Options
---

1. Install with [`pip`](https://pypi.org/project/shallow-backup/)
    + `$ pip install shallow-backup`
    + `$ sudo shallow-backup`

2. Download the `shallow-backup` binary from Releases tab.


### What's Next?
---

1. Automatic restic backup.
2. MacOS GUI for non-CLI users.

### How to Contribute
---

1. Clone repo and create a new branch: `$ git checkout https://github.com/alichtman/shallow-backup -b name_for_new_branch`.
2. Make changes and test
3. Submit Pull Request with comprehensive description of changes

# Change Log

## [Unreleased](https://github.com/alichtman/shallow-backup/tree/HEAD)

[Full Changelog](https://github.com/alichtman/shallow-backup/compare/v1.3...HEAD)

**Fixed bugs:**

- It doesn't backup global npm packages? [\#61](https://github.com/alichtman/shallow-backup/issues/61)
- Error? Or do I just not know how to use this. [\#54](https://github.com/alichtman/shallow-backup/issues/54)

**Closed issues:**

- Add config file for dotfiles and directories to back up. [\#76](https://github.com/alichtman/shallow-backup/issues/76)
- Automatically create .gitignore to protect private files [\#71](https://github.com/alichtman/shallow-backup/issues/71)
- Don't delete the .git directory when creating a new backup [\#68](https://github.com/alichtman/shallow-backup/issues/68)
- Extract lists of files/directories that don't change to a constants file [\#67](https://github.com/alichtman/shallow-backup/issues/67)
- Add Pipfile for Pipenv [\#64](https://github.com/alichtman/shallow-backup/issues/64)
- Default install missing ConfigParser dependency? [\#62](https://github.com/alichtman/shallow-backup/issues/62)
- No module named configparser [\#60](https://github.com/alichtman/shallow-backup/issues/60)
- Could shallow-backup integrate with git for backup? [\#57](https://github.com/alichtman/shallow-backup/issues/57)
- README [\#56](https://github.com/alichtman/shallow-backup/issues/56)
- Make shallow-backup compatible with Python 2.7 [\#55](https://github.com/alichtman/shallow-backup/issues/55)
- Remove XCode Backup [\#53](https://github.com/alichtman/shallow-backup/issues/53)
- Homebrew Release [\#6](https://github.com/alichtman/shallow-backup/issues/6)

**Merged pull requests:**

- Git integration for shallow-backup [\#78](https://github.com/alichtman/shallow-backup/pull/78) ([alichtman](https://github.com/alichtman))
- Revert "Autoformat all Python in repo with `autopep8`" [\#75](https://github.com/alichtman/shallow-backup/pull/75) ([alichtman](https://github.com/alichtman))
- Make npm backup global packages only [\#74](https://github.com/alichtman/shallow-backup/pull/74) ([jasikpark](https://github.com/jasikpark))
- Autoformat all Python in repo with `autopep8` [\#70](https://github.com/alichtman/shallow-backup/pull/70) ([jasikpark](https://github.com/jasikpark))
- Added Pipfile [\#66](https://github.com/alichtman/shallow-backup/pull/66) ([rmad17](https://github.com/rmad17))
- Add -configs mode. [\#63](https://github.com/alichtman/shallow-backup/pull/63) ([schilli91](https://github.com/schilli91))

## [v1.3](https://github.com/alichtman/shallow-backup/tree/v1.3) (2018-05-30)
[Full Changelog](https://github.com/alichtman/shallow-backup/compare/v1.2...v1.3)

## [v1.2](https://github.com/alichtman/shallow-backup/tree/v1.2) (2018-05-30)
[Full Changelog](https://github.com/alichtman/shallow-backup/compare/v1.0...v1.2)

**Fixed bugs:**

- Don't store embedded git repos [\#44](https://github.com/alichtman/shallow-backup/issues/44)
- Check if package manager installed before creating backup [\#41](https://github.com/alichtman/shallow-backup/issues/41)
- Running with sudo causes this error for homebrew and pip [\#39](https://github.com/alichtman/shallow-backup/issues/39)

**Closed issues:**

- Cargo backup list [\#46](https://github.com/alichtman/shallow-backup/issues/46)
- Don't back up .pyc files [\#43](https://github.com/alichtman/shallow-backup/issues/43)
- GUI [\#42](https://github.com/alichtman/shallow-backup/issues/42)
- Fix Permissions Error on Preferences [\#40](https://github.com/alichtman/shallow-backup/issues/40)
- dev\_dots option to only backup dev-related dotfiles [\#33](https://github.com/alichtman/shallow-backup/issues/33)
- Don't copy atom packages [\#32](https://github.com/alichtman/shallow-backup/issues/32)
- Upgrade from cp to rsync for dotfiles [\#31](https://github.com/alichtman/shallow-backup/issues/31)
- Automatic backup to restic [\#26](https://github.com/alichtman/shallow-backup/issues/26)
- Submit to same lists as stronghold [\#14](https://github.com/alichtman/shallow-backup/issues/14)

**Merged pull requests:**

- Fix dotfolder bug [\#52](https://github.com/alichtman/shallow-backup/pull/52) ([alichtman](https://github.com/alichtman))
- Add cargo backup [\#51](https://github.com/alichtman/shallow-backup/pull/51) ([alichtman](https://github.com/alichtman))
- Clean up empty package list files [\#50](https://github.com/alichtman/shallow-backup/pull/50) ([alichtman](https://github.com/alichtman))

## [v1.0](https://github.com/alichtman/shallow-backup/tree/v1.0) (2018-05-14)
[Full Changelog](https://github.com/alichtman/shallow-backup/compare/v0.4...v1.0)

**Closed issues:**

- Add reinstall option [\#37](https://github.com/alichtman/shallow-backup/issues/37)
- Backup Sublime Settings [\#36](https://github.com/alichtman/shallow-backup/issues/36)
- Add System Preferences [\#35](https://github.com/alichtman/shallow-backup/issues/35)
- Add XCode UserData [\#34](https://github.com/alichtman/shallow-backup/issues/34)
- Application Preferences and Config Files [\#30](https://github.com/alichtman/shallow-backup/issues/30)
- Backup Browser Prefs [\#29](https://github.com/alichtman/shallow-backup/issues/29)
- "The Idea" -\> "Inspiration" [\#28](https://github.com/alichtman/shallow-backup/issues/28)
- Add option to encrypt decrypt git repository [\#27](https://github.com/alichtman/shallow-backup/issues/27)
- backup native app prefs [\#25](https://github.com/alichtman/shallow-backup/issues/25)
- backup chrome prefs [\#24](https://github.com/alichtman/shallow-backup/issues/24)
- backup firefox prefs [\#23](https://github.com/alichtman/shallow-backup/issues/23)
- Backup all files that begin with dot, like literally all dotfiles [\#21](https://github.com/alichtman/shallow-backup/issues/21)
- Add jetbrains config files [\#20](https://github.com/alichtman/shallow-backup/issues/20)
- Add Atom packages list [\#19](https://github.com/alichtman/shallow-backup/issues/19)
- Add sublime text packages list [\#18](https://github.com/alichtman/shallow-backup/issues/18)
- Coverage for other package managers [\#2](https://github.com/alichtman/shallow-backup/issues/2)

## [v0.4](https://github.com/alichtman/shallow-backup/tree/v0.4) (2018-04-14)
**Closed issues:**

- uninstall option [\#17](https://github.com/alichtman/shallow-backup/issues/17)
- Copy font .otf and .ttf files, not just a list of names [\#16](https://github.com/alichtman/shallow-backup/issues/16)
- figure out how to set pypi name to shallow-backup [\#15](https://github.com/alichtman/shallow-backup/issues/15)
- README Updates [\#13](https://github.com/alichtman/shallow-backup/issues/13)
- Protection for text\_backup dir [\#12](https://github.com/alichtman/shallow-backup/issues/12)
- PyPi [\#11](https://github.com/alichtman/shallow-backup/issues/11)
- setup.py descriptors [\#9](https://github.com/alichtman/shallow-backup/issues/9)
- Add -reinstall cli option [\#8](https://github.com/alichtman/shallow-backup/issues/8)
- Add CLI [\#7](https://github.com/alichtman/shallow-backup/issues/7)
- README [\#5](https://github.com/alichtman/shallow-backup/issues/5)
- Not backing up all fonts [\#4](https://github.com/alichtman/shallow-backup/issues/4)
- better name pls [\#3](https://github.com/alichtman/shallow-backup/issues/3)
- Better README [\#1](https://github.com/alichtman/shallow-backup/issues/1)



\* *This Change Log was automatically generated by [github_changelog_generator](https://github.com/skywinder/Github-Changelog-Generator)*
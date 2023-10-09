# Changelog

## [v6.1](https://github.com/alichtman/shallow-backup/tree/v6.1) (2023-10-09)

[Full Changelog](https://github.com/alichtman/shallow-backup/compare/v6.0...v6.1)

**Fixed bugs:**

- 🙋‍♀️ running shallow-backup interactively \(backup all\) does not save to the folder [\#282](https://github.com/alichtman/shallow-backup/issues/282)
- Git commit breaks sometimes if submodules exist [\#229](https://github.com/alichtman/shallow-backup/issues/229)
- npm packages backup: Doesn't handle scopes, fails with unmet peer dependencies [\#226](https://github.com/alichtman/shallow-backup/issues/226)

**Merged pull requests:**

- Fix: Update README.md file to reflect work done on issue \#328 [\#330](https://github.com/alichtman/shallow-backup/pull/330) ([BreakingPitt](https://github.com/BreakingPitt))

## [v6.0](https://github.com/alichtman/shallow-backup/tree/v6.0) (2023-08-29)

[Full Changelog](https://github.com/alichtman/shallow-backup/compare/v5.3...v6.0)

**Closed issues:**

- Convert options from `-` to `--` where it makes sense [\#328](https://github.com/alichtman/shallow-backup/issues/328)
- `backup-fonts` is in the wrong spot in the help menu [\#325](https://github.com/alichtman/shallow-backup/issues/325)
- KeyError: 'all' on commit procedure [\#306](https://github.com/alichtman/shallow-backup/issues/306)

**Merged pull requests:**

- fix: Convert options from - to -- where it makes sense [\#329](https://github.com/alichtman/shallow-backup/pull/329) ([BreakingPitt](https://github.com/BreakingPitt))
- Move backup-fonts to the right spot in the help menu [\#327](https://github.com/alichtman/shallow-backup/pull/327) ([alichtman](https://github.com/alichtman))
- Create black.yml [\#326](https://github.com/alichtman/shallow-backup/pull/326) ([alichtman](https://github.com/alichtman))
-  Deprecate apm backups and restores [\#320](https://github.com/alichtman/shallow-backup/pull/320) ([alichtman](https://github.com/alichtman))
- Bump cryptography from 38.0.4 to 39.0.1 [\#318](https://github.com/alichtman/shallow-backup/pull/318) ([dependabot[bot]](https://github.com/apps/dependabot))
- Bump gitpython from 3.1.29 to 3.1.30 [\#317](https://github.com/alichtman/shallow-backup/pull/317) ([dependabot[bot]](https://github.com/apps/dependabot))
- Fix npm backup issue \#226 [\#315](https://github.com/alichtman/shallow-backup/pull/315) ([nick-The-One](https://github.com/nick-The-One))

## [v5.3](https://github.com/alichtman/shallow-backup/tree/v5.3) (2022-12-14)

[Full Changelog](https://github.com/alichtman/shallow-backup/compare/v5.2...v5.3)

## [v5.2](https://github.com/alichtman/shallow-backup/tree/v5.2) (2022-06-19)

[Full Changelog](https://github.com/alichtman/shallow-backup/compare/v5.1...v5.2)

**Fixed bugs:**

- Support default branches other than `master` [\#305](https://github.com/alichtman/shallow-backup/issues/305)

**Closed issues:**

- Add warning if shallow-backup.conf is writable by all [\#309](https://github.com/alichtman/shallow-backup/issues/309)
- `shallow-backup` crashes if repo can't be created [\#308](https://github.com/alichtman/shallow-backup/issues/308)

**Merged pull requests:**

- Add warning if config is vulnerable to exploitation [\#310](https://github.com/alichtman/shallow-backup/pull/310) ([alichtman](https://github.com/alichtman))
- fix: push to different branch names [\#307](https://github.com/alichtman/shallow-backup/pull/307) ([jnoortheen](https://github.com/jnoortheen))

## [v5.1](https://github.com/alichtman/shallow-backup/tree/v5.1) (2021-12-11)

[Full Changelog](https://github.com/alichtman/shallow-backup/compare/v5.0.1...v5.1)

**Fixed bugs:**

- Uncaught `shutil.Error` if file is not found during backup [\#298](https://github.com/alichtman/shallow-backup/issues/298)
- fonts with spaces in filename are not backed up. [\#280](https://github.com/alichtman/shallow-backup/issues/280)
- Failing npm Reinstall [\#148](https://github.com/alichtman/shallow-backup/issues/148)
- Back up gemlist properly [\#38](https://github.com/alichtman/shallow-backup/issues/38)

**Closed issues:**

- Bug - dotfiles fail to save `[Errno 2] No such file or directory:` [\#297](https://github.com/alichtman/shallow-backup/issues/297)
- Error when trying to show current backup: AttributeError: 'list' object has no attribute 'items'~ [\#295](https://github.com/alichtman/shallow-backup/issues/295)
- npm backup overwriting pip3 backup [\#284](https://github.com/alichtman/shallow-backup/issues/284)
- clarify install instructions [\#283](https://github.com/alichtman/shallow-backup/issues/283)
- Allow keys to be missing from the config to declutter [\#279](https://github.com/alichtman/shallow-backup/issues/279)
- Add config key for dotfiles to not reinstall [\#252](https://github.com/alichtman/shallow-backup/issues/252)
- Backup brew tap  [\#218](https://github.com/alichtman/shallow-backup/issues/218)
- Automatic archiving after a new backup [\#176](https://github.com/alichtman/shallow-backup/issues/176)

**Merged pull requests:**

- Make file copy errors user friendly [\#303](https://github.com/alichtman/shallow-backup/pull/303) ([alichtman](https://github.com/alichtman))
- Catch shutil.Error if file is not found [\#302](https://github.com/alichtman/shallow-backup/pull/302) ([alichtman](https://github.com/alichtman))
- Clarify install instructions [\#301](https://github.com/alichtman/shallow-backup/pull/301) ([alichtman](https://github.com/alichtman))
- Make backup and reinstall condition keys optional [\#300](https://github.com/alichtman/shallow-backup/pull/300) ([alichtman](https://github.com/alichtman))
- Handle piping commands properly [\#299](https://github.com/alichtman/shallow-backup/pull/299) ([alichtman](https://github.com/alichtman))
- Update homebrew support [\#294](https://github.com/alichtman/shallow-backup/pull/294) ([tim-coutinho](https://github.com/tim-coutinho))
- Add cargo backup / reinstall [\#291](https://github.com/alichtman/shallow-backup/pull/291) ([tim-coutinho](https://github.com/tim-coutinho))
- Fix interactive backup all not working [\#287](https://github.com/alichtman/shallow-backup/pull/287) ([tim-coutinho](https://github.com/tim-coutinho))
- Fix npm backup overwriting pip3 backup [\#285](https://github.com/alichtman/shallow-backup/pull/285) ([tim-coutinho](https://github.com/tim-coutinho))

## [v5.0.1](https://github.com/alichtman/shallow-backup/tree/v5.0.1) (2020-05-14)

[Full Changelog](https://github.com/alichtman/shallow-backup/compare/v5.0.0a...v5.0.1)

**Merged pull requests:**

- Bump version to 5.0.1 [\#278](https://github.com/alichtman/shallow-backup/pull/278) ([alichtman](https://github.com/alichtman))

## [v5.0.0a](https://github.com/alichtman/shallow-backup/tree/v5.0.0a) (2020-05-13)

[Full Changelog](https://github.com/alichtman/shallow-backup/compare/v4.0.4...v5.0.0a)

**Fixed bugs:**

- Setting backup path to ~/.shallow\_backup breaks subsequent runs [\#265](https://github.com/alichtman/shallow-backup/issues/265)
- shutil.SameFileError shallow-backup.conf [\#260](https://github.com/alichtman/shallow-backup/issues/260)

**Closed issues:**

- Add `--dry_run` key to not actually copy any files on backup or reinstall [\#274](https://github.com/alichtman/shallow-backup/issues/274)
- Cannot interactively set backup path to existing backup repo [\#266](https://github.com/alichtman/shallow-backup/issues/266)
- Add tests for adding paths to config [\#249](https://github.com/alichtman/shallow-backup/issues/249)
- Run Travis on both Mac and Linux [\#197](https://github.com/alichtman/shallow-backup/issues/197)

**Merged pull requests:**

- Standardize flags [\#276](https://github.com/alichtman/shallow-backup/pull/276) ([alichtman](https://github.com/alichtman))
- Add -dry\_run flag [\#275](https://github.com/alichtman/shallow-backup/pull/275) ([alichtman](https://github.com/alichtman))
- Add conditional backup and reinstallation [\#272](https://github.com/alichtman/shallow-backup/pull/272) ([alichtman](https://github.com/alichtman))
- Refactor [\#271](https://github.com/alichtman/shallow-backup/pull/271) ([alichtman](https://github.com/alichtman))
- Be clear that changing backup path moves the folder [\#268](https://github.com/alichtman/shallow-backup/pull/268) ([ThatsJustCheesy](https://github.com/ThatsJustCheesy))
- Allow setting backup path to ~/.shallow-backup [\#267](https://github.com/alichtman/shallow-backup/pull/267) ([ThatsJustCheesy](https://github.com/ThatsJustCheesy))

## [v4.0.4](https://github.com/alichtman/shallow-backup/tree/v4.0.4) (2020-03-29)

[Full Changelog](https://github.com/alichtman/shallow-backup/compare/v4.0.3...v4.0.4)

**Fixed bugs:**

- FileNotFoundError: ~/shallow-backup/dotfiles/.gitignore [\#257](https://github.com/alichtman/shallow-backup/issues/257)

**Merged pull requests:**

- Create dotfiles dir before creating .gitignore [\#259](https://github.com/alichtman/shallow-backup/pull/259) ([alichtman](https://github.com/alichtman))
- Fix default config creation [\#258](https://github.com/alichtman/shallow-backup/pull/258) ([alichtman](https://github.com/alichtman))

## [v4.0.3](https://github.com/alichtman/shallow-backup/tree/v4.0.3) (2020-03-26)

[Full Changelog](https://github.com/alichtman/shallow-backup/compare/v4.0.2...v4.0.3)

## [v4.0.2](https://github.com/alichtman/shallow-backup/tree/v4.0.2) (2020-03-25)

[Full Changelog](https://github.com/alichtman/shallow-backup/compare/v4.0.1...v4.0.2)

**Merged pull requests:**

- Follow symlinks and avoid PermissionError when reinstalling .git repos [\#256](https://github.com/alichtman/shallow-backup/pull/256) ([alichtman](https://github.com/alichtman))

## [v4.0.1](https://github.com/alichtman/shallow-backup/tree/v4.0.1) (2020-03-25)

[Full Changelog](https://github.com/alichtman/shallow-backup/compare/v4.0...v4.0.1)

**Merged pull requests:**

- Correctly exclude files on reinstallation and add tests [\#255](https://github.com/alichtman/shallow-backup/pull/255) ([alichtman](https://github.com/alichtman))
- Avoid reinstalling img/ and README from dotfiles [\#254](https://github.com/alichtman/shallow-backup/pull/254) ([alichtman](https://github.com/alichtman))

## [v4.0](https://github.com/alichtman/shallow-backup/tree/v4.0) (2020-03-22)

[Full Changelog](https://github.com/alichtman/shallow-backup/compare/v3.4...v4.0)

**Closed issues:**

- Interface for selecting which dotfiles to back up [\#228](https://github.com/alichtman/shallow-backup/issues/228)
- Use symlinking instead of copying [\#188](https://github.com/alichtman/shallow-backup/issues/188)

**Merged pull requests:**

- Carefully reinstall .git and .gitignore files [\#251](https://github.com/alichtman/shallow-backup/pull/251) ([alichtman](https://github.com/alichtman))

## [v3.4](https://github.com/alichtman/shallow-backup/tree/v3.4) (2020-03-22)

[Full Changelog](https://github.com/alichtman/shallow-backup/compare/v3.3...v3.4)

## [v3.3](https://github.com/alichtman/shallow-backup/tree/v3.3) (2020-03-21)

[Full Changelog](https://github.com/alichtman/shallow-backup/compare/v3.2...v3.3)

**Fixed bugs:**

- Error when reinstalling all [\#216](https://github.com/alichtman/shallow-backup/issues/216)
- copytree\(\) doesn't overwrite, so reinstall sometimes fails [\#209](https://github.com/alichtman/shallow-backup/issues/209)

**Closed issues:**

- Add `--add` flag for adding new paths to be backed up [\#247](https://github.com/alichtman/shallow-backup/issues/247)
- Add Support for Hammerspoon dotfolder [\#244](https://github.com/alichtman/shallow-backup/issues/244)

**Merged pull requests:**

- Refactor --add option and bump to v3.3 [\#250](https://github.com/alichtman/shallow-backup/pull/250) ([alichtman](https://github.com/alichtman))
- Add CLI option for adding paths to config [\#248](https://github.com/alichtman/shallow-backup/pull/248) ([alichtman](https://github.com/alichtman))
- Fix IsADirectory error upon reinstallation [\#246](https://github.com/alichtman/shallow-backup/pull/246) ([alichtman](https://github.com/alichtman))

## [v3.2](https://github.com/alichtman/shallow-backup/tree/v3.2) (2019-11-17)

[Full Changelog](https://github.com/alichtman/shallow-backup/compare/v3.1...v3.2)

**Merged pull requests:**

- Move config to ~/.config/shallow-backup.conf [\#242](https://github.com/alichtman/shallow-backup/pull/242) ([alichtman](https://github.com/alichtman))

## [v3.1](https://github.com/alichtman/shallow-backup/tree/v3.1) (2019-11-15)

[Full Changelog](https://github.com/alichtman/shallow-backup/compare/v2.8...v3.1)

**Closed issues:**

- Revamp tests [\#237](https://github.com/alichtman/shallow-backup/issues/237)
- Conform to XDG spec [\#236](https://github.com/alichtman/shallow-backup/issues/236)

**Merged pull requests:**

- Respect XDG Base Directory spec [\#239](https://github.com/alichtman/shallow-backup/pull/239) ([alichtman](https://github.com/alichtman))
- Fix tests [\#238](https://github.com/alichtman/shallow-backup/pull/238) ([alichtman](https://github.com/alichtman))

## [v2.8](https://github.com/alichtman/shallow-backup/tree/v2.8) (2019-10-16)

[Full Changelog](https://github.com/alichtman/shallow-backup/compare/v2.7...v2.8)

**Closed issues:**

- Unable to run macOS [\#235](https://github.com/alichtman/shallow-backup/issues/235)

## [v2.7](https://github.com/alichtman/shallow-backup/tree/v2.7) (2019-10-08)

[Full Changelog](https://github.com/alichtman/shallow-backup/compare/v2.6...v2.7)

**Fixed bugs:**

- Handle JSON errors in the config [\#233](https://github.com/alichtman/shallow-backup/issues/233)

**Merged pull requests:**

- Config syntax error handling [\#234](https://github.com/alichtman/shallow-backup/pull/234) ([alichtman](https://github.com/alichtman))

## [v2.6](https://github.com/alichtman/shallow-backup/tree/v2.6) (2019-09-23)

[Full Changelog](https://github.com/alichtman/shallow-backup/compare/v2.4...v2.6)

**Fixed bugs:**

- Can't back up dotfiles that don't live directly inside $HOME [\#230](https://github.com/alichtman/shallow-backup/issues/230)
- Double check git commit logic [\#227](https://github.com/alichtman/shallow-backup/issues/227)

**Closed issues:**

- How do you backup minus the shallow-backup repo? [\#225](https://github.com/alichtman/shallow-backup/issues/225)

**Merged pull requests:**

- Patch failing commit behavior when submodules are present [\#232](https://github.com/alichtman/shallow-backup/pull/232) ([alichtman](https://github.com/alichtman))
- Allow backing up dotfiles outside of $HOME [\#231](https://github.com/alichtman/shallow-backup/pull/231) ([alichtman](https://github.com/alichtman))

## [v2.4](https://github.com/alichtman/shallow-backup/tree/v2.4) (2019-05-12)

[Full Changelog](https://github.com/alichtman/shallow-backup/compare/v2.3...v2.4)

**Fixed bugs:**

- Back up fonts directory  [\#219](https://github.com/alichtman/shallow-backup/issues/219)

**Closed issues:**

- When clearing old backup files, delete everything except `.git/` and `.gitignore` [\#223](https://github.com/alichtman/shallow-backup/issues/223)
- You should try asciinema instead of upload big GIF file demo [\#222](https://github.com/alichtman/shallow-backup/issues/222)
- Similar\(ish\) project to be aware of? [\#220](https://github.com/alichtman/shallow-backup/issues/220)

**Merged pull requests:**

- Don't delete .git when removing old backups [\#224](https://github.com/alichtman/shallow-backup/pull/224) ([alichtman](https://github.com/alichtman))
- No such file or directory during fonts backup [\#217](https://github.com/alichtman/shallow-backup/pull/217) ([robbixc](https://github.com/robbixc))

## [v2.3](https://github.com/alichtman/shallow-backup/tree/v2.3) (2019-01-07)

[Full Changelog](https://github.com/alichtman/shallow-backup/compare/v2.2...v2.3)

**Fixed bugs:**

- Backup pip3 packages [\#211](https://github.com/alichtman/shallow-backup/issues/211)

**Closed issues:**

- Restore VSCode backups [\#213](https://github.com/alichtman/shallow-backup/issues/213)
- Reinstall VSCode backup [\#212](https://github.com/alichtman/shallow-backup/issues/212)
- Exception handling [\#206](https://github.com/alichtman/shallow-backup/issues/206)
- Ruby gems Backup and VSCode [\#204](https://github.com/alichtman/shallow-backup/issues/204)
- Don't prompt for confirmation to delete subdir if all files in the subdir are tracked and unchanged [\#146](https://github.com/alichtman/shallow-backup/issues/146)
- VSCode Backup [\#45](https://github.com/alichtman/shallow-backup/issues/45)

**Merged pull requests:**

- Exception handling [\#207](https://github.com/alichtman/shallow-backup/pull/207) ([ibokuri](https://github.com/ibokuri))
- Added VSCode settings and extensions backup/reinstall, pip3 backup. [\#205](https://github.com/alichtman/shallow-backup/pull/205) ([AlexanderProd](https://github.com/AlexanderProd))

## [v2.2](https://github.com/alichtman/shallow-backup/tree/v2.2) (2018-12-14)

[Full Changelog](https://github.com/alichtman/shallow-backup/compare/v2.1...v2.2)

**Fixed bugs:**

- KeyError: 'sublime2' when creating a backup [\#202](https://github.com/alichtman/shallow-backup/issues/202)
- gitpython Not Installed Automatically w/ setup.py [\#200](https://github.com/alichtman/shallow-backup/issues/200)
- Configs need to be a mapping in the config file. [\#195](https://github.com/alichtman/shallow-backup/issues/195)
- Prompt to remove outdated config if detected. [\#189](https://github.com/alichtman/shallow-backup/issues/189)
- Remove this plist special case logic.  [\#187](https://github.com/alichtman/shallow-backup/issues/187)

**Closed issues:**

- Fix tests that fail due to multiprocessing [\#196](https://github.com/alichtman/shallow-backup/issues/196)
- Test abspath/env expanding function [\#194](https://github.com/alichtman/shallow-backup/issues/194)
- Extract all config section names to a dict in config.py [\#190](https://github.com/alichtman/shallow-backup/issues/190)
- Extract messages to constants file [\#179](https://github.com/alichtman/shallow-backup/issues/179)
- Turn this into a generic copy method [\#177](https://github.com/alichtman/shallow-backup/issues/177)
- Extract package managers to config file [\#165](https://github.com/alichtman/shallow-backup/issues/165)
- Option to add ssh keys when they're reinstalled [\#150](https://github.com/alichtman/shallow-backup/issues/150)
- Selectively back up from .atom folder [\#133](https://github.com/alichtman/shallow-backup/issues/133)
- Separate public and private backups [\#132](https://github.com/alichtman/shallow-backup/issues/132)
- Symlink instead of copying files [\#125](https://github.com/alichtman/shallow-backup/issues/125)
- Automatic archiving after a new backup [\#176](https://github.com/alichtman/shallow-backup/issues/176)

**Merged pull requests:**

- Remove Sublime \[2/3\] packages backup [\#203](https://github.com/alichtman/shallow-backup/pull/203) ([alichtman](https://github.com/alichtman))
- \#200 added gitpython to setup.py [\#201](https://github.com/alichtman/shallow-backup/pull/201) ([AlexanderProd](https://github.com/AlexanderProd))

## [v2.1](https://github.com/alichtman/shallow-backup/tree/v2.1) (2018-11-14)

[Full Changelog](https://github.com/alichtman/shallow-backup/compare/v2.0...v2.1)

**Fixed bugs:**

- Prompt to remove outdated config if detected. [\#189](https://github.com/alichtman/shallow-backup/issues/189)
- Remove this plist special case logic.  [\#187](https://github.com/alichtman/shallow-backup/issues/187)
- Jetbrains IDE backups do not work [\#158](https://github.com/alichtman/shallow-backup/issues/158)

**Closed issues:**

- Test Package Reinstallation [\#185](https://github.com/alichtman/shallow-backup/issues/185)
- Update docs for next release [\#96](https://github.com/alichtman/shallow-backup/issues/96)

**Merged pull requests:**

- Add test for backups. [\#191](https://github.com/alichtman/shallow-backup/pull/191) ([alichtman](https://github.com/alichtman))

## [v2.0](https://github.com/alichtman/shallow-backup/tree/v2.0) (2018-11-09)

[Full Changelog](https://github.com/alichtman/shallow-backup/compare/v1.3...v2.0)

**Fixed bugs:**

- Enhance git repo move [\#168](https://github.com/alichtman/shallow-backup/issues/168)
- Accept ~ in backup path name [\#155](https://github.com/alichtman/shallow-backup/issues/155)
- Font Reinstallation doesn't work for some reason [\#145](https://github.com/alichtman/shallow-backup/issues/145)
- Tests won't run [\#142](https://github.com/alichtman/shallow-backup/issues/142)
- Module imports not working properly in refactored code [\#141](https://github.com/alichtman/shallow-backup/issues/141)
- Stop SUBLIME folders from being called `Packages` [\#113](https://github.com/alichtman/shallow-backup/issues/113)
- Backup Fonts doesn't back up all fonts [\#111](https://github.com/alichtman/shallow-backup/issues/111)
- Bug: Terminal.plist not being backed up [\#108](https://github.com/alichtman/shallow-backup/issues/108)
- On backup path update, the .git folder should be moved. [\#97](https://github.com/alichtman/shallow-backup/issues/97)
- Fix shell=True security issues [\#73](https://github.com/alichtman/shallow-backup/issues/73)
- It doesn't backup global npm packages? [\#61](https://github.com/alichtman/shallow-backup/issues/61)
- Error? Or do I just not know how to use this. [\#54](https://github.com/alichtman/shallow-backup/issues/54)

**Closed issues:**

- Unformatted error should be formatted and rephrased. [\#175](https://github.com/alichtman/shallow-backup/issues/175)
- Add "public repo" warning to setting remote URL prompt [\#174](https://github.com/alichtman/shallow-backup/issues/174)
- Extend printing utilities to formatted paths [\#172](https://github.com/alichtman/shallow-backup/issues/172)
- Refactor config file [\#166](https://github.com/alichtman/shallow-backup/issues/166)
- Support expanding ENV variables in path inputs [\#164](https://github.com/alichtman/shallow-backup/issues/164)
- --version should print version info [\#162](https://github.com/alichtman/shallow-backup/issues/162)
- Refactor version printing in CLI with Click [\#159](https://github.com/alichtman/shallow-backup/issues/159)
- Remove --add and --rm CLI args. [\#156](https://github.com/alichtman/shallow-backup/issues/156)
- Update config backup path mappings to be `config/...` [\#154](https://github.com/alichtman/shallow-backup/issues/154)
- Use --yes click option for confirmation to delete the backup. [\#152](https://github.com/alichtman/shallow-backup/issues/152)
- Rethink how `add` and `rm` args should work [\#140](https://github.com/alichtman/shallow-backup/issues/140)
- Reorganize project [\#136](https://github.com/alichtman/shallow-backup/issues/136)
- Update setup.py for next release [\#135](https://github.com/alichtman/shallow-backup/issues/135)
- Refactor --rm to take a single path arg [\#130](https://github.com/alichtman/shallow-backup/issues/130)
- Add --add & --rm commands to actions menu [\#129](https://github.com/alichtman/shallow-backup/issues/129)
- Add config paths to config file [\#128](https://github.com/alichtman/shallow-backup/issues/128)
- Speed Optimizations [\#124](https://github.com/alichtman/shallow-backup/issues/124)
- Speed Up Backup Process [\#123](https://github.com/alichtman/shallow-backup/issues/123)
- Extract all hardcoded filepaths to constants/functions [\#116](https://github.com/alichtman/shallow-backup/issues/116)
- ERROR collecting tests [\#115](https://github.com/alichtman/shallow-backup/issues/115)
- Refactor copying methods [\#112](https://github.com/alichtman/shallow-backup/issues/112)
- Make each package manager print in a color that's not the normal log color for reinstallation [\#109](https://github.com/alichtman/shallow-backup/issues/109)
- Linux Compatibility [\#104](https://github.com/alichtman/shallow-backup/issues/104)
- Add styling guide + design guide [\#103](https://github.com/alichtman/shallow-backup/issues/103)
- Set up continuous integration with Travis CI [\#102](https://github.com/alichtman/shallow-backup/issues/102)
- Add -delete\_backup argument to remove backup dir [\#95](https://github.com/alichtman/shallow-backup/issues/95)
- Currently shallow backup writes to directory ./DEFAULT/ if you don't choose a custom directory [\#93](https://github.com/alichtman/shallow-backup/issues/93)
- Running error when built from source? [\#92](https://github.com/alichtman/shallow-backup/issues/92)
- Backup Jetbrains IDE Configs [\#87](https://github.com/alichtman/shallow-backup/issues/87)
- More reinstallation support [\#86](https://github.com/alichtman/shallow-backup/issues/86)
- Add changelog [\#83](https://github.com/alichtman/shallow-backup/issues/83)
- Rename "configs" directory to "app\_configs"  [\#82](https://github.com/alichtman/shallow-backup/issues/82)
- Further Git Integration [\#81](https://github.com/alichtman/shallow-backup/issues/81)
- Prompt for remote url in CLI [\#79](https://github.com/alichtman/shallow-backup/issues/79)
- Add config file for dotfiles and directories to back up. [\#76](https://github.com/alichtman/shallow-backup/issues/76)
- Automatically create .gitignore to protect private files [\#71](https://github.com/alichtman/shallow-backup/issues/71)
- Testing Suite [\#69](https://github.com/alichtman/shallow-backup/issues/69)
- Don't delete the .git directory when creating a new backup [\#68](https://github.com/alichtman/shallow-backup/issues/68)
- Extract lists of files/directories that don't change to a constants file [\#67](https://github.com/alichtman/shallow-backup/issues/67)
- Add Pipfile for Pipenv [\#64](https://github.com/alichtman/shallow-backup/issues/64)
- Default install missing ConfigParser dependency? [\#62](https://github.com/alichtman/shallow-backup/issues/62)
- No module named configparser [\#60](https://github.com/alichtman/shallow-backup/issues/60)
- -reinstall should reinstall dotfiles [\#59](https://github.com/alichtman/shallow-backup/issues/59)
- Add -configs backup option [\#58](https://github.com/alichtman/shallow-backup/issues/58)
- Could shallow-backup integrate with git for backup? [\#57](https://github.com/alichtman/shallow-backup/issues/57)
- README [\#56](https://github.com/alichtman/shallow-backup/issues/56)
- Make shallow-backup compatible with Python 2.7 [\#55](https://github.com/alichtman/shallow-backup/issues/55)
- Remove XCode Backup [\#53](https://github.com/alichtman/shallow-backup/issues/53)
- Backup Atom Config [\#49](https://github.com/alichtman/shallow-backup/issues/49)
- Backup Terminal Preferences from .plist file [\#48](https://github.com/alichtman/shallow-backup/issues/48)
- Add option for backing up specific filepaths. [\#22](https://github.com/alichtman/shallow-backup/issues/22)
- Add GUI [\#10](https://github.com/alichtman/shallow-backup/issues/10)
- Homebrew Release [\#6](https://github.com/alichtman/shallow-backup/issues/6)
- Update docs for next release [\#96](https://github.com/alichtman/shallow-backup/issues/96)

**Merged pull requests:**

- Linux compatibility [\#183](https://github.com/alichtman/shallow-backup/pull/183) ([alichtman](https://github.com/alichtman))
- Added public repo warning [\#182](https://github.com/alichtman/shallow-backup/pull/182) ([alichtman](https://github.com/alichtman))
- Config file refactor [\#181](https://github.com/alichtman/shallow-backup/pull/181) ([alichtman](https://github.com/alichtman))
- Refactor config file architecture. [\#180](https://github.com/alichtman/shallow-backup/pull/180) ([alichtman](https://github.com/alichtman))
- New print\_color\_bold\_path helper methods [\#173](https://github.com/alichtman/shallow-backup/pull/173) ([nunomdc](https://github.com/nunomdc))
- Exit if a git repository exists on the new backup path [\#171](https://github.com/alichtman/shallow-backup/pull/171) ([nunomdc](https://github.com/nunomdc))
- Added long option for version output [\#170](https://github.com/alichtman/shallow-backup/pull/170) ([nunomdc](https://github.com/nunomdc))
- Expand environment variables [\#169](https://github.com/alichtman/shallow-backup/pull/169) ([nunomdc](https://github.com/nunomdc))
- Expand ~ as user's home directory [\#161](https://github.com/alichtman/shallow-backup/pull/161) ([nunomdc](https://github.com/nunomdc))
- Add --add and --rm path to Action Menu [\#157](https://github.com/alichtman/shallow-backup/pull/157) ([alichtman](https://github.com/alichtman))
- Prettify CLI help menu [\#153](https://github.com/alichtman/shallow-backup/pull/153) ([alichtman](https://github.com/alichtman))
- Fix font reinstallation [\#151](https://github.com/alichtman/shallow-backup/pull/151) ([alichtman](https://github.com/alichtman))
- Pkg mgr printing [\#149](https://github.com/alichtman/shallow-backup/pull/149) ([alichtman](https://github.com/alichtman))
- Better reinstallation options and better scripting support [\#147](https://github.com/alichtman/shallow-backup/pull/147) ([alichtman](https://github.com/alichtman))
- Fix travis [\#143](https://github.com/alichtman/shallow-backup/pull/143) ([alichtman](https://github.com/alichtman))
- Refactoring and Reorganization [\#139](https://github.com/alichtman/shallow-backup/pull/139) ([alichtman](https://github.com/alichtman))
- Readme [\#134](https://github.com/alichtman/shallow-backup/pull/134) ([alichtman](https://github.com/alichtman))
- Improved git integration. Added remote URL prompt. [\#131](https://github.com/alichtman/shallow-backup/pull/131) ([alichtman](https://github.com/alichtman))
- --add, --rm and -show args for config interaction [\#126](https://github.com/alichtman/shallow-backup/pull/126) ([alichtman](https://github.com/alichtman))
- fix bug: path was absolute so os.path.join was discarding the user ho… [\#120](https://github.com/alichtman/shallow-backup/pull/120) ([giancarloGiuffra](https://github.com/giancarloGiuffra))
- Clean up [\#119](https://github.com/alichtman/shallow-backup/pull/119) ([alichtman](https://github.com/alichtman))
- Extracted logo to constants.py [\#118](https://github.com/alichtman/shallow-backup/pull/118) ([alichtman](https://github.com/alichtman))
- Security update and refactoring [\#114](https://github.com/alichtman/shallow-backup/pull/114) ([alichtman](https://github.com/alichtman))
- Travis test fixes? [\#107](https://github.com/alichtman/shallow-backup/pull/107) ([alichtman](https://github.com/alichtman))
- Travis test [\#106](https://github.com/alichtman/shallow-backup/pull/106) ([alichtman](https://github.com/alichtman))
- Fix git move tests [\#105](https://github.com/alichtman/shallow-backup/pull/105) ([alichtman](https://github.com/alichtman))
- Add remove backup dir functionality [\#101](https://github.com/alichtman/shallow-backup/pull/101) ([neequole](https://github.com/neequole))
- Added support for JetBrains IDEs [\#100](https://github.com/alichtman/shallow-backup/pull/100) ([Brand-Temp](https://github.com/Brand-Temp))
- Move git folder on path change [\#99](https://github.com/alichtman/shallow-backup/pull/99) ([pyasi](https://github.com/pyasi))
- Pulls changes from remote before pushing. [\#98](https://github.com/alichtman/shallow-backup/pull/98) ([alichtman](https://github.com/alichtman))
- Push to remote URL and git logging added [\#91](https://github.com/alichtman/shallow-backup/pull/91) ([alichtman](https://github.com/alichtman))
-  Refactored config backup and added more user output  [\#90](https://github.com/alichtman/shallow-backup/pull/90) ([alichtman](https://github.com/alichtman))
- Add tests for copying. Setup project for pytest. [\#88](https://github.com/alichtman/shallow-backup/pull/88) ([pyasi](https://github.com/pyasi))
- Added changelog [\#84](https://github.com/alichtman/shallow-backup/pull/84) ([alichtman](https://github.com/alichtman))
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

[Full Changelog](https://github.com/alichtman/shallow-backup/compare/7c53c198f405828e6f1f0c4edf477b209b840fab...v0.4)

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



\* *This Changelog was automatically generated by [github_changelog_generator](https://github.com/github-changelog-generator/github-changelog-generator)*

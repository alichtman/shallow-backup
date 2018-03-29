# shallow-backup

This set of scripts is designed to make documenting Mac configurations incredibly simple.

`shallow-backup` gets up-to-date copies of your `dotfiles` and gathers package and application install lists in text files. **Remember to back up these output directories!**

To reinstall applications from the lists created, just run `$ package_manager install package_manager_list.txt`, where `package-manager` is a variable defined by the user.


**Example Use Case**

Instead of backing up your brew install library in a system backup which may occupy GBs of space, you could use `shallow-backup` to create lists of the packages and applications you have installed, which will occupy only KBs and can be transported much more easily. Additionally, you will get up-to-date versions of the packages when you reinstall. Reinstalling is as easy as `$ brew install brew_list.txt`.

#### Included Scripts
---

**Recommended Usage**

Place the folder holding the scripts inside the directory containing your `dotfiles`. All scripts can be run from that directory, and output files will populate in nested directories. Those should be backed up outside of your laptop.

**scrape_dotfiles.sh**

Output created in nested `dotfiles` directory.

1. `.pypirc`
1. `.ssh `
1. `.vim`
1. `.zshrc`

**scrape_installs.sh**

Output created in nested `installs` directory.

1. `brew` -> `brew_list.txt`
1. `brew cask` -> `brew_cask_list.txt`
1. `npm` -> `npm_list.txt`
1. `gem` -> `gem_list.txt`
1. `pip3` -> `pip3_list.txt`
1. `pip` -> `pip_list.txt`
1. Everything in system `Applications` -> `applications_list.txt`

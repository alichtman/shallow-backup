#! bin/bash
#
# Can be run from anywhere on the system
# Output in nested `installs` dir

mkdir installs
brew list > installs/brew_list.txt
brew cask list > installs/brew_cask_list.txt
npm list > installs/npm_list.txt
gem list > installs/gem_list.txt
ls /Applications/ > installs/applications_list.txt
pip3 list > installs/pip3_list.txt
pip list > installs/pip_list.txt

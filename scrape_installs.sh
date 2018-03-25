#! bin/bash
#
# Can be run from anywhere on the system, but it should be in its
# own dir because it creates a set of output files.

brew list > brew_list.txt
brew cask list > brew_cask_list.txt
npm list > npm_list.txt
gem list > gem_list.txt
ls /Applications/ > applications_list.txt
pip3 list > pip3_list.txt
pip list > pip_list.txt

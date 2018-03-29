#! bin/bash
#
# Must be placed in a dir that's in the same directory as the dotfiles.
# Output in nested `dotfiles` dir


mkdir dotfiles
cp -R ../.pypirc ./dotfiles/pypirc.txt
cp -R ../.ssh ./dotfiles/ssh
cp -R ../.vim ./dotfiles/vim
cp ../.zshrc ./dotfiles/zshrc.txt


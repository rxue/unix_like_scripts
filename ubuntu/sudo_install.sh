#!/bin/bash
echo "Install and then configure vim"
apt-get --assume-yes install vim
cat configuration/sudoer/templates/vimrc.local |tee /etc/vim/vimrc.local

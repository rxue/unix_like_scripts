#!/bin/bash
source ubuntu/install_functions.sh
apt-get --assume-yes install curl
echo "Install and then configure vim"
apt-get --assume-yes install vim
cat configuration/sudoer/templates/vimrc.local |tee /etc/vim/vimrc.local
sudo_install_chrome

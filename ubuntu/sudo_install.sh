#!/bin/bash
source ubuntu/install_functions.sh
apt-get --assume-yes install curl
echo "Install and then configure vim"
apt-get --assume-yes install vim
cat configuration/sudoer/templates/vimrc.local |tee /etc/vim/vimrc.local
install_chrome
apt-get --assume-yes install openjdk-21-jdk
install_maven
source ubuntu/install_jetbrains_software.sh
install_latest_intellij_idea

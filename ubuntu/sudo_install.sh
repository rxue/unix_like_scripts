#!/bin/bash
source ubuntu/install_functions.sh
apt-get --assume-yes install curl
[[ ! $(which vim) ]] && install_vim
[[ ! $(which google-chrome) ]] && install_chrome
apt-get --assume-yes install openjdk-21-jdk
[[ ! $(which mvn) ]] && install_maven
source ubuntu/install_jetbrains_software.sh
[[ ! $(which idea) ]] && install_latest_intellij_idea
[[ ! $(which pycharm) ]] && install_latest_pycharm

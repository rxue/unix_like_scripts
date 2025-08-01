# Install and configure vim
# Reference: http://vim.wikia.com/wiki/Indenting_source_code

install_nodejs () {
  install_2_dir=/opt/nodejs
  mkdir $install_2_dir
  local download_link=https://nodejs.org/dist/v21.6.2/node-v21.6.2-linux-x64.tar.xz
  _extract_tar_2 ${download_link} $install_2_dir xvf
  local extracted_package_name=`_basename_without_extension ${download_link}`
  ln -fs ${install_2_dir}/${extracted_package_name}/bin/node /usr/local/bin/node
  ln -fs ${install_2_dir}/${extracted_package_name}/bin/npm /usr/local/bin/npm
  ln -fs ${install_2_dir}/${extracted_package_name}/bin/npx /usr/local/bin/npx
}

# configure_python3 () {
#  apt-get install python3-pip
#  # venv is a subset of virtualenv, so use virtualenv. Reference: https://stackoverflow.com/questions/41573587/what-is-the-difference-between-venv-pyvenv-pyenv-virtualenv-virtualenvwrappe
#  pip3 virtualenv
#}
# FAQ: 
# * How Maven compile Java source code? Answer: Maven compile source code by finding using the - javac - command in the OS

install_system_monitors () {
  apt-get install strace
  apt-get install htop
}
# Reference: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html
install_aws_cli () {
  curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
  unzip awscliv2.zip
  ./aws/install
  rm awscliv2.zip
  rm -f aws
}

# extra
install_postfix () {
  debconf-set-selections <<< "postfix postfix/mailname string example.com"
  debconf-set-selections <<< "postfix postfix/main_mailer_type string 'Internet Site'"
  apt-get install -y postfix
  sed -i "s/inet_interfaces =.*$/inet_interfaces = loopback-only/" /etc/postfix/main.cf 
}


# Install and configure vim
# Reference: http://vim.wikia.com/wiki/Indenting_source_code
_basename_without_extension () {
  local file_fullname=$(basename ${1})
  local result=""
  if [[ ${file_fullname} == *.*.* ]]; then
    result=`basename "${file_fullname%.*.*}"`
  elif [[ ${file_fullname} == *.* ]]; then
    result=`basename "${file_fullname%.*}"`
  fi
  echo ${result}
}
_extract_tar_2 () {
  local download_link=${1}
  local target_dir=${2}
  wget ${download_link}
  local tar_file_name=`basename $download_link`
  local tar_options=${3}
  tar -$tar_options $tar_file_name -C $target_dir
  rm $tar_file_name
}

install_maven () {
  local download_link=https://dlcdn.apache.org/maven/maven-3/3.9.0/binaries/apache-maven-3.9.0-bin.tar.gz
  _extract_tar_2 ${download_link} /opt/ xvzf
  local extracted_package_name=`_basename_without_extension ${download_link}`
  ln -fs /opt/${extracted_package_name%-bin}/bin/mvn /usr/local/bin/mvn

}
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
install_vim () {
  apt-get --assume-yes install vim
  cat sudoer/templates/vimrc.local |tee /etc/vim/vimrc.local
}

# configure_python3 () {
#  apt-get install python3-pip
#  # venv is a subset of virtualenv, so use virtualenv. Reference: https://stackoverflow.com/questions/41573587/what-is-the-difference-between-venv-pyvenv-pyenv-virtualenv-virtualenvwrappe
#  pip3 virtualenv
#}
# FAQ: 
# * How Maven compile Java source code? Answer: Maven compile source code by finding using the - javac - command in the OS

install_eclipse () {
  direct_download_link=$(python3 python/get_eclipse_package_direct_download_link.py)
  wget ${direct_download_link}
  tar_file_name=$(python3 python/utils.py get_str ${direct_download_link} ".*.tar.gz" "/")
  tar -xvzf ${tar_file_name} -C /opt/
  rm ${tar_file_name}
  # Refer to http://stackoverflow.com/questions/37864572/using-different-location-for-eclipses-p2-file
  ln -fs /opt/eclipse/eclipse /usr/bin/eclipse
  python3 python/add_to_gnome_main_menu.py eclipse /opt/eclipse/eclipse /opt/eclipse/icon.xpm
}
_add_to_gnome_main_menu () {
  local app_name=$1
  local desktop_file=/usr/share/applications/${app_name}.desktop
  cp configuration/sudoer/templates/app.desktop.template $desktop_file
  sed -i "s/#{app_name}/"${app_name}"/g" $desktop_file
  sed -i "s%#{executable_file_path}%"${2}"%g" $desktop_file
  sed -i "s%#{icon_path}%"${3}"%g" $desktop_file
}
_get_intellij_idea_latest_download_url () {
  curl --silent https://data.services.jetbrains.com/products?code=IIC |jq -r '.[0].releases[0].downloads.linux.link'
}
_download_latest_intellij_idea () {
  local download_url=`_get_intellij_idea_latest_download_url`
  echo "Download IntelliJ Idea from link: "$download_url
  curl -LO $download_url
}
install_latest_intellij_idea () {
  _download_latest_intellij_idea
  local program_dir=$(basename `_get_intellij_idea_latest_download_url` |sed 's/.tar.gz//')
  echo "file name is "$program_dir
  local intellij_dir=/opt/intellij
  tar -xvzf ${program_dir}.tar.gz -C ${intellij_dir}/
  local idea_bin_dir=/opt/intellij/${program_dir}/bin
  ln -fs ${idea_bin_dir}/idea.sh /usr/bin/intellij.idea
  _add_to_gnome_main_menu intellij.idea ${idea_bin_dir}/idea.sh ${idea_bin_dir}/idea.png
}

install_system_monitors () {
  apt-get install strace
  apt-get install htop
}
# $1 - user to add as sudoer 
#add_sudoer () {
#  user_name=$1
#  config_statement=$(grep '^root' /etc/sudoers)
#  [[ ! $(grep '^'${user_name} /etc/sudoers) ]] && echo ${config_statement/root/$user_name} >> /etc/sudoers
#  
#}

# Reference: https://docs.docker.com/engine/install/debian/
install_docker () {
  # Set up the repository
  apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
  # Add Docker's Official GPG key
  curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg 
  echo \
  "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/debian \
  $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
  apt-get update
  apt-get install docker-ce docker-ce-cli containerd.io
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


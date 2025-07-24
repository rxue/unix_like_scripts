install_vim () {
  apt-get --assume-yes install vim
  cat ubuntu/templates/vimrc.local | tee /etc/vim/vimrc.local
}
install_chrome () {
  wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
  dpkg -i google-chrome-stable_current_amd64.deb
  if [ $? -ne 0 ]; then
    # Reference: man 8 apt-get
    apt-get --assume-yes install -f
  fi
  dpkg -i google-chrome-stable_current_amd64.deb
  rm google-chrome-stable_current_amd64.deb
}
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
  local version=3.9.11
  local download_link=https://dlcdn.apache.org/maven/maven-3/${version}/binaries/apache-maven-${version}-bin.tar.gz
  _extract_tar_2 ${download_link} /opt/ xvzf
  local extracted_package_name=`_basename_without_extension ${download_link}`
  ln -fs /opt/${extracted_package_name%-bin}/bin/mvn /usr/local/bin/mvn
}
# Reference: https://docs.docker.com/engine/install/debian/
install_docker () {
  # Set up the repository
  apt-get --assume-yes install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
  # Add Docker's Official GPG key
  install -m 0755 -d /etc/apt/keyrings
  curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
  chmod a+r /etc/apt/keyrings/docker.gpg
  echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
  # Install
  apt-get update
  apt-get --assume-yes install docker-ce docker-ce-cli containerd.io
  echo "add docker user group and add the current user to it"
  newgrp docker
  usermod -aG docker $USER
}


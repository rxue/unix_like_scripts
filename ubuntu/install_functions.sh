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
  local program_name=$(basename `_get_intellij_idea_latest_download_url`)
  if [ -e "$program_name" ]; then
    echo "IntelliJ installatio file exists already"
  else
    curl -LO $download_url
  fi
}
_echo_extracted_program_dir () {
  local downloaded_file_name=$(basename `_get_intellij_idea_latest_download_url`)
  dir=$(tar -tf $downloaded_file_name |head -1)
  echo "${dir%?}"
}
install_latest_intellij_idea () {
  _download_latest_intellij_idea
  local intellij_dir=/opt/intellij
  mkdir -p $intellij_dir
  local downloaded_file_name=$(basename `_get_intellij_idea_latest_download_url`)
  tar -xvzf ${downloaded_file_name} -C ${intellij_dir}/
  local extracted_program_dir=$(_echo_extracted_program_dir)
  local idea_bin_dir=${intellij_dir}/${extracted_program_dir}/bin
  ln -fs ${idea_bin_dir}/idea /usr/bin/idea
  _add_to_gnome_main_menu idea ${idea_bin_dir}/idea ${idea_bin_dir}/idea.png
}

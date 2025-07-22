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

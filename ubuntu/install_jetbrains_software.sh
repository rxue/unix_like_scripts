_add_to_gnome_main_menu () {
  local app_name=$1
  local desktop_file=/usr/share/applications/${app_name}.desktop
  cp configuration/sudoer/templates/app.desktop.template $desktop_file
  sed -i "s/#{app_name}/"${app_name}"/g" $desktop_file
  sed -i "s%#{executable_file_path}%"${2}"%g" $desktop_file
  sed -i "s%#{icon_path}%"${3}"%g" $desktop_file
}
_get_latest_download_url () {
  local product_code=$1
  curl --silent https://data.services.jetbrains.com/products?code=${product_code} |jq -r '.[0].releases[0].downloads.linux.link'
}
_get_latest_download_file_name () {
  local product_code=$1
  local download_url=`_get_latest_download_url $product_code`
  basename $download_url
}
_download_latest () {
  local product_code=$1
  if [ -e "$(_get_latest_download_file_name $product_code)" ]; then
    echo "File to download exists already"
  else
    download_url=`_get_latest_download_url $product_code`
    echo "Download from link: "$download_url
    curl -LO $download_url
  fi
}
_echo_extracted_program_dir () {
  local product_code=$1
  local downloaded_file_name=$(_get_latest_download_file_name $product_code)
  dir=$(tar -tf $downloaded_file_name |head -1)
  echo "${dir%?}"
}
download_and_extract () {
  local product_code=$1
  _download_latest $product_code
  local target_dir=$2
  mkdir -p $target_dir
  local downloaded_file_name=$(_get_latest_download_file_name $product_code)
  echo "Extract ${downloaded_file_name} to "${target_dir}
  tar -xvzf ${downloaded_file_name} -C ${target_dir}/
}
install_latest_intellij_idea () {
  local product_code=IIC
  local target_dir=/opt/jetbrains
  download_and_extract $product_code $target_dir
  local idea_bin_dir=${target_dir}/$(_echo_extracted_program_dir $product_code)/bin
  ln -fs ${idea_bin_dir}/idea /usr/bin/idea
  _add_to_gnome_main_menu idea ${idea_bin_dir}/idea ${idea_bin_dir}/idea.png
}
install_latest_pycharm () {
  local product_code=PCC
  local target_dir=/opt/jetbrains
  download_and_extract $product_code $target_dir
  local idea_bin_dir=${target_dir}/$(_echo_extracted_program_dir $product_code)/bin
  ln -fs ${idea_bin_dir}/pycharm /usr/bin/pycharm
  _add_to_gnome_main_menu pycharm ${idea_bin_dir}/pycharm ${idea_bin_dir}/pycharm.png
}

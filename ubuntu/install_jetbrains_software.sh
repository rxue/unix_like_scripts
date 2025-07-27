_make_desktop_file () {
  local executable=$1
  local desktop_file=/usr/share/applications/${executable}.desktop
  cp templates/app.desktop.template $desktop_file
  local program_dir=$2
  local name=`jq -r '.name' ${program_dir}/product-info.json`
  sed -i "s/#{name}/${name}/" $desktop_file
  sed -i "s%#{executable_file_path}%"${program_dir}/bin/${executable}"%g" $desktop_file
  sed -i "s/#{executable}/${executable}/" $desktop_file
  local startupWmClass=`jq -r '.launch[0].startupWmClass' ${program_dir}/product-info.json`
  sed -i "s/#{startupWmClass}/${startupWmClass}/" $desktop_file
}
_add_icon () {
  local executable=$1
  local program_image_dir=$2
  local icon_extension=$3
  local icon=${program_image_dir}/${executable}.${icon_extension}
  local icon_size=`identify -format "%wx%h\n" ${icon}`
  cp $icon /usr/share/icons/hicolor/${icon_size}/apps/
}
_get_latest_download_url () {
  local product_code=$1
  if [ -z "${product_code}" ]; then
    echo "product code has to be given as the first argument"
  else  
    curl --silent https://data.services.jetbrains.com/products?code=${product_code} |jq -r '.[0].releases[0].downloads.linux.link'
  fi
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
install_latest () {
  local product_code=$1
  local download_target_dir=/opt/jetbrains
  download_and_extract $product_code $download_target_dir
  local extracted_dir=${download_target_dir}/$(_echo_extracted_program_dir $product_code)
  echo "extracted directory: "$extracted_dir
  local executable=$2
  ln -fs ${extracted_dir}/bin/idea /usr/bin/${executable}
  _make_desktop_file $executable ${extracted_dir}
  _add_icon $executable ${extracted_dir}/bin png
  _add_icon $executable ${extracted_dir}/bin svg
  gtk-update-icon-cache /usr/share/icons/hicolor
}
install_latest_intellij_idea () {
  local product_code=IIC
  local target_dir=/opt/jetbrains
  download_and_extract $product_code $target_dir
  local idea_dir=${target_dir}/$(_echo_extracted_program_dir $product_code)
  echo "Idea directory: "$idea_dir
  ln -fs ${idea_dir}/bin/idea /usr/bin/idea
  _make_desktop_file idea ${idea_dir}
  _add_icon idea ${idea_dir}/bin png
  _add_icon idea ${idea_dir}/bin svg
  gtk-update-icon-cache /usr/share/icons/hicolor
}
install_latest_pycharm () {
  local product_code=PCC
  local target_dir=/opt/jetbrains
  download_and_extract $product_code $target_dir
  local pycharm_dir=${target_dir}/$(_echo_extracted_program_dir $product_code)
  ln -fs ${pycharm_dir}/bin/pycharm /usr/bin/pycharm
  _make_desktop_file pycharm $pycharm_dir
  _add_icon pycharm ${pycharm_dir}/bin png
  _add_icon pycharm ${pycharm_dir}/bin svg
}

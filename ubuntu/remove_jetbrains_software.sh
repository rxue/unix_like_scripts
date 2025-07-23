remove () {
 local app_name=$1
 rm /usr/bin/${app_name}
 rm /usr/share/applications/${app_name}.desktop
 local bin_dir=$2
 [[ -n "${bin_dir}" ]] && rm -rf $bin_dir
}


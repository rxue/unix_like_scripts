remove () {
 local executable=$1
 rm /usr/share/applications/${executable}.desktop
 local program_dir=$(dirname $(dirname `readlink /usr/bin/${executable}`))
 echo "Program directory: "$program_dir
 [[ -n "${program_dir}" ]] && rm -rf $program_dir
 rm /usr/bin/${executable}
 echo "remove icons"
 find /usr/share/icons -type f -name "${executable}.*" |xargs -r rm -f
 gtk-update-icon-cache /usr/share/icons/hicolor
}


# Install and configure vim
# Reference: http://vim.wikia.com/wiki/Indenting_source_code
configure_vim () {
  cp /etc/vim/vimrc.local ~/.vimrc
  config_statements=`cat <<EOF
# Imitate NerdTree: https://shapeshed.com/vim-netrw/
let g:netrw_banner = 0
let g:netrw_liststyle = 3
let g:netrw_browse_split = 4
let g:netrw_altv = 1
let g:netrw_winsize = 25
augroup ProjectDrawer
  autocmd!
  autocmd VimEnter * :Vexplore
augroup END
EOF`
  echo "${config_statements}" >> ~/.vimrc
}
# $1 - name
# $2 - email
configure_git () {
  local _name=$1
  local _email=$2
  git config --global user.name "${_name}"
  git config --global user.email "${_email}"
  # display colours for example on git status or git diff commands
  git config --global --add color.ui true
  # set vim as the default editor of git
  git config --global core.editor "vim"
  ssh-keygen -t ed25519 -C "${_email}"
}

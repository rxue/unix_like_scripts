import sys
# Reference: https://valadoc.org/glib-2.0/GLib.Variant.html
from gi.repository import Gio
from gi.repository import GLib
#from ast import literal_eval
media_keys_schema = 'org.gnome.settings-daemon.plugins.media-keys' 
media_keys_settings = Gio.Settings.new(media_keys_schema)
key_custom_keybindings = 'custom-keybindings'
custom_key_bindings = media_keys_settings.get_value(key_custom_keybindings)
paths = custom_key_bindings.get_strv()
custom_keybinding_schema = media_keys_schema + '.custom-keybinding'
def _get_new_custom_keybinding_path(name:str):
  custom_name = name.replace(' ', '').lower()
  return "/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/" + custom_name + '/'

def _add_new_custom_keybinding_path(new_custom_keybinding_path:str):
  global media_keys_settings
  global key_custom_keybindings
  global custom_key_bindings
  global paths
  paths.append(new_custom_keybinding_path)
  media_keys_settings.set_value(key_custom_keybindings, GLib.Variant.new_strv(paths))
  
def make_shortcut(name:str,command:str,shortcut:str):
  global media_keys_schema 
  new_custom_keybinding_path = _get_new_custom_keybinding_path(name)
  global paths
  if new_custom_keybinding_path in paths:
    print("short cut,",name + ", existed already")
  else:
    _add_new_custom_keybinding_path(new_custom_keybinding_path)
    global custom_keybinding_schema
    custom_keybinding_settings = Gio.Settings.new_with_path(custom_keybinding_schema, new_custom_keybinding_path)
    custom_keybinding_settings.set_string('name', name)
    custom_keybinding_settings.set_string('command', command)
    custom_keybinding_settings.set_string('binding', shortcut)
    custom_keybinding_settings.apply()
    Gio.Settings.sync()
  
if __name__ == "__main__":
  new_operation_name = sys.argv[1]
  command = sys.argv[2]
  shortcut = sys.argv[3]
  make_shortcut(new_operation_name, command, shortcut)

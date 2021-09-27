import os
import configparser
import qr_alchemy.gui_process as gui
import qr_alchemy.plugins as qr_plugins

sys_configfile_path=""
user_configfile_path=""
qr_configfile="qr_alchemy.conf"
qr_user_configdir=".config/qr_alchemy/"
qr_plugin_dir="/usr/share/qr_alchemy/input_plugins/"
qr_user_plugin_dir=qr_user_configdir + "input_plugins/"

def _get_homedir():
    if "HOME" in  os.environ:
        return os.environ['HOME']
    else:
        return os.environ['/']

def set_sys_configfile(file):
    global sys_configfile_path
    sys_configfile_path=file

def set_user_configfile(file):
    global sys_configfile_path
    sys_configfile_path=file

def _get_user_configfile():
    global user_configfile_path
    if user_configfile_path == '':
        homedir=_get_homedir()
        user_configfile_path=homedir + '/' + qr_user_configdir + qr_configfile
    return user_configfile_path

def update_confog_actionmap(code_type, a_type, a_subtype):
    section = 'action_map'
    key = code_type
    if a_subtype == '':
        value=a_type
    else:
        value=a_type + ":" + a_subtype
    update_config(section, key, value)

def update_config(section, key, value):
    global user_configfile_path

    user_configfile_path=_get_user_configfile()
    config = configparser.ConfigParser()
    
    try:
        config.read(user_configfile_path)
    except:
        print("user config not found")
        
    if not section in config:
        config[section]=dict()
    config[section][key]=value
    with open(user_configfile_path, 'w') as configfile:
        config.write(configfile)

def get_config():
    global sys_configfile_path
    config = configparser.ConfigParser()
    config.read(sys_configfile_path)

    user_configfile_path=_get_user_configfile()

    try:
        config.read(user_configfile_path)

    except:
        print("user configfile unavailable")
    
    config_new = dict()
    for topic in config:
        config_new[topic]=dict()
    for entry in config['action_map']:
        action = config['action_map'][entry]
        split = action.split(':', 2)
        action_type = split[0]
        if action_type == '':
            continue

        if len(split) > 1:
            action_subtype = split[1]
            config_new['action_map'][entry] = [action_type, action_subtype]
        else:
            config_new['action_map'][entry] = [action_type]
    return config_new

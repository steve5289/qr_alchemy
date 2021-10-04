### Config Lib
# Provides the ability to access and mofify the configuration files.
#
# Current setup is there is a system config file and a user config file, 
# Settings in the user config file override settings in the system config file.
# Only the user config file can be modified from this
#
# The contents of the configfile are cached in the qr_config variable to reduce 
# disk access polls


import configparser
import os
import subprocess
import sys

import qralchemy.common as qr_common

sys_configfile_path=""
user_configfile_path=""
qr_configfile="qralchemy.conf"
qr_user_configdir=".config/qralchemy/"
qr_plugin_dir="/usr/share/qralchemy/input_plugins/"
qr_user_plugin_dir=qr_user_configdir + "input_plugins/"

qr_config = None

def set_sys_configfile(file):
    global sys_configfile_path
    sys_configfile_path=file
    refresh_config()

def set_user_configfile(file):
    global user_configfile_path
    user_configfile_path=file
    refresh_config()

def _get_user_configfile():
    global user_configfile_path
    if user_configfile_path == '':
        homedir=qr_common.get_homedir()
        user_configfile_path=homedir + '/' + qr_user_configdir + qr_configfile
    return user_configfile_path

def update_config_actionmap(code_type, a_type, a_subtype):
    section = 'action_map'
    key = code_type
    if a_subtype == '':
        value=a_type
    else:
        value=a_type + ":" + a_subtype
    update_config(section, key, value)

def update_config(section, key, value):
    global user_configfile_path

    # note that we only read the user config and not the system config as to 
    # not replicate the system config into the user config file
    user_configfile_path=_get_user_configfile()
    config = configparser.ConfigParser()
    
    try:
        config.read(user_configfile_path)
    except:
        print("user config not found")
        
    if not section in config:
        config[section]=dict()
    config[section][key]=str(value)
    with open(user_configfile_path, 'w') as configfile:
        config.write(configfile)
    refresh_config()

def refresh_config():
    global sys_configfile_path
    global qr_config

    config = configparser.ConfigParser()
    
    try:
        config.read(sys_configfile_path)
    except:
        print('system config not available')

    user_configfile_path=_get_user_configfile()

    try:
        config.read(user_configfile_path)

    except:
        print("user configfile unavailable")
    
    qr_config = dict()
    for topic in config:
        qr_config[topic]=dict()
        if topic == 'action_map':
            continue
        for entry in config[topic]:
            if config[topic][entry] != '':
                qr_config[topic][entry] = config[topic][entry]
    # The action map is special as it contains a colen(:) seperated list as 
    # configparser can't handle an array in that field.
    if 'action_map' not in config:
        return
    for entry in config['action_map']:
        action = config['action_map'][entry]
        split = action.split(':', 2)
        action_type = split[0]
        if action_type == '':
            continue

        if len(split) > 1:
            action_subtype = split[1]
            qr_config['action_map'][entry] = [action_type, action_subtype]
        else:
            qr_config['action_map'][entry] = [action_type]
    

def get_config():
    global qr_config
    if qr_config == None:
        refresh_config()
    return qr_config

def set_offer_system(code_type, active):
    home = qr_common.get_homedir()
    apps_dir=home + '/.local/share/applications'
    appfile = apps_dir + '/qralchemy_process.desktop'

    if active:
        update_config('system_offer', code_type, 1)
    else:
        # To ensure the user can null out a field provided by the system config 
        # file, we allow null entries to signify unset
        update_config('system_offer', code_type, '')

    config = get_config()
    
    if config['system_offer']:
        code_types = config['system_offer'].keys()
        output =  "[Desktop Entry]\n"
        output += "Name=QR Alchemy Processer\n"
        output += "Exec=" +sys.argv[0] + " %u\n"
        output += "Icon=qralchemy\n"
        output += "Type=Application\n"
        output += "NoDisplay=true\n"
        output += "MimeType="
        for code_type in code_types:
            output +="x-scheme-handler/"+ code_type +";"
        output += "\n"

        fh_w = open(appfile, 'w')
        fh_w.write(output)
        fh_w.close()

        # Has xdg read the desktop files and update it's mappings for what mime 
        # types launch what programs.
        subprocess.run(['update-desktop-database', apps_dir])
        # Sets this program as the new default for the given mime code
        subprocess.run(['xdg-mime','default', 'qralchemy_process.desktop', "x-scheme-handler/"+ code_type])
    else:
        try:
            os.remove(appfile)
        except:
            pass
        # Has xdg read the desktop files and update it's mappings for what mime 
        # types launch what programs.
        subprocess.run(['update-desktop-database', apps_dir])

def get_offer_system(code_type):
    config = get_config()
    if not 'system_offer' in config:
        return
    if code_type in config['system_offer']:
        return True
    return False

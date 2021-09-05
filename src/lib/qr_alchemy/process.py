
import subprocess
import configparser
import os
import qr_alchemy.gui_process as gui

qr_configfile_path=""
qr_configfile="qr_alchemy.conf"
qr_user_configdir=".config/qr_alchemy/"
qr_action_types=['System Default', 'Nothing', 'Plugin', 'Program']
qr_plugin_dir="/usr/share/qr_alchemy/input_plugins/"
qr_user_plugin_dir=qr_user_configdir + "input_plugins/"

def configfile(file):
    global qr_configfile_path
    qr_configfile_path=file

def qr_image_handler(file):
    qr_code_raw = subprocess.check_output(['zbarimg', '-q', '--raw', file])
    qr_code = qr_code_raw.decode("utf-8")
 
     
    if qr_code:
        return qr_code
    return None

def qr_code_handler(qr_code):
    header = qr_get_header(qr_code)
    action = qr_get_action(header)

    qr_exec(action, qr_code)

def get_qr_action_types():
    return qr_action_types

def qr_exec(action, qr_code):
    if str.startswith(action, "cli:"):
        junk, cli = action.split(':',2)
        print(cli, qr_code)
        subprocess.run([cli, qr_code])
    elif action == 'text':
        print("text function not yet implemented")
        print("qr code: '" + qr_code +"'")

def qr_get_header(qr_code):
    split = qr_code.split(':')
    if (len(split) >= 2):
        return split[0]
    return ''
    
def qr_get_action(header):
    header2action = qr_code2action()

    if header in header2action:
        return header2action[header]
    return header2action['*']

def _get_homedir():
    if "HOME" in  os.environ:
        return os.environ['HOME']
    else:
        return os.environ['/']

def _get_user_configfile():
    homedir=_get_homedir()
    qr_userconfig=homedir + qr_user_configdir + qr_configfile
    return qr_userconfig
    
    
def qr_code2action():
    config = configparser.ConfigParser()
    config.read(qr_configfile_path)

    qr_userconfig=_get_user_configfile()
    config_user=configparser.ConfigParser()

    try:
        config_user.read(qr_userconfig)

        config |= config_user
    except:
        print("user configfile unavailable")
    
    return config['action_map']


def qr_update_configaction(key, value):

    qr_userconfig=_get_user_configfile()
    
    config = configparser.ConfigParser()
    
    try:
        config.read(qr_userconfig)
    except:
        print("user config not found")
        
    config['action_map'][key]=value
    config.write(qr_userconfig)



def qr_get_plugins():

    plugins=_qr_get_plugins_from_dir(qr_plugin_dir)
    user_plugins=_qr_get_plugins_from_dir(qr_user_plugin_dir)

    plugins |= user_plugins 

    return plugins

def _qr_get_plugins_from_dir(plugin_dir):
    if not os.path.isdir(plugin_dir):
        return dict()

    files = os.listdir(plugin_dir)
    plugins=dict()
    
    for file in files:
        path = qr_plugin_dir + file
        # check if it's executable and a file
        if os.access(path, os.X_OK) and os.isfile(path):
            plugins[file]=path
    return plugins
    

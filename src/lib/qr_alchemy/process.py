
import subprocess
import configparser
import os

qr_configfile_path=""
qr_configfile="qr_alchemy.conf"
qr_user_configdir=".config/qr_alchemy/"

def configfile(file):
    global qr_configfile_path
    qr_configfile_path=file

def qr_image_handler(file):
    qr_code_raw = subprocess.check_output(['zbarimg', '-q', '--raw', file])
    qr_code = qr_code_raw.decode("utf-8")
  
    if qr_code:
        print(qr_code)
        qr_code_handler(qr_code)
    else:
        print("code not found in image")

def qr_code_handler(qr_code):
    header = qr_get_header(qr_code)

    action = qr_get_action(header)
    
    qr_exec(action, qr_code)


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

### Plugin Lib
# Provides the ability to query, add, and delete input and output plugins

import os
import stat
import sys
import subprocess
import shutil

import qr_alchemy.common as qr_common


sys_input_plugin_dir=""
sys_output_plugin_dir=""

qr_userconfig=""
user_input_plugin_dir=""
user_output_plugin_dir=""
qr_user_configdir=".config/qr_alchemy/"

def set_user_plugin_dir(path):
    global qr_user_configdir
    global qr_userconfig 
    global user_input_plugin_dir
    global user_output_plugin_dir

    qr_userconfig=path
    user_input_plugin_dir=qr_userconfig + "/input_plugins"
    user_output_plugin_dir=qr_userconfig + "/output_plugins"

def set_sys_plugin_dir(path):
    global sys_input_plugin_dir
    global sys_output_plugin_dir
    global qr_userconfig 

    sys_plugin_dir=path
    sys_input_plugin_dir=path+"/input_plugins"
    sys_output_plugin_dir=path+"/output_plugins"
    
    if qr_userconfig == "":
        homedir=qr_common.get_homedir()
        qr_userconfig=homedir + '/' + qr_user_configdir
        set_user_plugin_dir(qr_userconfig)
        
def _add_plugin(file, dest):
    os.makedirs(dest, exist_ok=True)
    dest_path = dest + '/' + os.path.basename(file)
    shutil.copyfile(file, dest_path)
    os.chmod(dest_path, stat.S_IRUSR | stat.S_IXUSR)


def _get_plugins(sys_dir,user_dir):
    plugin=dict()

    try:
        files = os.listdir(sys_dir)
        for file in files:
            path=sys_dir + '/' + file
            if os.access(path, os.X_OK) and os.path.isfile(path):
                plugin[file]=path
    except:
        pass
        
    try:
        files = os.listdir(user_dir)
        for file in files:
            path=user_dir + '/' + file
            if os.access(path, os.X_OK) and os.path.isfile(path):
                plugin[file]=path
    except:
        pass

    return plugin

## INPUT

def get_input_plugins():
    return _get_plugins(sys_input_plugin_dir,user_input_plugin_dir)

def run_input_plugin(plugin, qr_code):
    plugin_map=get_input_plugins()
    
    if not plugin in plugin_map:
        print('Error! plugin not found: ', plugin)
        return False
    
    pid=os.fork()
    if pid == 0:
        pid=os.fork()
        if pid == 0:
            args=('null', qr_code)
            os.execl(plugin_map[plugin], *args)
        else:
            sys.exit(0)
    else:
        os.wait()

def add_input_plugin(file):
    _add_plugin(file, user_input_plugin_dir)

def delete_input_plugin(plugin):
    plugin2path = get_input_plugins()
    if input_plugin_can_delete(plugin):
        os.remove(plugin2path[plugin])
        return True
    print("Error! Failed to delete: ", plugin2path[plugin])
    return False

def input_plugin_can_delete(plugin):
    global sys_input_plugin_dir
    plugin2path = get_input_plugins()
    if plugin2path[plugin].startswith(user_input_plugin_dir):
        return True
    return False

## OUTPUT
def get_output_plugins():
    return _get_plugins(sys_output_plugin_dir,user_output_plugin_dir)

def run_output_plugin(plugin):
    plugin_map=get_output_plugins()
    
    if not plugin in plugin_map:
        print('Error! plugin not found: ', plugin)
        return False
    
    cmd=subprocess.run([plugin_map[plugin],'start'], capture_output=True)
    byte_stdout = cmd.stdout
    str_stdout = byte_stdout.decode('UTF-8')
    return [cmd.returncode,str_stdout]

def stop_output_plugin(plugin):
    plugin_map=get_output_plugins()
    
    if not plugin in plugin_map:
        print('Error! plugin not found: ', plugin)
        return False
    
    cmd=subprocess.run([plugin_map[plugin],'stop'])

def add_output_plugin(file):
    _add_plugin(file, user_output_plugin_dir)

def delete_output_plugin(plugin):
    plugin2path = get_output_plugins()
    if output_plugin_can_delete(plugin):
        os.remove(plugin2path[plugin])
        return True
    print("Error! Failed to delete: ", plugin2path[plugin])
    return False

def output_plugin_can_delete(plugin):
    global sys_output_plugin_dir
    plugin2path = get_output_plugins()
    if not plugin in plugin2path:
        return False
    if plugin2path[plugin].startswith(user_output_plugin_dir):
        return True
    return False


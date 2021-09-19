import os
import subprocess

sys_input_plugin_dir=""
sys_output_plugin_dir=""

user_input_plugin_dir=""
user_output_plugin_dir=""

def _get_plugins(sys_dir,user_dir):
    plugin=dict()

    files = os.listdir(sys_dir)
    for file in files:
        path=sys_dir + file
        if os.access(path, os.X_OK) and os.isfile(path):
            plugin[file]=path
        
    files = os.listdir(user_dir)
    for file in files:
        path=user_dir + file
        if os.access(path, os.X_OK) and os.isfile(path):
            plugin[file]=path

    return plugin

## INPUT
def set_sys_input_plugin_dir(path):
    sys_input_plugin_dir=path

def set_user_input_plugin_dir(path):
    user_input_plugin_dir=path

def get_input_plugins():
    return _get_plugins(sys_input_plugin_dir,user_input_plugin_dir)

def run_input_plugin(plugin, qr_code):
    plugin_map=get_input_plugins()
    
    if not plugin in plugin_map:
        print('Error! plugin not found: ', plugin)
        return False
    
    pid=os.fork
    if pid == 0:
        pid=os.fork
        if pid == 0:
            os.exec(plugin_map[plugin], qr_code)
        else:
            sys.exit(0)
    else:
        os.waitid(pid)
    

## OUTPUT
def set_sys_output_plugin_dir(path):
    sys_input_plugin_dir=path

def set_user_output_plugin_dir(path):
    user_input_plugin_dir=path

def get_output_plugins():
    return _get_plugins(sys_output_plugin_dir,user_output_plugin_dir)

def run_output_plugin(plugin, qr_code):
    plugin_map=get_output_plugins
    
    if not plugin in plugin_map:
        print('Error! plugin not found: ', plugin)
        return False
    
    cmd=subprocess.run([plugin_map[plugin], qr_code])

    return [cmd.returncode,cmd.stdout]

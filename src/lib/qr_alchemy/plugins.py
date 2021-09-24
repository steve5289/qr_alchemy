import os
import subprocess

sys_input_plugin_dir=""
sys_output_plugin_dir=""

user_input_plugin_dir=""
user_output_plugin_dir=""
qr_user_configdir=".config/qr_alchemy/"

def _get_homedir():
    if "HOME" in  os.environ:
        return os.environ['HOME']
    else:
        return os.environ['/']

def set_sys_plugin_dir(path):
    global sys_input_plugin_dir
    global sys_output_plugin_dir
    global user_input_plugin_dir
    global user_output_plugin_dir

    sys_plugin_dir=path
    sys_input_plugin_dir=path+"/input_plugins"
    sys_output_plugin_dir=path+"/output_plugins"
    
    homedir=_get_homedir()
    qr_userconfig=homedir + '/' + qr_user_configdir
    user_input_plugin_dir=qr_userconfig + "/input_plugins"
    user_output_plugin_dir=qr_userconfig + "/output_plugins"

def _get_plugins(sys_dir,user_dir):
    plugin=dict()

    try: 
        files = os.listdir(sys_dir)
        for file in files:
            path=sys_dir + '/' + file
            if os.access(path, os.X_OK):
                plugin[file]=path
    except:
        pass
        
    try:
        files = os.listdir(user_dir)
        for file in files:
            path=user_dir + '/' + file
            if os.access(path, os.X_OK) and os.isfile(path):
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


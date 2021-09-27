
import subprocess
import qr_alchemy.gui_process as gui
import qr_alchemy.plugins as qr_plugins
import qr_alchemy.config as qr_config

qr_action_types=['System Default', 'Nothing', 'Plugin', 'Program']

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
    a_type = action[0]
    if len(action) > 1:
        a_subtype = action[1]
    else:
        a_subtype = ''

    if a_type == "System Default":
        subprocess.run(['xdg-open', qr_code])
    elif a_type == "Program":
        subprocess.run([a_subtype, qr_code])
    elif a_type == 'Plugin':
        qr_plugins.run_input_plugin(a_subtype,qr_code)

def qr_get_header(qr_code):
    split = qr_code.split(':')
    if (len(split) >= 2):
        return split[0].lower()
    return ''
    
def qr_get_action(header):
    header2action = qr_code2action()
    print('header2action:', header2action)

    if header in header2action:
        return header2action[header]
    elif '*' in header2action:
        return header2action['*']
    else:
        return ['System Default']


def qr_code2action():
    config = qr_config.get_config()
    return config['action_map']

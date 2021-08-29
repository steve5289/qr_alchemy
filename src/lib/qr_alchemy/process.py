
import subprocess
import configparser

qr_configfile=""

def configfile(file): 
    global qr_configfile
    qr_configfile=file

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


def qr_code2action():
    config = configparser.ConfigParser()
    config.read("./src/etc/qr_alchemy.conf")
    
    return config['action_map']

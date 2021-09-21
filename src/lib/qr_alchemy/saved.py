import os
import pickle
from datetime import datetime

qr_user_configdir=".config/qr_alchemy/"
savefile="saved_qr.dat"
histfile="history_qr.dat"
hist_max=10

def _get_homedir():
    if "HOME" in os.environ:
        return os.environ['HOME'] + '/'
    else:
        return os.environ['/']

def _get_user_savefile():
    homedir=_get_homedir()
    qr_userconfig=homedir + qr_user_configdir + savefile
    if not os.path.isdir(homedir + qr_user_configdir):
        os.mkdir(homedir + qr_user_configdir)
    return qr_userconfig
    
def _get_user_histfile():
    homedir=_get_homedir()
    qr_userconfig=homedir + qr_user_configdir + histfile
    if not os.path.isdir(homedir + qr_user_configdir):
        os.mkdir(homedir + qr_user_configdir)
    return qr_userconfig
    
def get_saved_codes():
    savefile=_get_user_savefile()

    try:
        fh = open(savefile,'rb')
        codes=pickle.load(fh)
        fh.close()
    except:
        codes = dict()
    return codes

def set_saved_code(name,qr_code):
    savefile=_get_user_savefile()
    saved_codes=get_saved_codes()
    fh = open(savefile, 'wb')
    
    saved_codes[name]=qr_code
    pickle.dump(saved_codes, fh)
    fh.close()

def delete_saved_code(name):
    savefile=_get_user_savefile()
    saved_codes=get_saved_codes()
    fh = open(savefile, 'wb')
    
    saved_codes.pop(name)
    pickle.dump(saved_codes, fh)
    fh.close()

def is_code_saved(qr_code):
    saved_codes=get_saved_codes()
    if qr_code in saved_codes.values():
        return True
    return False

def get_code_saved_name(qr_code):
    saved_codes=get_saved_codes()
    for key in saved_codes.keys():
        if qr_code == saved_codes[key]:
            return key
    return None

def get_history():
    histfile=_get_user_histfile()
    codes = list()
    try:
        fh = open(histfile,'rb')
        codes=pickle.load(fh)
        fh.close()
    except:
        codes = list()
    return codes

def add_history(qr_code):
    if not isinstance(qr_code, str):
        return
    histfile=_get_user_histfile()

    dt_now = datetime.now()
    now = dt_now.strftime("%Y-%m-%d %H:%M:%S")
    codes = get_history()
    fh_w = open(histfile, 'wb')

    entry = [now, qr_code]
    codes.insert(0, entry)
    while len(codes) > hist_max:
        del codes[-1]
    pickle.dump(codes, fh_w)
    fh_w.close()

def clear_history():
    histfile=_get_user_histfile()
    codes=list()

    fh_w = open(histfile, 'wb')
    pickle.dump(codes, fh_w)
    fh_w.close()
    

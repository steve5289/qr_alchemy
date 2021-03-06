### Saved Lib
# Provides the ability to query, add and delete saved qr codes.

import os
import pickle
from datetime import datetime

import qralchemy.common as qr_common

savefile=""

def set_savefile(file):
    global savefile
    savefile=file

def _get_user_savefile():
    global savefile
    if not savefile:
        qr_user_configdir=".config/qralchemy/"
        filename="saved_qr.dat"
        homedir=qr_common.get_homedir()
        savedir=homedir + '/' + qr_user_configdir
        savefile=savedir + filename
        if not os.path.isdir(savedir):
            os.makedirs(savedir, exist_ok=True)
    return savefile
    
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

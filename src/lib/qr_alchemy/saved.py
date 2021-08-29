import os
import pickle

qr_user_configdir=".config/qr_alchemy/"
savefile="saved_qr.dat"
histfile="history_qr.dat"

def _get_homedir():
    if "HOME" in  os.environ:
        return os.environ['HOME']
    else:
        return os.environ['/']

def _get_user_savefile():
    homedir=_get_homedir()
    qr_userconfig=homedir + qr_user_configdir + savefile
    return qr_userconfig
    
def get_saved_codes():
    savefile=_get_user_savefile()


    try:
        fh = open(savefile,'r')
        codes=pickle.load(fh)
        fh.close()
    except:
        codes = dict()
    return codes

def set_saved_code(name,qr_code):
    savefile=_get_user_savefile()
    fh = open(savefile, 'wb')
    saved_codes=get_saved_codes()
    
    saved_codes[name]=qr_type
    pickle.dump(saved_codes, savefile)
    close(fh)

        
    

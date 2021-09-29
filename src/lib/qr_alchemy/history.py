import os
import pickle
from datetime import datetime

hist_max=10

def _get_homedir():
    if "HOME" in os.environ:
        return os.environ['HOME'] + '/'
    else:
        return os.environ['/']

def set_histfile(file):
    global histfile
    histfile=file

def _get_user_histfile():
    global histfile
    if not histfile:
        qr_user_configdir=".config/qr_alchemy/"
        filename="history_qr.dat"
        homedir=_get_homedir()
        histfile=homedir + qr_user_configdir + filename
        if not os.path.isdir(homedir + qr_user_configdir):
           os.mkdir(homedir + qr_user_configdir)
    return histfile
    
def get_history():
    global histfile
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
    

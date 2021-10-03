### History Lib
# Provides the ability to add, query and clear the code history

import os
import pickle
from datetime import datetime

import qr_alchemy.config as qr_config
import qr_alchemy.common as qr_common

max_hist=10
histfile=""

def set_max_hist(num):
    global max_hist
    if num != max_hist:
        qr_config.update_config('general', 'max_hist', num)
        max_hist=num
        trim_history()

def get_max_hist():
    global max_hist
    config = qr_config.get_config()
    if 'general' in config and 'max_hist' in config['general']:
        max_hist = int(config['general']['max_hist'])
    return max_hist

def set_histfile(file):
    global histfile
    histfile=file

def _get_user_histfile():
    global histfile
    if not histfile:
        qr_user_configdir=".config/qr_alchemy/"
        filename="history_qr.dat"
        homedir=qr_common.get_homedir()
        histfile=homedir + qr_user_configdir + filename
        if not os.path.isdir(homedir + qr_user_configdir):
           os.mkdir(homedir + qr_user_configdir)
    return histfile
    
def get_history():
    global histfile
    histfile=_get_user_histfile()
    codes = list()

    get_max_hist()

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

    entry = [now, qr_code]
    codes.insert(0, entry)
    while len(codes) > max_hist:
        del codes[-1]
    fh_w = open(histfile, 'wb')
    pickle.dump(codes, fh_w)
    fh_w.close()

def trim_history():
    codes = get_history()
    updated=False
    while len(codes) > max_hist:
        del codes[-1]
        updated=True
    if updated:
        fh_w = open(histfile, 'wb')
        pickle.dump(codes, fh_w)
        fh_w.close()

def clear_history():
    histfile=_get_user_histfile()
    codes=list()

    fh_w = open(histfile, 'wb')
    pickle.dump(codes, fh_w)
    fh_w.close()
    

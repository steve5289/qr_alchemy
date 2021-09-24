
import gi
import subprocess
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk,Gio,Gdk, GdkPixbuf
import qr_alchemy.gui as gui
import tempfile

def generate_qr_img(qr_code):
    prog = 'qrencode'
    
    fh = tempfile.NamedTemporaryFile()
    tmpfile=fh.name

    args = [ '-o', tmpfile,'-s',100, qr_code]
    cmd=subprocess.run([prog, '-o', tmpfile, qr_code])

    print('tmpfile:', tmpfile)

    image_gui = gui.ResizableImage(path=tmpfile)
    fh.close()
    return image_gui


import gi
import subprocess
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk,Gio,Gdk, GdkPixbuf
import qr_alchemy.gui as gui

def generate_qr_img(qr_code):
    prog = 'qrencode'
    image_type="PNG"
    
    cmd=subprocess.run([prog, '-o', '-', '-t', image_type, qr_code], capture_output=True)

    return gui.ResizableImage(image_data=cmd.stdout, image_type='image/'+image_type)

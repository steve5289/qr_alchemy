### Generate Lib
# Library for the generation of qr code images

import gi
import subprocess
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk,Gio,Gdk, GdkPixbuf

import qralchemy.gui as gui

def generate_qr_img(qr_code):
    prog = 'qrencode'
    image_type="PNG"
    
    cmd=subprocess.run([prog, '-o', '-', '-t', image_type, qr_code], capture_output=True)

    # Not sure I like this, but also not sure how to really pass an image as 
    # the output, so this is how it's done
    return gui.ResizableImage(image_data=cmd.stdout, image_type='image/'+image_type)

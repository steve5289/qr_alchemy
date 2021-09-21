
import gi
import subprocess
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk,Gio,Gdk, GdkPixbuf

def generate_qr_img(qr_code):
    prog = 'qrencode'
    tmpfile="/tmp/qr_code.png"
    args = [ '-o', tmpfile,'-s',100, qr_code]
    cmd=subprocess.run([prog, '-o', tmpfile, qr_code])

    return Gtk.Image.new_from_file(tmpfile)

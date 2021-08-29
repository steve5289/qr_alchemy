
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class EntryDialog(Gtk.MessageDialog):
    en_name = Gtk.Entry()
    state=Gtk.ResponseType.CANCEL
    name=""
    def __init__(self, parent,title,message):
        Gtk.MessageDialog.__init__(self, title=title)

        dialog = self.get_content_area()

        ## Top Box
        box_t = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=1)
        dialog.pack_start(box_t, True, True, 0)

        # Label
        lb_desc = Gtk.Label(label="Please Enter a name to give the qr code that will be saved:")
        lb_desc.set_line_wrap(True)
        box_t.pack_start(lb_desc, False, True, 0)
    
        # Entry
        box_t.pack_start(self.en_name, False, True, 0)

        bu_cancel = Gtk.Button(label="Cancel")
        bu_cancel.connect("clicked", self.bu_cancel_clicked)
        bu_ok = Gtk.Button(label="Ok")
        bu_ok.connect("clicked", self.bu_ok_clicked)

        box_b = Gtk.Box(spacing=1)
        box_t.pack_end(box_b, False, True, 0)
        box_b.pack_start(bu_cancel,  False, True, 0)
        box_b.pack_end(bu_ok, False, True, 0)

    def bu_cancel_clicked(self, qr_code):
        self.state=Gtk.ResponseType.CANCEL
        self.destroy()
        
    def bu_ok_clicked(self, qr_code):
        self.state=Gtk.ResponseType.OK
        self.name=self.en_name.get_text()
        self.destroy()
        
    def get_name(self):
        return self.name

    def get_state(self):
        return self.state

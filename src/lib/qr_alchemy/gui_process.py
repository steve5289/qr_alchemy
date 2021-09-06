
import gi
import qr_alchemy.process as qr_process
import qr_alchemy.saved as qr_saved
import qr_alchemy.gui as gui

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class QrActionWindow(Gtk.Window):
    bu_save=Gtk.Button(label="Save")
    qr_code=""
    def __init__(self, qr_code):
        Gtk.Window.__init__(self, title="QR Code Detected")

        self.qr_code=qr_code
        qr_saved.add_history(qr_code)

        ## Top Box
        box_t = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=1)
        self.add(box_t)

        # Label
        lb_desc = Gtk.Label(label="A qr code has been detected in this image, what would you like to do with it?\n\nQR Code:\n" + qr_code)
        lb_desc.set_line_wrap(True)
        box_t.pack_start(lb_desc, False, True, 0)

        ## Bottom Box
        box_b = Gtk.Box(spacing=1)
        box_t.pack_end(box_b, False, True, 0)

        # Buttons
        bu_cancel = Gtk.Button(label="Do Nothing")
        bu_cancel.connect("clicked", self.bu_cancel_clicked)
        bu_save = Gtk.Button(label="Save")
        bu_save.connect("clicked", self.bu_save_clicked)
        bu_run = Gtk.Button(label="Run")
        bu_run.connect("clicked", self.bu_run_clicked)
        

        
        box_b.pack_start(bu_cancel,  False, True, 0)
        box_b.pack_end(bu_run, False, True, 0)
        box_b.pack_end(bu_save, False, True, 24)
        

    def bu_save_clicked(self, qr_code):
        save_window = gui.EntryDialog(
           self,
           title="QR Save",
           message="Please Enter a name to give the qr code that will be saved:"        
        )
        save_window.show_all()
        save_window.run()

        name = save_window.get_name()
        state = save_window.get_state()

        if state == Gtk.ResponseType.OK:
            print("got name:" + name)
            qr_saved.set_saved_code(name,self.qr_code)

    def bu_run_clicked(self,qr_code):
        qr_process.qr_code_handler(self.qr_code)
        self.destroy()
        return

    def bu_cancel_clicked(self,qr_code):
        self.destroy()
        return

def qr_gui_handle_code(qr_code):
    win = QrActionWindow(qr_code=qr_code)
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()

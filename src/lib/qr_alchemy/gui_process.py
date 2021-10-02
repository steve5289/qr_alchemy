
import gi
import qr_alchemy.process as qr_process
import qr_alchemy.generate as qr_generate
import qr_alchemy.saved as qr_saved
import qr_alchemy.history as qr_history
import qr_alchemy.gui as gui

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class QrActionWindow(Gtk.Window):
    bu_save=Gtk.Button(label="Save")
    qr_code=""
    def __init__(self, qr_code, save_history=True,display_image=False):
        Gtk.Window.__init__(self, title="QR Code Detected")

        self.qr_code=qr_code
        if save_history:
            qr_history.add_history(qr_code)

        ## Top Box
        box_t = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=1)
        self.add(box_t)

        # Buttons
        ## Bottom Box
        box_b = Gtk.Box(spacing=1)
        box_t.pack_start(box_b, False, True, 0)

        bu_cancel = Gtk.Button(label="Done")
        bu_cancel.connect("clicked", self.bu_cancel_clicked)
        self.bu_save = Gtk.Button(label="Save")
        self.bu_save.connect("clicked", self.bu_save_clicked)
        bu_run = Gtk.Button(label="Run")
        bu_run.connect("clicked", self.bu_run_clicked)
        self.refresh_save_state()
        
        box_b.pack_start(bu_cancel,  False, True, 0)
        box_b.pack_end(bu_run, False, True, 0)
        box_b.pack_end(self.bu_save, False, True, 24)

        # Label
        lb_desc = Gtk.Label(label="What would you like to do with this qr code?")
        lb_desc.set_line_wrap(True)
        lb_desc.set_alignment(0,0)
        box_t.pack_start(lb_desc, False, True, 10)

        seperator = Gtk.Separator()
        box_t.pack_start(seperator, False, True, 10)

        # QR code Display
        if display_image:
            img_code = qr_generate.generate_qr_img(qr_code)
            box_t.pack_start(img_code, True, True, 0)

        # Label
        lb_code = Gtk.Label(label=qr_code)
        lb_code.set_alignment(0,0)
        lb_code.set_selectable(True)
        lb_code.set_line_wrap(True)
        lb_code.set_line_wrap_mode(2)
        box_t.pack_start(lb_code, False, False, 0)


        
    def refresh_save_state(self):
        if qr_saved.is_code_saved(self.qr_code):
            code_name=qr_saved.get_code_saved_name(self.qr_code)
            self.bu_save.set_label("Delete Saved")
        else:
            self.bu_save.set_label("Save")

    def bu_save_clicked(self, button):
        if qr_saved.is_code_saved(self.qr_code):
            code_name=qr_saved.get_code_saved_name(self.qr_code)
            ok_window = gui.OkDialog(
                self,
                title="Really Delete?",
                message="Are you sure you want to delete saved code: " +code_name + "?"
            )
            ok_window.show_all()
            ok_window.run()
            state = ok_window.get_state()
            if state == Gtk.ResponseType.OK:
                qr_saved.delete_saved_code(code_name)
        else:
            save_window = gui.EntryDialog(
                self,
                title="QR Save",
                message="Please Enter a name to give the qr code that will be saved:"        
            )
            save_window.show_all()
            save_window.run()

            name = save_window.get_result()
            state = save_window.get_state()

            if state == Gtk.ResponseType.OK:
                qr_saved.set_saved_code(name,self.qr_code)
        self.refresh_save_state()

    def bu_run_clicked(self,button):
        qr_process.qr_code_handler(self.qr_code)
        self.destroy()
        return

    def bu_cancel_clicked(self,button):
        self.destroy()
        return

def qr_gui_handle_code(qr_code, save_history=True, display_image=False):
    win = QrActionWindow(qr_code=qr_code, save_history=save_history,display_image=display_image)
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()

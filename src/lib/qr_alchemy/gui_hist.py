
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk,Gio

import qr_alchemy.process as qr_process
import qr_alchemy.history as qr_history
import qr_alchemy.gui as gui
import qr_alchemy.gui_process as gui_process
import qr_alchemy.gui_config as gui_config
import qr_alchemy.gui_saved as gui_saved


# The general format of the history, saved, and display dialogs is very 
# similar. Should figure out a way to see if this can be made more generic
class QrHistPage(Gtk.Window):
    hist_codes=list()
    box = None
    def __init__(self):
        self.box = Gtk.Box()

        # Creating the ListStore model
        self.ls_hist = Gtk.ListStore(str, str)
        self.refresh_history()

        self.tv_hist = Gtk.TreeView(model=self.ls_hist)
        for i, column_title in enumerate(
            ["Date", "QR Code"]
        ):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            self.tv_hist.append_column(column)
            if column_title == "QR Code":
                column.set_resizable(True)
                column.set_max_width(50)
        select = self.tv_hist.get_selection()
        select.set_mode(Gtk.SelectionMode.MULTIPLE)
        self.tv_hist.set_activate_on_single_click(True)
        self.tv_hist.connect('row-activated', self.selected_hist_entry)

        # setting up the layout, putting the treeview in a scrollwindow, and the buttons in a row
        stv_hist = Gtk.ScrolledWindow()
        stv_hist.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        stv_hist.add(self.tv_hist)
        self.box.pack_start(stv_hist, True, True, 1)

    def refresh_history(self):
        self.ls_hist.clear()
        self.hist_codes=qr_history.get_history()
        for row in self.hist_codes:
            self.ls_hist.append(row)

    def selected_hist_entry(self,null1, null2, null3):
        path,data = self.tv_hist.get_cursor()
        if path == None:
            return
        indices = path.get_indices()
        
        
        qr_code=self.hist_codes[indices[0]][1]
        
        gui_process.qr_gui_handle_code(qr_code,save_history=False, display_image=True)
        select = self.tv_hist.get_selection()
        select.unselect_all()

    def get_box(self):
        return self.box


        
def qr_gui_main():
    win = QrMainWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()


import gi
import qr_alchemy.process as qr_process
import qr_alchemy.saved as qr_saved
import qr_alchemy.gui as gui
import qr_alchemy.gui_process as gui_process
import qr_alchemy.gui_config as gui_config
import qr_alchemy.gui_saved as gui_saved

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk,Gio

class QrHistPage(Gtk.Window):
    # HACK ALERT!!!!
    # This uses the select multiple entries for the treeviews. This is 
    # because this select option doesn't try to auto select things when 
    # the tabs are switched.
    # Currently picking an entry is handled by adding a function to the 
    # selection that always says don't select. This is done as it prevents 
    # selection but also allows us to call things when there is a selection.
    # 
    # There must be a better way of doing this... But I haven't found it yet...
    hist_codes=list()
    disable_actions=False
    box = Gtk.Box()
    def __init__(self):
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
        select.set_select_function(self.selected_hist_entry)

        # setting up the layout, putting the treeview in a scrollwindow, and the buttons in a row
        stv_hist = Gtk.ScrolledWindow()
        stv_hist.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        stv_hist.add(self.tv_hist)
        self.box.pack_start(stv_hist, True, True, 1)

    def refresh_history(self):
        self.disable_actions=True
        self.hist_codes=qr_saved.get_history()
        for row in self.hist_codes:
            self.ls_hist.append(row)
        self.disable_actions=False

    def selected_hist_entry(self,null1, null2, null3, null4):
        if self.disable_actions:
            return
        path,data = self.tv_hist.get_cursor()
        if path == None:
            return
        indices = path.get_indices()
        
        
        qr_code=self.hist_codes[indices[0]][1]
        
        gui_process.qr_gui_handle_code(qr_code,save_history=False)
        return False

    def get_box(self):
        return self.box


        
def qr_gui_main():
    win = QrMainWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()

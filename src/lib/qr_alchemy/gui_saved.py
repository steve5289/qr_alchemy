
import gi
import qr_alchemy.process as qr_process
import qr_alchemy.saved as qr_saved
import qr_alchemy.gui as gui
import qr_alchemy.gui_process as gui_process
import qr_alchemy.gui_config as gui_config

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class QrSavedPage():
    # HACK ALERT!!!!
    # This uses the select multiple entries for the treeviews. This is 
    # because this select option doesn't try to auto select things when 
    # the tabs are switched.
    # Currently picking an entry is handled by adding a function to the 
    # selection that always says don't select. This is done as it prevents 
    # selection but also allows us to call things when there is a selection.
    # 
    # There must be a better way of doing this... But I haven't found it yet...
    tv_saved = Gtk.TreeView()
    saved_codes=list()
    saved_code=dict()
    box=Gtk.Box()

    def __init__(self):

        # Creating the ListStore model
        self.ls_saved = Gtk.ListStore(str, str)
        self.refresh_saved()

        self.tv_saved = Gtk.TreeView(model=self.ls_saved)
        for i, column_title in enumerate(
            ["Name", "QR Code"]
        ):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            self.tv_saved.append_column(column)
            if column_title == "QR Code":
                column.set_resizable(True)
                column.set_max_width(50)
        select = self.tv_saved.get_selection()
        select.set_mode(Gtk.SelectionMode.MULTIPLE)
        self.tv_saved.set_activate_on_single_click(True)
        self.tv_saved.connect('row-activated', self.selected_saved_entry)

        # setting up the layout, putting the treeview in a scrollwindow, and the buttons in a row
        stv_saved = Gtk.ScrolledWindow()
        stv_saved.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        stv_saved.add(self.tv_saved)
        self.box.pack_start(stv_saved, True, True, 1)

    def refresh_saved(self):

        self.saved_code=qr_saved.get_saved_codes()
        self.ls_saved.clear()
        self.saved_codes=sorted(self.saved_code.keys())
        for name in self.saved_codes:
            self.ls_saved.append([name, self.saved_code[name]])

    def selected_saved_entry(self,null1,null2,null3):
        path,data = self.tv_saved.get_cursor()
        if path == None:
            return
        indices = path.get_indices()
        
        
        qr_code=self.saved_code[self.saved_codes[indices[0]]]
        
        gui_process.qr_gui_handle_code(qr_code,save_history=False,display_image=True)
        self.refresh_saved()
        select = self.tv_saved.get_selection()
        select.unselect_all()

    def get_box(self):
        return self.box

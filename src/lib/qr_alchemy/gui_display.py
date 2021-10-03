
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import qr_alchemy.saved as qr_saved
import qr_alchemy.gui as gui
import qr_alchemy.gui_process as gui_process
import qr_alchemy.plugins as qr_plugins



# The general format of the history, saved, and display dialogs is very 
# similar. Should figure out a way to see if this can be made more generic
class QrDisplayPage():
    tv_display = None
    plugins=list()
    plugin_map=dict()
    box=Gtk.Box()

    def __init__(self):
        # Creating the ListStore model
        self.ls_display = Gtk.ListStore(str)
        self.refresh()

        self.tv_display = Gtk.TreeView(model=self.ls_display)
        for i, column_title in enumerate(
            ["Plugin"]
        ):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            self.tv_display.append_column(column)
            if column_title == "QR Code":
                column.set_resizable(True)
                column.set_max_width(50)
        select = self.tv_display.get_selection()
        select.set_mode(Gtk.SelectionMode.MULTIPLE)
        self.tv_display.set_activate_on_single_click(True)
        self.tv_display.connect('row-activated', self.selected_display_entry)

        # setting up the layout, putting the treeview in a scrollwindow, and the buttons in a row
        stv_display = Gtk.ScrolledWindow()
        stv_display.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        stv_display.add(self.tv_display)
        self.box.pack_start(stv_display, True, True, 1)

    def refresh(self):
        self.plugin_map=qr_plugins.get_output_plugins()
        self.ls_display.clear()
        self.plugins=sorted(self.plugin_map.keys())
        for name in self.plugins:
            self.ls_display.append([name])

    def selected_display_entry(self,null1,null2,null3):
        path,data = self.tv_display.get_cursor()
        if path == None:
            return
        indices = path.get_indices()
        
        
        plugin=self.plugins[indices[0]]
        
        rc,qr_code = qr_plugins.run_output_plugin(plugin)
        if rc == 0 and qr_code != '':
            gui_process.qr_gui_handle_code(qr_code, display_image=True)
        qr_plugins.stop_output_plugin(plugin)
        select = self.tv_display.get_selection()
        select.unselect_all()
        

    def get_box(self):
        return self.box

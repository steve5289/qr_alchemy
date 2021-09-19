
import gi
import qr_alchemy.process as qr_process
import qr_alchemy.saved as qr_saved
import qr_alchemy.gui as gui
import qr_alchemy.gui_process as gui_process
import qr_alchemy.gui_config as gui_config

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk,Gio

import traceback

class QrSavedWindow(Gtk.Window):
    # HACK ALERT!!!!
    # These variables are for stopping this program from automatically launching 
    # the first thing shown in the list (due ti it getting 'selected'
    # These must be a better way, but I can't find one right now...
    tv_saved = Gtk.TreeView()
    saved_codes=list()
    saved_code=dict()
    hist_codes=list()
    disable_actions=False
    saved_click=0
    hist_click=0
    def __init__(self):
        super().__init__(title="QR Alchemy")
        self.set_border_width(0)

        self.notebook = Gtk.Notebook()
        self.add(self.notebook)
        self.notebook.append_page(self.page_saved(), Gtk.Label('Saved'))
        self.notebook.append_page(self.page_history(), Gtk.Label('History'))


        self.hb = Gtk.HeaderBar()
        self.hb.set_show_close_button(True)
        self.hb.props.title="QR Alchemy"
        self.set_titlebar(self.hb)

        bu_conf = Gtk.Button()
        bu_conf_icon = Gio.ThemedIcon(name='emblem-system')
        bu_conf_image = Gtk.Image.new_from_gicon(bu_conf_icon, Gtk.IconSize.MENU)
        bu_conf.add(bu_conf_image)
        bu_conf.connect("clicked", self.bu_config_clicked)
        self.hb.pack_end(bu_conf)

        self.show_all()

    def bu_config_clicked(self, button):
        config_window = gui_config.qr_gui_config()
        self.first_select = 1
        

    def page_saved(self):

        box = Gtk.Box()
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
        select.set_mode(Gtk.SelectionMode.NONE)
        self.tv_saved.connect('row-activated', self.selected_saved_entry)

        # setting up the layout, putting the treeview in a scrollwindow, and the buttons in a row
        stv_saved = Gtk.ScrolledWindow()
        stv_saved.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        box.pack_start(stv_saved, True, True, 1)
        stv_saved.add(self.tv_saved)
        return box

    def refresh_saved(self):

        self.disable_actions=True
        self.saved_code=qr_saved.get_saved_codes()
        self.ls_saved.clear()
        self.saved_codes=sorted(self.saved_code.keys())
        for name in self.saved_codes:
            self.ls_saved.append([name, self.saved_code[name]])
        self.disable_actions=False

    def selected_saved_entry(self,thing1, thing2, tv_saved):
        if self.disable_actions:
            return
        path,data = self.tv_saved.get_cursor()
        if path == None:
            return
        indices = path.get_indices()
        
        
        qr_code=self.saved_code[self.saved_codes[indices[0]]]
        
        #traceback.print_stack()
        gui_process.qr_gui_handle_code(qr_code)
        #self.refresh_saved()

    def page_history(self):
        box = Gtk.Box()
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
        select.set_mode(Gtk.SelectionMode.NONE)
        self.tv_hist.connect('row-activated', self.selected_hist_entry)

        # setting up the layout, putting the treeview in a scrollwindow, and the buttons in a row
        stv_hist = Gtk.ScrolledWindow()
        stv_hist.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        box.pack_start(stv_hist, True, True, 1)
        stv_hist.add(self.tv_hist)
        return box

    def refresh_history(self):
        self.disable_actions=True
        self.hist_codes=qr_saved.get_history()
        for row in self.hist_codes:
            self.ls_hist.append(row)
        self.disable_actions=False

    def selected_hist_entry(self, thing1, thing2, tv_hist):
        if self.disable_actions:
            return
        #if self.hist_click == 0:
        path,data = self.tv_hist.get_cursor()
        if path == None:
            return
        indices = path.get_indices()
        
        
        qr_code=self.hist_codes[indices[0]][1]
        
        gui_process.qr_gui_handle_code(qr_code)
        #self.refresh_saved()


        
def qr_gui_saved():
    win = QrSavedWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()

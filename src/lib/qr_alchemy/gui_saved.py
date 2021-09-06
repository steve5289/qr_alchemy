
import gi
import qr_alchemy.process as qr_process
import qr_alchemy.saved as qr_saved
import qr_alchemy.gui as gui
import qr_alchemy.gui_process as gui_process
import qr_alchemy.gui_config as gui_config

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk,Gio

class QrSavedWindow(Gtk.Window):
    # HACK ALERT!!!!
    # These variables are for stopping this program from automatically launching 
    # the first thing shown in the list (due ti it getting 'selected'
    # These must be a better way, but I can't find one right now...
    first_select=0
    first_select_hist=0
    first_select_sav=0
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
        saved=qr_saved.get_saved_codes()

        box = Gtk.Box()
        # Creating the ListStore model
        ls_saved = Gtk.ListStore(str, str)
        for name in sorted(saved.keys()):
            ls_saved.append([name, saved[name]])

        tv_saved = Gtk.TreeView(model=ls_saved)
        for i, column_title in enumerate(
            ["Name", "QR Code"]
        ):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            tv_saved.append_column(column)
            if column_title == "QR Code":
                column.set_resizable(True)
                column.set_max_width(50)
        select = tv_saved.get_selection()
        #select.set_mode(Gtk.SelectionMode.SINGLE)
        tv_saved.connect('cursor-changed', self.selected_saved_entry)

        # setting up the layout, putting the treeview in a scrollwindow, and the buttons in a row
        stv_saved = Gtk.ScrolledWindow()
        stv_saved.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        box.pack_start(stv_saved, True, True, 1)
        stv_saved.add(tv_saved)
        return box

    def selected_saved_entry(self, tv_saved):
        if self.first_select_sav == 1 or self.first_select == 0:
            #model, treeitr = selection.get_selected()
            selected = tv_saved.get_selection()
            data, i = selected.get_selected()
            if i is not None:
                qr_code=data[i][1]
                gui_process.qr_gui_handle_code(qr_code)
        self.first_select_sav=1
        self.first_select = 1

    def page_history(self):
        history=qr_saved.get_history()

        box = Gtk.Box()
        # Creating the ListStore model
        ls_hist = Gtk.ListStore(str, str)
        for entry in history:
            ls_hist.append(list(entry))

        tv_hist = Gtk.TreeView(model=ls_hist)
        for i, column_title in enumerate(
            ["Date", "QR Code"]
        ):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            tv_hist.append_column(column)
            if column_title == "QR Code":
                column.set_resizable(True)
                column.set_max_width(50)
        select = tv_hist.get_selection()
        #select.set_mode(Gtk.SelectionMode.SINGLE)
        tv_hist.connect('cursor-changed', self.selected_hist_entry)

        # setting up the layout, putting the treeview in a scrollwindow, and the buttons in a row
        stv_hist = Gtk.ScrolledWindow()
        stv_hist.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        box.pack_start(stv_hist, True, True, 1)
        stv_hist.add(tv_hist)
        return box

    def selected_hist_entry(self, tv_hist):
        if self.first_select_hist == 1 or self.first_select == 0:
            #model, treeitr = selection.get_selected()
            selected = tv_hist.get_selection()
            data, i = selected.get_selected()
            if i is not None:
                qr_code=data[i][1]
                gui_process.qr_gui_handle_code(qr_code)
        self.first_select_hist=1
        self.first_select = 1

        
def qr_gui_saved():
    win = QrSavedWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()

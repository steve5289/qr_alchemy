
import gi
import qr_alchemy.gui_config as gui_config
import qr_alchemy.gui_saved as gui_saved
import qr_alchemy.gui_hist as gui_hist

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk,Gio

import traceback

class QrMainWindow(Gtk.Window):
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
    hist_codes=list()
    disable_actions=False
    hist_click=0
    def __init__(self):
        super().__init__(title="QR Alchemy")
        self.set_border_width(0)

        # Title
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

        # Pages
        self.notebook = Gtk.Notebook()
        self.add(self.notebook)
        page_saved = gui_saved.QrSavedPage()
        page_hist = gui_hist.QrHistPage()
        
        
        self.notebook.append_page(page_saved.get_box(), Gtk.Label('Saved'))
        self.notebook.append_page(page_hist.get_box(), Gtk.Label('History'))

        self.show_all()

    def bu_config_clicked(self, button):
        config_window = gui_config.qr_gui_config()
        self.first_select = 1
        
        
def qr_gui_main():
    win = QrMainWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()

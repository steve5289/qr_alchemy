
import gi
import qr_alchemy.gui_config as gui_config
import qr_alchemy.gui_saved as gui_saved
import qr_alchemy.gui_hist as gui_hist
import qr_alchemy.gui_display as gui_disp

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk,Gio

class QrMainWindow(Gtk.Window):
    page_saved = None
    page_hist = None
    page_disp = None
    def __init__(self):
        super().__init__(title="QR Alchemy")
        self.set_border_width(0)

        # Title
        self.hb = Gtk.HeaderBar()
        self.hb.set_show_close_button(True)
        self.hb.props.title="QR Alchemy"
        self.set_titlebar(self.hb)

        bu_conf = Gtk.Button()
        bu_conf_icon = Gio.ThemedIcon(name='preferences-system-symbolic')
        bu_conf_image = Gtk.Image.new_from_gicon(bu_conf_icon, Gtk.IconSize.MENU)
        bu_conf.add(bu_conf_image)
        bu_conf.connect("clicked", self.bu_config_clicked)
        self.hb.pack_end(bu_conf)

        # Pages
        self.notebook = Gtk.Notebook()
        self.add(self.notebook)
        
        self.page_saved = gui_saved.QrSavedPage()
        self.page_hist = gui_hist.QrHistPage()
        self.page_disp = gui_disp.QrDisplayPage()
        
        self.notebook.append_page(self.page_disp.get_box(), Gtk.Label('Display'))
        self.notebook.append_page(self.page_saved.get_box(), Gtk.Label('Saved'))
        self.notebook.append_page(self.page_hist.get_box(), Gtk.Label('History'))
        self.notebook.connect("switch-page", self.nb_page_changed)

        self.show_all()

    def bu_config_clicked(self, button):
        config_window = gui_config.qr_gui_config()
        self.page_hist.refresh_history()
        
    def nb_page_changed(self, notebook, page, page_num):
        if page_num == 1:
            self.page_saved.refresh_saved()
        elif page_num == 2:
            self.page_hist.refresh_history()
            

def qr_gui_main():
    win = QrMainWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()

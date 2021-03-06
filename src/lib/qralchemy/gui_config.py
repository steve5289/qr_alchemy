### Configuration Gui Lib
# Provides the configuration window

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk,Gio

import qralchemy.process as qr_process
import qralchemy.plugins as qr_plugins
import qralchemy.gui as gui
import qralchemy.config as qr_config
import qralchemy.gui_config_general as config_general
import qralchemy.gui_config_actions as config_actions
import qralchemy.gui_config_plugins as config_plugins


class QRConfig(Gtk.Window):
    state=Gtk.ResponseType.CANCEL
    name=""
    def __init__(self):
        Gtk.Window.__init__(self, title="Configuration")

        # Window Header Bar
        self.hb = Gtk.HeaderBar()
        self.hb.set_show_close_button(True)
        self.hb.props.title="Configuration"

        bu_close = Gtk.Button()
        bu_close_icon = Gio.ThemedIcon(name='go-previous-symbolic')
        bu_close_image = Gtk.Image.new_from_gicon(bu_close_icon, Gtk.IconSize.MENU)
        bu_close.add(bu_close_image)
        bu_close.connect("clicked", self.bu_close_clicked)

        self.hb.pack_start(bu_close)
        self.set_titlebar(self.hb)
        self.connect

        ## Notebooks/Pages
        # Each page is a box provided by annother lib
        self.notebook = Gtk.Notebook()
        self.add(self.notebook)
        page_general=config_general.QRGeneralConfig(self)
        self.notebook.append_page(page_general.get_box(), Gtk.Label('General'))
        page_action=config_actions.QRActionConfig(self)
        self.notebook.append_page(page_action.get_box(), Gtk.Label('Action'))
        page_inp_plugins=config_plugins.QRPluginConfig(parent=self,plugin_type='Input')
        self.notebook.append_page(page_inp_plugins.get_box(), Gtk.Label('In Plugin'))
        page_out_plugins=config_plugins.QRPluginConfig(parent=self,plugin_type='Output')
        self.notebook.append_page(page_out_plugins.get_box(), Gtk.Label('Out Plugin'))

    
    def bu_close_clicked(self,button):
        self.destroy()

def qr_gui_config():
    win = QRConfig()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()

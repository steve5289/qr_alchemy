
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk,Gio
import qr_alchemy.process as qr_process
import qr_alchemy.plugins as qr_plugins
import qr_alchemy.gui as gui
import qr_alchemy.config as qr_config
import qr_alchemy.gui_config_general as config_general
import qr_alchemy.gui_config_actions as config_actions


class QRConfig(Gtk.Window):
    state=Gtk.ResponseType.CANCEL
    name=""
    def __init__(self):
        Gtk.Window.__init__(self, title="QR Code Detected")
        #Gtk.Dialog.__init__(self, title='Configuration')

        #dialog = self.get_content_area()
        self.hb = Gtk.HeaderBar()
        self.hb.set_show_close_button(True)
        self.hb.props.title="Configuration"

        bu_close = Gtk.Button()
        bu_close_icon = Gio.ThemedIcon(name='carousel-arrow-previous-symbolic')
        bu_close_image = Gtk.Image.new_from_gicon(bu_close_icon, Gtk.IconSize.MENU)
        bu_close.add(bu_close_image)
        bu_close.connect("clicked", self.bu_close_clicked)

        self.hb.pack_start(bu_close)
        self.set_titlebar(self.hb)
        self.connect

        ## Top Box
        print('test1')
        self.notebook = Gtk.Notebook()
        self.add(self.notebook)
        page_general=config_general.QRGeneralConfig()
        self.notebook.append_page(page_general.get_box(), Gtk.Label('General'))
        print('test2')
        page_action=config_actions.QRActionConfig()
        self.notebook.append_page(page_action.get_box(), Gtk.Label('Actions'))
        print('test3')

    
    def bu_close_clicked(self,button):
        self.destroy()

def qr_gui_config():
    win = QRConfig()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()

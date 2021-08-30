
import gi
import qr_alchemy.process as qr_process
import qr_alchemy.saved as qr_saved
import qr_alchemy.gui as gui

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class QrSavedWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Treeview Filter Demo")
        self.set_border_width(0)


        self.add(self.page_history())


        self.show_all()
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

        # setting up the layout, putting the treeview in a scrollwindow, and the buttons in a row
        stv_hist = Gtk.ScrolledWindow()
        stv_hist.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        box.pack_start(stv_hist, True, True, 1)
        stv_hist.add(tv_hist)
        return box
        


    #def __init__(self):
    #    Gtk.Window.__init__(self, title="Stored QR Codes")
#
#
#        history=qr_saved.get_history()
#
#        ## Top Box
#        box_t = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=1)
#        self.add(box_t)
#
#        # ListStore
#        ls_hist = Gtk.ListStore(str,str)
#        for entry in history:
#            ls_hist.append(list(entry))
#        box_t.pack_start(ls_hist, False, True, 0)
        


def qr_gui_saved():
    win = QrSavedWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()

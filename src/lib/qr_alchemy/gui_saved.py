
import gi
import qr_alchemy.process as qr_process
import qr_alchemy.saved as qr_saved
import qr_alchemy.gui as gui
import qr_alchemy.gui_process as gui_process

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class QrSavedWindow(Gtk.Window):
    first_select=0
    def __init__(self):
        super().__init__(title="QR Alchemy")
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
        if self.first_select == 1:
            #model, treeitr = selection.get_selected()
            selected = tv_hist.get_selection()
            data, i = selected.get_selected()
            if i is not None:
                qr_code=data[i][1]
                gui_process.qr_gui_handle_code(qr_code=qr_code, exit_on_close=False)
        self.first_select=1

        
        



def qr_gui_saved():
    win = QrSavedWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()

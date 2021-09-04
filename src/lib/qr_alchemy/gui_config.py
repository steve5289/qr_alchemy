
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import qr_alchemy.process as qr_process


class QRConfig(Gtk.MessageDialog):
    en_name = Gtk.Entry()
    state=Gtk.ResponseType.CANCEL
    name=""
    def __init__(self, parent,title,message):
        Gtk.MessageDialog.__init__(self, title=title)

        dialog = self.get_content_area()

        ## Top Box
        box_t = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=1)
        dialog.pack_start(box_t, True, True, 0)
        page_a=self.page_actions()
        box_t.pack_start(page_a, True, True,0)

    

    def page_actions(self):
        actions=qr_process.qr_code2action()

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=1)

        # Label
        lb_desc = Gtk.Label(label="Choose what actions to perform based on what type of qr code is recieved:")
        lb_desc.set_line_wrap(True)
        box.pack_start(lb_desc, False, True, 0)

        # Creating the ListStore model
        ls_act = Gtk.ListStore(str, str)
        for key in sorted(actions.keys()):
            ls_act.append([key, actions[key]])

        tv_act = Gtk.TreeView(model=ls_act)
        for i, column_title in enumerate(
            ["Type", "Action"]
        ):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            tv_act.append_column(column)
            if column_title == "Action":
                column.set_resizable(True)
                column.set_max_width(50)
        select = tv_act.get_selection()

        # setting up the layout, putting the treeview in a scrollwindow, and the buttons in a row
        stv_act = Gtk.ScrolledWindow()
        stv_act.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        box.pack_start(stv_act, True, True, 1)
        stv_act.add(tv_act)
        return box

    def bu_cancel_clicked(self, qr_code):
        self.state=Gtk.ResponseType.CANCEL
        self.destroy()
        
    def bu_ok_clicked(self, qr_code):
        if self.en_name.get_text():
            self.state=Gtk.ResponseType.OK
            self.name=self.en_name.get_text()
            self.destroy()
        
    def get_name(self):
        return self.name

    def get_state(self):
        return self.state

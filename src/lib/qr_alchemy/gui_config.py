
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

        # Buttons
        box_h = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=1)
        bu_delete = Gtk.Button(label="Delete")
        bu_delete.connect("clicked", self.bu_delete_clicked)
        bu_add    = Gtk.Button(label="Add")
        bu_add.connect("clicked", self.bu_add_clicked)
        bu_edit   = Gtk.Button(label="Edit")
        bu_add.connect("clicked", self.bu_edit_clicked)
        box_h.pack_start(bu_delete, False, False, 0)
        box_h.pack_end(bu_add, False, False, 0)
        box_h.pack_end(bu_edit, False, False, 0)
        box.pack_start(box_h, True, False, 0)

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

    def bu_delete_clicked(self, qr_code):
        print('delete')
        
    def bu_add_clicked(self, qr_code):
        print('add')
        entryDialog = QRConfigEntry(self,title='bob', message='hello')
        entryDialog.show_all()
        entryDialog.run()
        
    def bu_edit_clicked(self, qr_code):
        print('edit')
        

class QRConfigEntry(Gtk.MessageDialog):
    en_name = Gtk.Entry()
    state=Gtk.ResponseType.CANCEL
    name=""
    def __init__(self, parent,title,message):
        Gtk.MessageDialog.__init__(self, title=title)

        dialog = self.get_content_area()

        ## Top Box
        box_t = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=1)
        dialog.pack_start(box_t, True, True, 0)

        # ComboBox
        action_types = qr_process.get_qr_action_types()
        ls_type = Gtk.ListStore(str)
        for a_type in action_types:
            ls_type.append([a_type])

        cb_type = Gtk.ComboBox.new_with_model(ls_type)
        cb_type.connect('changed', self.cb_type_changed)
        
        
        page_a=self.page_actions()
        box_t.pack_start(page_a, True, True,0)

    
    def cb_type_changed(self, comboBox):
        print('changed')

    def page_actions(self):
        actions=qr_process.qr_code2action()

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=1)

        # Label
        lb_desc = Gtk.Label(label="Choose what actions to perform based on what type of qr code is recieved:")
        lb_desc.set_line_wrap(True)
        box.pack_start(lb_desc, False, True, 0)

        # Buttons
        box_h = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=1)
        bu_cancel = Gtk.Button(label="Cancel")
        bu_cancel.connect("clicked", self.bu_cancel_clicked)
        bu_ok    = Gtk.Button(label="Ok")
        bu_ok.connect("clicked", self.bu_ok_clicked)
        box_h.pack_start(bu_ok, False, False, 0)
        box_h.pack_end(bu_cancel, False, False, 0)
        box.pack_start(box_h, True, False, 0)

        return box

    def bu_ok_clicked(self, qr_code):
        self.state = state=Gtk.ResponseType.OK
        print('ok')
        self.destroy()
        
    def bu_cancel_clicked(self, qr_code):
        self.state = state=Gtk.ResponseType.CANCEL
        print('cancel')
        self.destroy()

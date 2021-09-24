
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk,Gio
import qr_alchemy.process as qr_process
import qr_alchemy.plugins as qr_plugins
import qr_alchemy.gui as gui


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
        box_t = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=1)
        self.add(box_t)
        page_a=self.page_actions()
        box_t.pack_start(page_a, True, True,0)

    
    def bu_close_clicked(self,button):
        self.destroy()

    def page_actions(self):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=1)

        # Label
        lb_desc = Gtk.Label(label="Choose what actions to perform based on what type of qr code is recieved:")
        lb_desc.set_line_wrap(True)
        box.pack_start(lb_desc, False, True, 0)

        # Creating the ListStore model
        self.ls_act = Gtk.ListStore(str, str)
        self.ls_actions_populate(self.ls_act)

        self.tv_act = Gtk.TreeView(model=self.ls_act)
        for i, column_title in enumerate(
            ["Type", "Action"]
        ):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            self.tv_act.append_column(column)
            if column_title == "Action":
                column.set_resizable(True)
                column.set_max_width(50)
        select = self.tv_act.get_selection()

        # setting up the layout, putting the treeview in a scrollwindow
        stv_act = Gtk.ScrolledWindow()
        stv_act.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        # Buttons
        box_h = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=1)
        bu_delete = Gtk.Button(label="Delete")
        bu_delete.connect("clicked", self.bu_delete_clicked)
        bu_add    = Gtk.Button(label="Add")
        bu_add.connect("clicked", self.bu_add_clicked)
        bu_edit   = Gtk.Button(label="Edit")
        bu_edit.connect("clicked", self.bu_edit_clicked)
        box_h.pack_start(bu_delete, False, False, 0)
        box_h.pack_end(bu_add, False, False, 0)
        box_h.pack_end(bu_edit, False, False, 0)

        box.pack_start(stv_act, True, True, 1)
        stv_act.add(self.tv_act)
        box.pack_end(box_h, False, False, 0)
        return box

    def ls_actions_populate(self,listStore):
        self.ls_act.clear()
        self.actions=qr_process.qr_code2action()
        for key in sorted(self.actions.keys()):
            self.ls_act.append([key, ':'.join(self.actions[key])])
        

    def bu_delete_clicked(self, qr_code):
        selected = self.tv_act.get_selection()
        data, i = selected.get_selected()
        
        if i == None:
            return
            
        code_type=data[i][0]
        if code_type == '*':
            return

        ok_window = gui.OkDialog(
           self,
           title="Really Delete?",
           message="Are you sure you want to delete " +code_type + "?"       
        )
        ok_window.show_all()
        ok_window.run()

        state = ok_window.get_state()
        if state != Gtk.ResponseType.OK:
            return

        qr_process.qr_update_configaction(data[i][0], '', '')
        self.ls_actions_populate(self.ls_act)
        
    def bu_add_clicked(self, qr_code):
        entryDialog = QRConfigEntry(self,title='Add New Action')
        entryDialog.connect("destroy", Gtk.main_quit)
        entryDialog.run()

        results=entryDialog.get_results()
        if results['state'] == Gtk.ResponseType.OK and not results['code_type'] in self.actions:
            qr_process.qr_update_configaction(results['code_type'], results['action_type'], results['action_subtype'])
            self.ls_actions_populate(self.ls_act)

    def bu_edit_clicked(self, win):
        selected = self.tv_act.get_selection()
        data, i = selected.get_selected()
        if i is not None:
            code_type=data[i][0]
            
            action = qr_process.qr_get_action(code_type)
            action_type = action[0]
            if len(action) > 1:
                action_subtype = action[1]
            else:
                action_subtype = ''
        
            entryDialog = QRConfigEntry(self,title='Edit Action',code_type=code_type, action_type=action_type, action_subtype=action_subtype)
            entryDialog.run()

            results=entryDialog.get_results()
            if results['state'] == Gtk.ResponseType.OK and (results['action_type'] != action_type or results['action_subtype'] != action_subtype):
                qr_process.qr_update_configaction(code_type, results['action_type'], results['action_subtype'])
                self.ls_actions_populate(self.ls_act)
        

class QRConfigEntry(Gtk.Dialog):
    state=Gtk.ResponseType.CANCEL
    code_type=None
    action_type=None
    plugin=None
    prog=None
    pg_plugin=None
    
    def __init__(self, parent, title, code_type=None, action_type=None, action_subtype=None):
        Gtk.MessageDialog.__init__(self, title=title)

        self.code_type=code_type
        self.action_type=action_type
        if action_type == "Plugin":
            self.plugin=action_subtype
        if action_type == "Program":
            self.prog=action_subtype

        dialog = self.get_content_area()
        
        ## Top Box
        box_t = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=1)
        dialog.pack_start(box_t, True, True, 0)

        ## Code type Box
        box_code_type = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=1)
        box_t.pack_start(box_code_type, False, True, 0)

        # Label
        lb_desc_code = Gtk.Label(label="QR Code Type:")
        lb_desc_code.set_line_wrap(False)
        box_code_type.pack_start(lb_desc_code, False, True, 0)

        # Entry
        en_code = Gtk.Entry()
        if self.code_type != None:
            en_code.set_text(self.code_type)
            en_code.set_editable(False)
            en_code.set_sensitive(False)
        box_code_type.pack_end(en_code, False, True, 0)

        ## Action Box
        box_action = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=1)
        box_t.pack_start(box_action, False, True, 0)

        # Label
        lb_desc_action = Gtk.Label(label="Action:")
        lb_desc_action.set_line_wrap(False)
        box_action.pack_start(lb_desc_action, False, True, 0)

        # ComboBox
        action_types = qr_process.get_qr_action_types()
        ls_type = Gtk.ListStore(str)
        i = 0
        default_action=0
        for a_type in action_types:
            ls_type.append([a_type])
            if a_type == self.action_type:
                default_action = i
            i+=1

        cb_type = Gtk.ComboBox.new_with_model(ls_type)
        rt_type = Gtk.CellRendererText()
        cb_type.pack_start(rt_type, True)
        cb_type.add_attribute(rt_type, 'text', 0)
        cb_type.set_active(default_action)
        self.cb_type_changed(cb_type)
        box_action.pack_end(cb_type, False, False, 0)

        ## Plugin Box
        self.pg_plugin=self.page_plugin()
        box_t.pack_start(self.pg_plugin, False, True,0)

        ## Command Box
        self.pg_prog = self.page_prog()
        box_t.pack_start(self.pg_prog, False, True,0)
       
        

        # Buttons
        box_h = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=1)
        bu_cancel = Gtk.Button(label="Cancel")
        bu_ok    = Gtk.Button(label="Ok")
        box_h.pack_end(bu_ok, False, False, 0)
        box_h.pack_start(bu_cancel, False, False, 0)
        box_t.pack_end(box_h, False, False, 0)

        ## Control what is shown
        box_t.show_all()
        if self.action_type != "Plugin":
            self.pg_plugin.hide()
        if self.action_type != "Program":
            self.pg_prog.hide()

        ## Setup Connections
        bu_cancel.connect("clicked", self.bu_cancel_clicked)
        bu_ok.connect("clicked", self.bu_ok_clicked)
        cb_type.connect('changed', self.cb_type_changed)
        en_code.connect('changed', self.en_code_changed)

    def cb_type_changed(self, comboBox):
        cb_tree_itr = comboBox.get_active_iter()
        model = comboBox.get_model()
        self.action_type = model[cb_tree_itr][0]
        if self.action_type == "Plugin":
            try:
                self.pg_plugin.show_all()
            except:
                pass
        else:
            try:
                self.pg_plugin.hide()
            except:
                pass
        if self.action_type == "Program":
            try:
                self.pg_prog.show_all()
            except:
                pass
        else:
            try:
                self.pg_prog.hide()
            except:
                pass

    def en_code_changed(self, entry):
        self.code_type = entry.get_text()

    def page_plugin(self):
        actions=qr_process.qr_code2action()

        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=1)

        # Label
        lb_desc = Gtk.Label(label="Plugin:")
        lb_desc.set_line_wrap(False)
        box.pack_start(lb_desc, False, True, 0)

        # combobox
        input_plugins = qr_plugins.get_input_plugins()
        ls_plugin = Gtk.ListStore(str)
        i = 0
        default_value=None
        for plugin in sorted(input_plugins.keys()):
            ls_plugin.append([plugin])
            if plugin == self.plugin:
                default_value = i
            i+=1

        cb_plugin = Gtk.ComboBox.new_with_model(ls_plugin)
        rt_plugin = Gtk.CellRendererText()
        cb_plugin.pack_start(rt_plugin, True)
        cb_plugin.add_attribute(rt_plugin, 'text', 0)
        cb_plugin.connect('changed', self.cb_plugin_changed)
        if default_value != None:
            cb_plugin.set_active(default_value)
        box.pack_end(cb_plugin, False, False, 0)

        return box

    def page_prog(self):
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=1)

        # Label
        lb_desc = Gtk.Label(label="Program:")
        lb_desc.set_line_wrap(False)
        box.pack_start(lb_desc, False, True, 0)

        # Entry
        en_prog = Gtk.Entry()
        if self.prog != None:
            en_prog.set_text(self.prog)
        en_prog.connect('changed', self.en_prog_changed)
        box.pack_end(en_prog, False, False, 0)

        return box

    def en_prog_changed(self, entry):
        self.prog = entry.get_text()

    def cb_plugin_changed(self, comboBox):
        cb_tree_itr = comboBox.get_active_iter()
        model = comboBox.get_model()
        self.plugin = model[cb_tree_itr][0]
        

    def bu_ok_clicked(self, qr_code):
        if self.code_type == None or self.action_type == None:
            return
        if self.action_type == 'Program' and self.prog == None:
            return
        if self.action_type == 'Plugin' and self.plugin == None:
            return

        self.state = state=Gtk.ResponseType.OK
        self.destroy()
        
    def bu_cancel_clicked(self, qr_code):
        self.state = state=Gtk.ResponseType.CANCEL
        self.destroy()

    def get_results(self):
        results = dict()
        results['state']=self.state
        results['code_type']=self.code_type
        results['action_type']=self.action_type
        if self.action_type == "Plugin":
            results['action_subtype']=self.plugin
        elif self.action_type == "Program":
            results['action_subtype']=self.prog
        else:
            results['action_subtype']=''
        
        return results

def qr_gui_config():
    win = QRConfig()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()

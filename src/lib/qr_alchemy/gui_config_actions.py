### Gui Configuration of Actions Lib
# Allows the setting of what to do for each qr code type, and allows the 
# program to redirect system requests to this program to allow for user changes.

# This is a subset of the gui_config lib, as it just calls this to provie the 
# Actions Tab in the main config window.

import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk,Gio

import qr_alchemy.config as qr_config
import qr_alchemy.process as qr_process
import qr_alchemy.plugins as qr_plugins
import qr_alchemy.gui as gui


class QRActionConfig():
    state=Gtk.ResponseType.CANCEL
    name=""
    box = None
    def __init__(self):
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=1)

        # Page Description Pabel
        lb_desc = Gtk.Label(label="Choose what actions to perform based on what type of qr code is recieved:")
        lb_desc.set_line_wrap(True)
        self.box.pack_start(lb_desc, False, True, 0)

        # Add Button
        box_h = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=1)
        bu_add    = Gtk.Button()
        bu_add_icon = Gio.ThemedIcon(name='list-add-symbolic')
        bu_add_image = Gtk.Image.new_from_gicon(bu_add_icon, Gtk.IconSize.MENU)
        bu_add.add(bu_add_image)
        bu_add.connect("clicked", self.bu_add_clicked)
        box_h.pack_end(bu_add, False, False, 0)

        self.box.pack_start(box_h, False, False, 0)

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
        self.tv_act.set_activate_on_single_click(True)
        self.tv_act.connect("row-activated", self.bu_edit_clicked)

        # setting up the layout, putting the treeview in a scrollwindow
        stv_act = Gtk.ScrolledWindow()
        stv_act.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        stv_act.add(self.tv_act)
        self.box.pack_start(stv_act, True, True, 1)

    def ls_actions_populate(self,listStore):
        self.ls_act.clear()
        self.actions=qr_process.qr_code2action()
        self.action_keys=sorted(self.actions.keys())
        for key in self.action_keys:
            self.ls_act.append([key, ':'.join(self.actions[key])])
        
    def get_box(self):
        return self.box

    def bu_add_clicked(self, qr_code):
        entryDialog = QRConfigEntry(self,title='Add New Action')
        entryDialog.run()
        self.ls_actions_populate(self.ls_act)

    def bu_edit_clicked(self, null1, null2, null3):
        path,data = self.tv_act.get_cursor()
        if path == None:
            return
        indices = path.get_indices()
        
        code_type=self.action_keys[indices[0]]
            
        action = qr_process.qr_get_action(code_type)
        action_type = action[0]
        if len(action) > 1:
            action_subtype = action[1]
        else:
            action_subtype = ''
        system_offer=qr_config.get_offer_system(code_type)
        
        edit_dialog = QRConfigEntry(
            self,
            title='Edit Action',
            code_type=code_type, 
            action_type=action_type, 
            action_subtype=action_subtype, 
            system_offer=system_offer
        )
        edit_dialog.run()

        self.ls_actions_populate(self.ls_act)
        

class QRConfigEntry(Gtk.Dialog):
    state=Gtk.ResponseType.CANCEL
    code_type=None
    action_type=None
    plugin=None
    prog=None
    pg_plugin=None
    exists=False

    def __init__(self, parent, title, code_type=None, action_type=None, action_subtype=None, system_offer=False):
        Gtk.MessageDialog.__init__(self, title=title)

        self.code_type=code_type
        self.system_offer=system_offer
        if self.code_type != None:
            self.exists=True
        self.action_type=action_type
        if action_type == "Plugin":
            self.plugin=action_subtype
        if action_type == "Program":
            self.prog=action_subtype

        dialog = self.get_content_area()
        
        ## Main Box
        box_t = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=1)
        dialog.pack_start(box_t, True, True, 0)

        # Top Buttons
        box_h = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=1)
        bu_cancel = Gtk.Button(label="Cancel")
        bu_cancel.connect("clicked", self.bu_cancel_clicked)
        bu_delete = Gtk.Button(label="Delete")
        bu_delete.connect("clicked", self.bu_delete_clicked)
        if self.code_type == '*':
            bu_delete.set_sensitive(False)
        bu_ok    = Gtk.Button(label="Ok")
        bu_ok.connect("clicked", self.bu_ok_clicked)
        box_h.pack_end(bu_ok, False, False, 0)
        box_h.pack_start(bu_cancel, False, False, 0)
        if self.exists:
            box_h.pack_start(bu_delete, False, False, 15)
        box_t.pack_start(box_h, False, False, 0)


        ## Code Type Box
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
        en_code.connect('changed', self.en_code_changed)
        box_code_type.pack_end(en_code, False, True, 0)
        

        ## Offer To System Box
        box_system_offer = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=1)
        box_t.pack_start(box_system_offer, False, True, 0)

        # Label
        lb_system_offer = Gtk.Label(label="Offer to system:")
        lb_system_offer.set_line_wrap(False)
        box_system_offer.pack_start(lb_system_offer, False, True, 0)

        # Switch
        sw_system_offer = Gtk.Switch()
        sw_system_offer.set_active(self.system_offer)
        sw_system_offer.connect('notify::active', self.sw_system_offer_activated)
        box_system_offer.pack_end(sw_system_offer, False, True, 0)


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
        cb_type.connect('changed', self.cb_type_changed)
        self.cb_type_changed(cb_type)
        box_action.pack_end(cb_type, False, False, 0)


        ## Plugin Box
        self.pg_plugin=self.page_plugin()
        box_t.pack_start(self.pg_plugin, False, True,0)


        ## Command Box
        self.pg_prog = self.page_prog()
        box_t.pack_start(self.pg_prog, False, True,0)


        ## Control what is shown
        box_t.show_all()
        if self.action_type != "Plugin":
            self.pg_plugin.hide()
        if self.action_type != "Program":
            self.pg_prog.hide()

    def sw_system_offer_activated(self, switch, gparam):
        self.system_offer = switch.get_active()

    # cb_type_changed
    # Depending on what type the combobox switche is set to show the related 
    # things and hide the rest
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

        # Combobox
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
        # Don't let the user hit 'ok' when things are not set in a savable 
        # manner
        if self.code_type == None or self.action_type == None:
            return
        if self.action_type == 'Program' and self.prog == None:
            return
        if self.action_type == 'Plugin' and self.plugin == None:
            return

        self.state = Gtk.ResponseType.OK
        if self.action_type == "Plugin":
            subtype=self.plugin
        elif self.action_type == "Program":
            subtype=self.prog
        else:
            subtype=''
        qr_config.update_config_actionmap(self.code_type, self.action_type, subtype)
        qr_config.set_offer_system( self.code_type, self.system_offer)
        self.destroy()
        
    def bu_cancel_clicked(self, button):
        self.state = Gtk.ResponseType.CANCEL
        self.destroy()

    def bu_delete_clicked(self, button):
        if self.code_type == '*':
            return

        ok_window = gui.OkDialog(
           self,
           title="Really Delete?",
           message="Are you sure you want to delete " +self.code_type + "?\nThis will cause these to use the default action."       
        )
        ok_window.show_all()
        ok_window.run()

        qr_config.update_confog_actionmap(self.code_type, '', '')
        self.state = Gtk.ResponseType.OK
        self.destroy()

    def get_state():
        return self.state


import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk,Gio
import qr_alchemy.plugins as qr_plugins
import qr_alchemy.gui as gui
import qr_alchemy.config as qr_config


class QRPluginConfig():
    name=""
    box = None
    def __init__(self, plugin_type):
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=1)
        self.plugin_type=plugin_type

        # Label
        lb_desc = Gtk.Label(label="Add/Remove " + plugin_type + " Plugins")
        lb_desc.set_line_wrap(True)
        self.box.pack_start(lb_desc, False, True, 0)

        # Buttons
        box_h = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=1)
        bu_add    = Gtk.Button()
        bu_add_icon = Gio.ThemedIcon(name='list-add-symbolic')
        bu_add_image = Gtk.Image.new_from_gicon(bu_add_icon, Gtk.IconSize.MENU)
        bu_add.add(bu_add_image)
        bu_add.connect("clicked", self.bu_add_clicked)
        box_h.pack_end(bu_add, False, False, 0)

        self.bu_del    = Gtk.Button()
        self.bu_del.set_sensitive(False)
        bu_del_icon = Gio.ThemedIcon(name='list-remove-symbolic')
        bu_del_image = Gtk.Image.new_from_gicon(bu_del_icon, Gtk.IconSize.MENU)
        self.bu_del.add(bu_del_image)
        self.bu_del.connect("clicked", self.bu_del_clicked)
        box_h.pack_start(self.bu_del, False, False, 0)

        self.box.pack_start(box_h, False, False, 0)
        # Creating the ListStore model
        self.ls_plug = Gtk.ListStore(str)
        self.ls_plug_populate()

        self.tv_plug = Gtk.TreeView(model=self.ls_plug)
        for i, column_title in enumerate(
            ["Plugin"]
        ):

            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
            self.tv_plug.append_column(column)
            if column_title == "Action":
                column.set_resizable(True)
                column.set_max_width(50)
        self.tv_plug.connect("cursor-changed", self.tv_plug_selected)
        select = self.tv_plug.get_selection()

        # setting up the layout, putting the treeview in a scrollwindow
        stv_plug = Gtk.ScrolledWindow()
        stv_plug.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        stv_plug.add(self.tv_plug)
        self.box.pack_start(stv_plug, True, True, 1)

    def ls_plug_populate(self):
        self.ls_plug.clear()
        if self.plugin_type == 'Input':
            self.plugins=qr_plugins.get_input_plugins()
        else:
            self.plugins=qr_plugins.get_output_plugins()
            
        self.plugin_keys=sorted(self.plugins.keys())
        for key in self.plugin_keys:
            self.ls_plug.append([key])
        
    def get_box(self):
        return self.box

    def tv_plug_selected(self, user_data):
        selected = self.tv_plug.get_selection()
        data, i = selected.get_selected()
        
        if i == None:
            self.bu_del.set_sensitive(False)
            return
        
        plugin=data[i][0]
        if not plugin in self.plugins:
            self.bu_del.set_sensitive(False)
            return

        if self.plugin_type == 'Input':
            can_delete=qr_plugins.input_plugin_can_delete(plugin)
        else:
            can_delete=qr_plugins.output_plugin_can_delete(plugin)
        self.bu_del.set_sensitive(can_delete)
            

    def bu_del_clicked(self, qr_code):
        selected = self.tv_plug.get_selection()
        data, i = selected.get_selected()
        
        if i == None:
            return
            
        plugin=data[i][0]
        if plugin == '*':
            return

        ok_window = gui.OkDialog(
           self,
           title="Really Delete?",
           message="Are you sure you want to delete '" + plugin + "'?"       
        )
        ok_window.show_all()
        ok_window.run()

        state = ok_window.get_state()
        if state != Gtk.ResponseType.OK:
            return

        if self.plugin_type == 'Input':
            qr_plugins.delete_input_plugin(plugin)
        else:
            qr_plugins.delete_output_plugin(plugin)
        self.ls_plug_populate()

    def bu_add_clicked(self, qr_code):
        dialog = Gtk.FileChooserDialog(
            title="Please choose an " + self.plugin_type + " plugin to add",
            action=Gtk.FileChooserAction.OPEN
        )

        dialog.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN,
            Gtk.ResponseType.OK,
        )

        state = dialog.run()

        if state == Gtk.ResponseType.OK:
            if self.plugin_type == 'Input':
                qr_plugins.add_input_plugin(dialog.get_filename())
            else:
                qr_plugins.add_output_plugin(dialog.get_filename())
        dialog.destroy()
        self.ls_plug_populate()

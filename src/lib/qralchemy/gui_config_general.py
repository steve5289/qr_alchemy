### General Configurations Lib
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk,Gio
import qralchemy.process as qr_process
import qralchemy.plugins as qr_plugins
import qralchemy.gui as gui
import qralchemy.config as qr_config
import qralchemy.history as qr_history


class QRGeneralConfig():
    box = None
    parent=None
    def __init__(self,parent):
        self.parent=parent
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=1)
        # Label
        lb_history = Gtk.Label()
        lb_history.set_markup("<b>History</b>")
        self.box.pack_start(lb_history, False, True, 0)

        # Set History
        box_set_max_hist = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=1)
        self.box.pack_start(box_set_max_hist, False, True, 0)
        lb_desc_code = Gtk.Label(label="Max History:")
        box_set_max_hist.pack_start(lb_desc_code, False, True, 0)

        hist_options = [
            [0, 'None'],
            [10, '10'],
            [25, '25'],
            [50, '50'],
            [100, '100'],
        ]
        ls_hist_options = Gtk.ListStore(int, str)
        for hist_option in hist_options:
            ls_hist_options.append(hist_option)
        cb_max_hist = Gtk.ComboBox().new_with_model_and_entry(ls_hist_options)
        cb_max_hist.set_entry_text_column(1)
        max_hist = qr_history.get_max_hist()
        default_max_hist=1
        for i in range(len(hist_options)):
            if hist_options[i][0] == max_hist:
                default_max_hist=i
        cb_max_hist.set_active(default_max_hist)
        cb_max_hist.connect("changed", self.cb_max_hist_changed)
        box_set_max_hist.pack_end(cb_max_hist, False, True, 0)

        # Button
        bu_clear_hist = Gtk.Button(label="Clear History")
        bu_clear_hist.connect("clicked", self.bu_clear_history_clicked)
        self.box.pack_start(bu_clear_hist, False, False, 0)

    def get_box(self):
        return self.box

    def cb_max_hist_changed(self, combo):
        tree_iter = combo.get_active_iter()
        if tree_iter is not None:
            model = combo.get_model()
            max_hist=model[tree_iter][0]
            qr_history.set_max_hist(max_hist)

    def bu_clear_history_clicked(self, button):
        qr_history.clear_history()

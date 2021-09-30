
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf, Gdk, Gio

class EntryDialog(Gtk.Dialog):
    en_result = Gtk.Entry()
    state=Gtk.ResponseType.CANCEL
    name=""
    def __init__(self, parent,title,message):
        Gtk.Dialog.__init__(self, title=title)

        dialog = self.get_content_area()

        self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        self.clipboard_sel = Gtk.Clipboard.get(Gdk.SELECTION_PRIMARY)

        ## Top Box
        box_t = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=1)
        dialog.pack_start(box_t, True, True, 0)

        # Main Buttons
        bu_cancel = Gtk.Button(label="Cancel")
        bu_cancel.connect("clicked", self.bu_cancel_clicked)
        bu_ok = Gtk.Button(label="Ok")
        bu_ok.connect("clicked", self.bu_ok_clicked)

        box_b = Gtk.Box(spacing=1)
        box_t.pack_start(box_b, False, True, 0)
        box_b.pack_start(bu_cancel,  False, True, 0)
        box_b.pack_end(bu_ok, False, True, 0)

        # Label
        lb_desc = Gtk.Label(label=message)
        lb_desc.set_line_wrap(True)
        box_t.pack_start(lb_desc, False, True, 0)
    
        # Entry
        box_t.pack_start(self.en_result, False, True, 0)
        self.en_result.connect("activate", self.bu_ok_clicked)

        # Paste Buttons
        bu_paste = Gtk.Button()
        bu_paste.connect("clicked", self.bu_paste_clicked)
        bu_paste_icon = Gio.ThemedIcon(name='edit-paste-symbolic.symbolic')
        bu_paste_image = Gtk.Image.new_from_gicon(bu_paste_icon, Gtk.IconSize.MENU)
        bu_paste.add(bu_paste_image)
        bu_paste_selected = Gtk.Button()
        bu_paste_sel_icon = Gio.ThemedIcon(name='selection-end-symbolic')
        bu_paste_sel_image = Gtk.Image.new_from_gicon(bu_paste_sel_icon, Gtk.IconSize.MENU)
        bu_paste_selected.add(bu_paste_sel_image)
        bu_paste_selected.connect("clicked", self.bu_paste_selected_clicked)

        box_paste = Gtk.Box(spacing=1)
        box_t.pack_start(box_paste, False, True, 0)
        box_paste.pack_start(bu_paste,  False, True, 0)
        box_paste.pack_start(bu_paste_selected, False, True, 30)

    def bu_cancel_clicked(self, qr_code):
        self.state=Gtk.ResponseType.CANCEL
        self.destroy()
        
    def bu_ok_clicked(self, qr_code):
        if self.en_result.get_text():
            self.state=Gtk.ResponseType.OK
            self.result=self.en_result.get_text()
            self.destroy()
        
    def bu_paste_clicked(self, qr_code):
        self.en_result
        cb_text = self.clipboard.wait_for_text()
        if cb_text != None:
            text=self.en_result.get_text() + cb_text
            self.en_result.set_text(text)


    def bu_paste_selected_clicked(self, qr_code):
        self.en_result
        cb_text = self.clipboard_sel.wait_for_text()
        if cb_text != None:
            text=self.en_result.get_text() + cb_text
            self.en_result.set_text(text)

    def get_result(self):
        return self.result

    def get_state(self):
        return self.state

class OkDialog(Gtk.Dialog):
    state=Gtk.ResponseType.CANCEL
    def __init__(self, parent,title,message):
        Gtk.Dialog.__init__(self, title=title)

        dialog = self.get_content_area()

        ## Top Box
        box_t = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=1)
        dialog.pack_start(box_t, True, True, 0)

        # Buttons
        bu_cancel = Gtk.Button(label="Cancel")
        bu_cancel.connect("clicked", self.bu_cancel_clicked)
        bu_ok = Gtk.Button(label="Ok")
        bu_ok.connect("clicked", self.bu_ok_clicked)

        box_b = Gtk.Box(spacing=1)
        box_t.pack_start(box_b, False, True, 0)
        box_b.pack_start(bu_cancel,  False, True, 0)
        box_b.pack_end(bu_ok, False, True, 0)

        # Label
        lb_desc = Gtk.Label(label=message)
        lb_desc.set_line_wrap(True)
        box_t.pack_start(lb_desc, False, True, 0)
    

    def bu_cancel_clicked(self, qr_code):
        self.state=Gtk.ResponseType.CANCEL
        self.destroy()
        
    def bu_ok_clicked(self, qr_code):
        self.state=Gtk.ResponseType.OK
        self.destroy()
        
    def get_state(self):
        return self.state


# Wrote this with much help from this blogpost: 
# https://gabmus.org/posts/create_an_auto-resizing_image_widget_with_gtk3_and_python/
# Thanks GabMus!
class ResizableImage(Gtk.DrawingArea):
    def __init__(self, image_data,image_type, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pixbuf_loader = GdkPixbuf.PixbufLoader.new_with_mime_type(image_type)
        self.pixbuf_loader.write(image_data)
        self.pixbuf_loader.close()
        self.pixbuf = self.pixbuf_loader.get_pixbuf()
        self.img_surface = Gdk.cairo_surface_create_from_pixbuf(
            self.pixbuf, 1, None
        )

    def get_useful_size(self):
        allocated_width = self.get_allocated_width()
        allocated_height = self.get_allocated_height()
        if allocated_width < allocated_height:
            effective_area = allocated_width
        else:
            effective_area = allocated_height

        image_width = self.pixbuf.get_width()
        image_height = self.pixbuf.get_height()
        return effective_area/image_width * image_height

    def get_scale_factor(self):
        width_scale = self.get_allocated_width() / self.pixbuf.get_width()
        height_scale = self.get_allocated_height() / self.pixbuf.get_height()

        if width_scale < height_scale:
            return width_scale
        return height_scale

    def do_draw(self, context):
        scale_factor = self.get_scale_factor()
        context.scale(scale_factor, scale_factor)
        context.set_source_surface(self.img_surface, 0, 0)
        context.paint()
        size = self.get_useful_size()
        self.set_size_request(300, 100)

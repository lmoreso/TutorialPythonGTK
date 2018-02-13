import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


fitxer_glade = "otherwindow.glade"
main_window_name = "otherwindow"


class OtherWindowHandler:        
    bEsMainApp = True
    GtkWindow = 0
    
    def __init__(self, GtkWindow, bEsMainApp = False):        
        self.bEsMainApp = bEsMainApp
        self.GtkWindow = GtkWindow
    
    def on_opcion_no_implementada(self, widget):
        dialog = Gtk.MessageDialog(self.GtkWindow, 0, Gtk.MessageType.INFO,
                                   Gtk.ButtonsType.OK, "Probes amb PyObject (GTK 3)")
        dialog.format_secondary_text(
            "Esta opción / acción no está implementada (todavía)")
        dialog.run()
        print("on_opcion_no_implementada", widget)
        print("    INFO dialog closed")
        dialog.destroy()
     
    def on_otherwindow_delete_event(self, *args):
        if self.bEsMainApp:
            Gtk.main_quit(*args)
            return True
        
class OtherWindow:        
    def __init__(self, bEsMainApp = False, bModal = True):        
        builder = Gtk.Builder()
        builder.add_from_file(fitxer_glade)
        mainwindow = builder.get_object(main_window_name)
        builder.connect_signals(OtherWindowHandler(mainwindow, bEsMainApp))
        if not bEsMainApp and bModal: 
            mainwindow.set_modal(True)
        mainwindow.show_all()
        if bEsMainApp:
            Gtk.main()

if __name__ == "__main__":
    print("Ejecutando otraventana.py")
    OtherWindow(True)    
    print("Adiós muy buenas.")

import cairo
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import tut_gtk_bucky_robers as br

fitxer_glade = "TutorialGTK.glade"
main_window_name = "main_window"

class DialogExample(Gtk.Dialog):

    def __init__(self, parent):
        # self, title, parent, flags (MODAL prevent interaction with main window until dialog returns), buttons
        Gtk.Dialog.__init__(self, "PopUp Title", parent, Gtk.DialogFlags.MODAL,
                            ("Custom cancel text", Gtk.ResponseType.CANCEL,
                             Gtk.STOCK_OK, Gtk.ResponseType.OK))
        self.set_default_size(200, 100)
        self.set_border_width(10)

        # Content area (area above buttons)
        area = self.get_content_area()
        area.add(Gtk.Label("Wow that's so amazing, you can open a pop up."))
        self.show_all()

class MainHandler():
    gtk_main_win = None
    gtk_builder = None
    
    def __init__(self, builder, gtkwin):
        #print("MainHandler.__init__()")
        self.gtk_builder = builder
        self.gtk_main_win = gtkwin

    def on_mnu_otherwindow(self, widget):
        print("on_mnu_otherwindow")
        from otraventana import OtherWindow
        OtherWindow()
        
    def on_mnu_br_tree_view_fil(self, widget):
        print("on_mnu_br_tree_view_fil")
        br.TreeViewFilterWindow(self.gtk_main_win, False, True)     
        
    def on_mnu_br_tree_view_ord(self, widget):
        print("on_mnu_br_tree_view_fil")
        br.TreeViewFilterWindow(self.gtk_main_win, True, False)     
        
    def on_mnu_br_tree_editable(self, widget):
        print("on_mnu_br_tree_view")
        br.CellRendererTextWindow(self.gtk_main_win)     
        
    def on_mnu_br_tree_sortable(self, widget):
        print("on_mnu_br_tree_sortable")
        br.SortableTreeWindow(self.gtk_main_win)      
        
    def on_mnu_ex_cairo(self, widget):
        print("on_mnu_ex_cairo")
        from  tutorialcairo import CairoWindow
        CairoWindow()
        
    def on_mnu_about_activate(self, widget):
        dialog = Gtk.MessageDialog(self.gtk_main_win, 0, Gtk.MessageType.INFO,
                                   Gtk.ButtonsType.OK, "Probes amb PyObject (GTK 3)")
        dialog.format_secondary_text(
            "Autor: Lluis Moreso Bosch (2018)")
        dialog.run()
        print("on_mnu_about_activate", widget)
        print("    INFO dialog closed")

        dialog.destroy()
    
    def on_opcion_no_implementada(self, widget):
        dialog = Gtk.MessageDialog(self.gtk_main_win, 0, Gtk.MessageType.INFO,
                                   Gtk.ButtonsType.OK, "Probes amb PyObject (GTK 3)")
        dialog.format_secondary_text(
            "Esta opción / acción no está implementada (todavía)")
        dialog.run()
        print("on_opcion_no_implementada", widget)
        print("    INFO dialog closed")

        dialog.destroy()
    
    def mnit_ex_dialog_activate_cb(self, param):
        dialog = DialogExample(self.gtk_main_win)

        # User can't interact with main window until dialog returns something
        response = dialog.run()

        print("mnit_ex_dialog_activate_cb", param)
        if response == Gtk.ResponseType.OK:
            print("    You clicked the OK button")
        elif response == Gtk.ResponseType.CANCEL:
            print("    You clicked the CANCEL button")

        dialog.destroy()
   
    def on_main_window_hide(self, widget):
        print("on_main_window_hide")
    
    def on_main_window_delete_event(self, *args):
        print("on_main_window_delete_event")
        
        dialog = Gtk.MessageDialog(self.gtk_main_win, 0, Gtk.MessageType.QUESTION,
                                   Gtk.ButtonsType.OK_CANCEL, "Realment vols tancar l'aplicació?")
        dialog.format_secondary_text(
            "Clica 'D'Acord' per tancar l'aplicació, o, 'Cancelar' per continuar treballant-hi.")
        dialog.set_default_response(Gtk.ResponseType.OK) 
        response = dialog.run()
        dialog.destroy()
        
        if response == Gtk.ResponseType.OK:
            print("QUESTION dialog closed by clicking OK button")
            Gtk.main_quit(*args)
        else:
            print("QUESTION dialog closed by clicking CANCEL button")
            self.gtk_main_win.show()
        
        return True

           
class MainWindow:        
     def __init__(self):        

        builder = Gtk.Builder()
        builder.add_from_file(fitxer_glade)
        mainwindow = builder.get_object(main_window_name)
        builder.connect_signals(MainHandler(builder, mainwindow))
        mainwindow.show_all()
        Gtk.main()

if __name__ == "__main__":
    print("Hello World!")
    MainWindow()
    print("Adiós muy buenas.")

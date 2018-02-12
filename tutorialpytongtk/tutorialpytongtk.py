import cairo
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import random
import math
import figurasgeo
import tut_gtk_bucky_robers as br

#fitxer_glade = "TutPythonGTK_2.glade"
#cairo_window_name = "dlg_ex_cairo"
fitxer_glade = "TutorialPythonGTK.glade"
cairo_window_name = "win_ex_cairo"
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
    LstStorePunts = 0
    DrawArea = 0
    LstSelection = 0
    gtk_chk_exemplecairo = 0
    gtk_chk_show_lines = 0
    gtk_chk_show_points = 0
    gtk_main_win = 0
    gtk_builder = 0
    gtk_cairo_win = 0
    
    
    def __init__(self, builder, gtkwin, cairo_win):
        print("MainHandler.__init__()")
        self.LstStorePunts = builder.get_object("liststore2")
        self.DrawArea = builder.get_object("chart_area")
        self.LstSelection = builder.get_object("treeview1").get_selection()
        #self.LstSelection.connect("changed", self.on_tree_selection_changed)  
        self.gtk_chk_exemplecairo = builder.get_object("chk_exemplecairo")
        self.gtk_chk_show_lines = builder.get_object("chk_show_lines")
        self.gtk_chk_show_points = builder.get_object("chk_show_points")
        self.gtk_chk_exemplecairo.set_active(False)
        self.gtk_chk_show_lines.set_active(True)
        self.gtk_chk_show_points.set_active(True)
        self.gtk_main_win = gtkwin
        self.gtk_builder = builder
        self.gtk_cairo_win = cairo_win
        self.on_btn_recta(0)
        self.print_punts("".ljust(2))
        
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
        self.gtk_cairo_win.present() 
        
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
   
    def on_tree_view_reorder(self, treeviewcolumn, *user_data):        
        print("on_tree_view_reorder")
        # Forçar repintat del area
        self.DrawArea.queue_draw()
            
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

    def on_cairo_win_deleted(self, *args):
        print("on_cairo_win_deleted")
        
        dialog = Gtk.MessageDialog(self.gtk_main_win, 0, Gtk.MessageType.QUESTION,
                                   Gtk.ButtonsType.YES_NO, "Realment vols tancar l'aplicació, o només tancar aquesta Finestra?")
        dialog.format_secondary_text(
            "Clica 'Si' per tancar l'aplicació, o, 'No' per tancar aquesta Finestra i continuar treballant amb l'Aplicació principal.")
        dialog.set_default_response(Gtk.ResponseType.YES) 
        response = dialog.run()
        dialog.destroy()
        
        if response == Gtk.ResponseType.YES:
            print("QUESTION dialog closed by clicking YES button")
            Gtk.main_quit(*args)
        else:
            print("QUESTION dialog closed by clicking NO button")
            self.gtk_cairo_win.hide()

        return True
    
    def on_btn_cairo_salir(self, *args):
        Gtk.main_quit(*args)
    
    def on_btn_cairo_cerrar(self, *args):
        self.gtk_cairo_win.hide()
        return True

    def on_btn_propietats_geo(self, param):
        self.on_opcion_no_implementada(param)
        
    def on_col_x_edited(self, widget, path, text):
        self.LstStorePunts[path][0] = float(text.replace(",", "."))

    def on_col_y_edited(self, widget, path, text):
        self.LstStorePunts[path][1] = float(text.replace(",", "."))

    def on_col_desc_edited(self, widget, path, text):
        self.LstStorePunts[path][2] = text    
        
    def on_btn_recta(self, param):
        print("on_btn_recta")
        figurasgeo.Recta(self.LstStorePunts)
        self.LstSelection.select_iter(self.LstStorePunts.get_iter_first())
            
    def on_btn_bezier(self, param):
        print("on_btn_bezier")
        figurasgeo.Bezier(self.LstStorePunts)
        self.LstSelection.select_iter(self.LstStorePunts.get_iter_first())
            
    def on_btn_logaritm(self, param):
        print("on_btn_logaritm", param)
        figurasgeo.Logaritm(self.LstStorePunts, 2, 1, -8, 3)
        self.LstSelection.select_iter(self.LstStorePunts.get_iter_first())
    
    def on_btn_elipse(self, param):
        print("on_btn_elipse", param)
        figurasgeo.Elipse(self.LstStorePunts, 5, 4)
        self.LstSelection.select_iter(self.LstStorePunts.get_iter_first())
            
    def on_btn_sinus(self, param):
        print("on_btn_sinus", param)
        figurasgeo.Sinus(self.LstStorePunts, False, 5, 0.05)
        self.LstSelection.select_iter(self.LstStorePunts.get_iter_first())
        
    def on_btn_parabola(self, param):
        print("on_btn_parabola", param)
        figurasgeo.Parabola(self.LstStorePunts, 0.40, 0, -5.8, 0.25)
        self.LstSelection.select_iter(self.LstStorePunts.get_iter_first())

    def on_btn_hiperbola(self, param):
        print("on_btn_hiperbola", param)
        figurasgeo.Hiperbola(self.LstStorePunts, 1, 0)
        self.LstSelection.select_iter(self.LstStorePunts.get_iter_first())
           
    def on_cheks_changed(self, param):
        #debug
        print("on_cheks_changed")
        print("".ljust(2), param)
        print("".ljust(2), param.get_name(), ": ", param.get_active())
        print("".ljust(2), "gtk_chk_exemplecairo: ", self.gtk_chk_exemplecairo.get_active())
        print("".ljust(2), "gtk_chk_show_lines: ", self.gtk_chk_show_lines.get_active())
        print("".ljust(2), "gtk_chk_show_points: ", self.gtk_chk_show_points.get_active())
        # Forçar repintat del area
        self.DrawArea.queue_draw()
        
    
    def on_tree_selection_changed(self, param):
        print("on_tree_selection_changed")
        print("".ljust(2), param)
        model, listiter = param.get_selected()
        if listiter != None:
            print("".ljust(2), "Valores: ", model[listiter][:]) 
        # Forçar repintat del area
        self.DrawArea.queue_draw()
        
    def print_punts(self, indent):
        print(indent, "X".rjust(8), "Y".rjust(8), " Descripció")
        print(indent, "=======".rjust(8), "=======".rjust(8), " ==============")
        for index in range(len(self.LstStorePunts)):
            #print(indent, row[:])
            x = self.LstStorePunts[index][0]
            y = self.LstStorePunts[index][1]
            desc = self.LstStorePunts[index][2]
            #print(indent, str(x).rjust(8), str(y).rjust(8), desc)
            print(indent, '{0:>8.3f} {1:>8.3f}  {2}'.format(x, y, desc))
            
    def dibuixa_punts(self, da, ctx):
        #Caracteristicas globales del pincel
        ctx.set_line_width(1)
        ctx.set_tolerance(0.1)
        ctx.set_line_join(cairo.LINE_JOIN_ROUND)
        #Iniciar
        ctx.save()
        # Centrar el (0, 0)
        x = da.get_allocated_width() / 2
        y = da.get_allocated_height() / 2
        ctx.translate(x, y)
        #ctx.rotate(180)
        # Dibujo los ejes de color negro
        ctx.set_source_rgb(0, 0, 0)
        ctx.move_to(-x, 0)
        ctx.line_to(x, 0)
        ctx.move_to(0, -y)
        ctx.line_to(0, y)    
        ctx.stroke()
        #Dibuixo l'array de punts
        zoom = 30        
        # Dibuixo les linies
        if self.gtk_chk_show_lines.get_active():
            ctx.set_source_rgb(0, 1, 1)
            for index in range(len(self.LstStorePunts)):
                if index == 0:
                    ctx.move_to(self.LstStorePunts[index][0] * zoom, self.LstStorePunts[index][1] * zoom)
                else:
                    ctx.line_to(self.LstStorePunts[index][0] * zoom, self.LstStorePunts[index][1] * zoom)                
            ctx.stroke()       
        # Dibuixo els punts
        if self.gtk_chk_show_points.get_active():
            ctx.set_source_rgb(0, 0, 1)
            for index in range(len(self.LstStorePunts)):
                # Arc(cx, cy, radius, start_angle, stop_angle)
                ctx.move_to(self.LstStorePunts[index][0] * zoom, self.LstStorePunts[index][1] * zoom)
                ctx.arc(self.LstStorePunts[index][0] * zoom, self.LstStorePunts[index][1] * zoom, 1, 0, 360)
            # Dibuixo el punt seleccionat mes gran i d'un altre color
            ctx.stroke()       
            model, listiter  = self.LstSelection.get_selected()
            if listiter != None:
                ctx.move_to(model[listiter][0] * zoom, model[listiter][1] * zoom)
                ctx.arc(model[listiter][0] * zoom, model[listiter][1] * zoom, 2, 0, 360)
                ctx.set_source_rgb(1, 0, 0)
                ctx.stroke()       
        #Finalitzo
        ctx.restore()

    def cb_draw_chart(self, da = 0, ctx = 0):
        # Debug
        print("cb_draw_chart")
        indent = "".ljust(2)
        self.print_punts(indent)           
        if da != 0: 
            print(indent, "da:", da)
        if ctx != 0: 
            print(indent, "ctx:", ctx)
        if self.gtk_chk_exemplecairo.get_active():
            import exemple_cairo
            print("  Dibuixo l'exemple del Cairo")
            exemple_cairo.draw(da, ctx)
        else:
            print("  Dibuixo els punts")
            #exemple_cairo.el_meu_exemple(da, ctx)
            self.dibuixa_punts(da, ctx)
                
    def cb_btn_superior(self, b):
        print("cb_btn_superior", b)
        model, listiter  = self.LstSelection.get_selected()
        if listiter != None:
            listiter_prev = self.LstStorePunts.iter_previous(listiter)
            if listiter_prev != None:
                self.LstStorePunts.swap(listiter, listiter_prev)
                print("  Mogut: ", model[listiter][:])                      
                self.print_punts("".ljust(2))
                # Forçar repintat del area
                self.DrawArea.queue_draw()
            else:
                print("  L'element ja es al principi")
        else:
            print("  No hi ha fila seleccionada!")
    
    def cb_btn_amunt(self, b):
        print("cb_btn_amunt", b)
        model, listiter  = self.LstSelection.get_selected()
        if listiter != None:
            self.LstStorePunts.move_after(listiter)
            print("  Mogut: ", model[listiter][:])                      
            self.print_punts("".ljust(2))
            # Forçar repintat del area
            self.DrawArea.queue_draw()
        else:
            print("  No hi ha fila seleccionada!")
    
    def cb_btn_add(self, b):
        print("cb_btn_add", b)
        x = random.randrange(-50, 50, 1) / 10.0
        y = random.randrange(-50, 50, 1) / 10.0
        listiter = self.LstStorePunts.append([x, y, "afegit!"])
        print("  Afegit: ", self.LstStorePunts[listiter][:])
        self.print_punts("".ljust(2))
        self.LstSelection.select_iter(listiter)
        # Forçar repintat del area
        self.DrawArea.queue_draw()
    
    def cb_btn_delete(self, b):
        print("cb_btn_delete", b)
        model, listiter  = self.LstSelection.get_selected()
        if listiter != None:
            print("".ljust(2), "A Borrar: ", self.LstStorePunts[listiter][:])          
            self.LstStorePunts.remove(listiter)
            self.print_punts("".ljust(2))
            # Forçar repintat del area
            self.DrawArea.queue_draw()
        else:
            print("  No hi ha fila seleccionada!")
    
    def cb_btn_avall(self, b):
        print("cb_btn_avall", b)
        model, listiter  = self.LstSelection.get_selected()
        if listiter != None:
            listiter_next = self.LstStorePunts.iter_next(listiter)
            if listiter_next != None:
                self.LstStorePunts.swap(listiter, listiter_next)
                print("".ljust(2), "Mogut: ", model[listiter][:])                      
                self.print_punts("".ljust(2))
                # Forçar repintat del area
                self.DrawArea.queue_draw()
            else:
                print("  L'element ja es al final!")
        else:
            print("  No hi ha fila seleccionada!")
    
    def cb_btn_inferior(self, b):
        print("cb_btn_inferior", b)
        model, listiter  = self.LstSelection.get_selected()
        if listiter != None:
            #print(listiter.stamp, listiter.user_data, listiter.user_data2, listiter.user_data3)
            self.LstStorePunts.move_before(listiter)
            print("".ljust(2), "Mogut: ", model[listiter][:])                      
            self.print_punts("".ljust(2))
            # Forçar repintat del area
            self.DrawArea.queue_draw()
        else:
            print("  No hi ha fila seleccionada!")
           
class MainWindow:        
     def __init__(self):        

        builder = Gtk.Builder()
        builder.add_from_file(fitxer_glade)
        cairowin = builder.get_object(cairo_window_name)
        mainwindow = builder.get_object(main_window_name)
        builder.connect_signals(MainHandler(builder, mainwindow, cairowin))
        mainwindow.show_all()
        Gtk.main()

if __name__ == "__main__":
    print("Hello World!")
    MainWindow()
    print("Adiós muy buenas.")

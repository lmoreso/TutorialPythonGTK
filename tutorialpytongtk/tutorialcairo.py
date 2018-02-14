import cairo
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import figurasgeo
import random

fitxer_glade = "TutorialCairo.glade"
main_window_name = "win_ex_cairo"

class CairoWindowHandler:        
    bEsMainApp = False
    LstStorePunts = None
    DrawArea = None
    LstSelection = None
    gtk_chk_exemplecairo = None
    gtk_chk_show_lines = None
    gtk_chk_show_points = None
    gtk_builder = None
    gtk_cairo_win = None
    
    def __init__(self, gtk_cairo_win, gtk_builder, bEsMainApp = False):        
        self.bEsMainApp = bEsMainApp
        self.gtk_cairo_win = gtk_cairo_win
        self.gtk_builder = gtk_builder
        self.LstStorePunts = gtk_builder.get_object("liststore2")
        self.DrawArea = gtk_builder.get_object("chart_area")
        self.LstSelection = gtk_builder.get_object("treeview1").get_selection()
        self.gtk_chk_exemplecairo = gtk_builder.get_object("chk_exemplecairo")
        self.gtk_chk_show_lines = gtk_builder.get_object("chk_show_lines")
        self.gtk_chk_show_points = gtk_builder.get_object("chk_show_points")
        self.gtk_chk_exemplecairo.set_active(False)
        self.gtk_chk_show_lines.set_active(True)
        self.gtk_chk_show_points.set_active(True)
        self.on_btn_recta(0)
        self.print_punts("".ljust(2))     
    
    def on_cairo_win_deleted(self, *args):
        if self.bEsMainApp:
            Gtk.main_quit(*args)
        else:
            self.gtk_cairo_win.hide()

        return True

    def on_btn_cairo_salir(self, *args):
        Gtk.main_quit(*args)
    
    def on_btn_cairo_cerrar(self, *args):
        return self.on_cairo_win_deleted(*args)

    def on_btn_propietats_geo(self, param):
        dialog = Gtk.MessageDialog(self.gtk_cairo_win, 0, Gtk.MessageType.INFO,
                                   Gtk.ButtonsType.OK, "Probes amb Cairo (GTK 3)")
        dialog.format_secondary_text(
            "Esta opción / acción no está implementada (todavía)")
        dialog.run()
        dialog.destroy()
        
    def on_col_x_edited(self, widget, path, text):
        self.LstStorePunts[path][0] = float(text.replace(",", "."))

    def on_col_y_edited(self, widget, path, text):
        self.LstStorePunts[path][1] = float(text.replace(",", "."))

    def on_col_desc_edited(self, widget, path, text):
        self.LstStorePunts[path][2] = text    
        
    def elimina_orden(self):
        self.LstStorePunts.set_sort_column_id(Gtk.TREE_SORTABLE_UNSORTED_SORT_COLUMN_ID, 0)

    def on_btn_cairo_unsort(self, param):
        self.elimina_orden()
        
    def on_btn_recta(self, param):
        print("on_btn_recta")
        self.elimina_orden()
        figurasgeo.Recta(self.LstStorePunts)
        self.LstSelection.select_iter(self.LstStorePunts.get_iter_first())
            
    def on_btn_bezier(self, param):
        print("on_btn_bezier")
        self.elimina_orden()
        figurasgeo.Bezier(self.LstStorePunts)
        self.LstSelection.select_iter(self.LstStorePunts.get_iter_first())
            
    def on_btn_logaritm(self, param):
        print("on_btn_logaritm", param)
        self.elimina_orden()
        figurasgeo.Logaritm(self.LstStorePunts, 2, 1, -8, 3)
        self.LstSelection.select_iter(self.LstStorePunts.get_iter_first())
    
    def on_btn_elipse(self, param):
        print("on_btn_elipse", param)
        self.elimina_orden()
        figurasgeo.Elipse(self.LstStorePunts, 5, 4)
        self.LstSelection.select_iter(self.LstStorePunts.get_iter_first())
            
    def on_btn_sinus(self, param):
        print("on_btn_sinus", param)
        self.elimina_orden()
        figurasgeo.Sinus(self.LstStorePunts, False, 5, 0.05)
        self.LstSelection.select_iter(self.LstStorePunts.get_iter_first())
        
    def on_btn_parabola(self, param):
        print("on_btn_parabola", param)
        self.elimina_orden()
        figurasgeo.Parabola(self.LstStorePunts, 0.40, 0, -5.8, 0.25)
        self.LstSelection.select_iter(self.LstStorePunts.get_iter_first())

    def on_btn_hiperbola(self, param):
        print("on_btn_hiperbola", param)
        self.elimina_orden()
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
            self.elimina_orden()
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
            self.elimina_orden()
            self.LstStorePunts.move_after(listiter)
            print("  Mogut: ", model[listiter][:])                      
            self.print_punts("".ljust(2))
            # Forçar repintat del area
            self.DrawArea.queue_draw()
        else:
            print("  No hi ha fila seleccionada!")
    
    def cb_btn_add(self, b):
        print("cb_btn_add", b)
        self.elimina_orden()
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
            self.elimina_orden()
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
            self.elimina_orden()
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
            self.elimina_orden()
            self.LstStorePunts.move_before(listiter)
            print("".ljust(2), "Mogut: ", model[listiter][:])                      
            self.print_punts("".ljust(2))
            # Forçar repintat del area
            self.DrawArea.queue_draw()
        else:
            print("  No hi ha fila seleccionada!")

    def on_tree_view_reorder(self, treeviewcolumn, *user_data):        
        print("on_tree_view_reorder")
        # Forçar repintat del area
        self.DrawArea.queue_draw()

class CairoWindow:        
    def __init__(self, bEsMainApp = False, bModal = True):        
        builder = Gtk.Builder()
        builder.add_from_file(fitxer_glade)
        mainwindow = builder.get_object(main_window_name)
        builder.connect_signals(CairoWindowHandler(mainwindow, builder, bEsMainApp))
        if not bEsMainApp and bModal: 
            mainwindow.set_modal(True)
        mainwindow.show_all()
        if bEsMainApp:
            builder.get_object("btn_cairo_cerrar").hide()
            Gtk.main()

if __name__ == "__main__":
    print("Ejecutando tutorialcairo.py")
    CairoWindow(True)    
    print("Adiós muy buenas.")

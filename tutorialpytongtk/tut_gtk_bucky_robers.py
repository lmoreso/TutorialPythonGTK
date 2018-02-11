#!/usr/bin/env python
"""
Basado en tutorial de Bucky Robers, pero no encuentro la url de GitHub
"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# List of tuples (this is the model, aka the data that will be displayed by the TreeView)
software_list = [(False, "Firefox", 2002, "C++", True),
                 (False, "Eclipse", 2004, "Java", False),
                 (False, "Pitivi", 2004, "Python", False),
                 (False, "Netbeans", 1996, "Java", False),
                 (True, "Chrome", 2008, "C++", False),
                 (False, "Filezilla", 2001, "C++", False),
                 (False, "Bazaar", 2005, "Python", False),
                 (True, "Git", 2005, "C", False),
                 (False, "Linux Kernel", 1991, "C", False),
                 (False, "GCC", 1987, "C", False),
                 (False, "Frostwire", 2004, "Java", False)]


class TreeViewFilterWindow(Gtk.Window):
    """
    Estudio de los Tree view:
        Ejemplo principal: 
            16_tree.py.
        Añadidas funcionalidades de otros ejemplos
    """
    
    def __init__(self, parent = None, ordenable = True, filtrable = False):
        Gtk.Window.__init__(self, title="Treeview Filter Demo")
        self.set_border_width(10)
        self.set_modal(True)
        self.set_transient_for(parent)
        self.set_default_size(500, 350)

        # Set up grid
        self.grid = Gtk.Grid()
        self.grid.set_column_homogeneous(True)
        self.grid.set_row_homogeneous(True)
        self.add(self.grid)

        # Convert your data to ListStore (lists that TreeViews can display) and specify data types
        self.software_liststore = Gtk.ListStore(bool, str, int, str, bool)
        for item in software_list:
            self.software_liststore.append(list(item))
        self.current_filter_language = None

        if filtrable:
            # Creating the filter, feeding it with the liststore model
            self.language_filter = self.software_liststore.filter_new()
            # setting the filter function, note that we're not using the
            self.language_filter.set_visible_func(self.language_filter_func)

            # creating the treeview, making it use the filter as a model, and adding the columns
            self.treeview = Gtk.TreeView.new_with_model(self.language_filter)
        else:
            # Si quiero que sea ordenable, no puedo usar la lista filtrable
            self.treeview = Gtk.TreeView(self.software_liststore)

#        for i, column_title in enumerate(["Software", "Release Year", "Programming Language"]):
#            renderer = Gtk.CellRendererText()
#            column = Gtk.TreeViewColumn(column_title, renderer, text=i)
#            self.treeview.append_column(column)
            
        cellNum = 0
        renderer = Gtk.CellRendererToggle()
        column = Gtk.TreeViewColumn("Selecciona", renderer, active=cellNum)
        renderer.connect("toggled", self.on_cell_toggled)
        if ordenable: column.set_sort_column_id(cellNum) # Make column sortable and selectable
        self.treeview.append_column(column)

        cellNum += 1
        renderer = Gtk.CellRendererText()
        renderer.set_property("editable", True)
        renderer.connect("edited", self.on_soft_edited)
        column = Gtk.TreeViewColumn("Software", renderer, text=cellNum)
        if ordenable: column.set_sort_column_id(cellNum) # Make column sortable and selectable
        self.treeview.append_column(column)
        
        cellNum += 1
        renderer = Gtk.CellRendererSpin()
        renderer.set_property("editable", True)
        renderer.set_property("digits", 0)
        adjustment = Gtk.Adjustment(0, 1800, 4000, 1, 10, 0)
        renderer.set_property("adjustment", adjustment)
        renderer.connect("edited", self.on_year_edited)
        column = Gtk.TreeViewColumn("Release Year", renderer, text=cellNum)
        if ordenable: column.set_sort_column_id(cellNum) # Make column sortable and selectable
        self.treeview.append_column(column)

        cellNum += 1
        renderer = Gtk.CellRendererText()
        renderer.set_property("editable", True)
        renderer.connect("edited", self.on_text_edited)
        column = Gtk.TreeViewColumn("Programming Language", renderer, text=cellNum)
        if ordenable: column.set_sort_column_id(cellNum) # Make column sortable and selectable
        self.treeview.append_column(column)
            
        cellNum += 1
        renderer = Gtk.CellRendererToggle()
        renderer.set_radio(True)
        column = Gtk.TreeViewColumn("El Mejor", renderer, active=cellNum)
        renderer.connect("toggled", self.on_cell_radio_toggled)
        self.treeview.append_column(column)

        
        if filtrable:
            # creating buttons to filter by programming language, and setting up their events
            self.buttons = list()
            for prog_language in ["Java", "C", "C++", "Python", "None"]:
                button = Gtk.Button(prog_language)
                self.buttons.append(button)
                button.connect("clicked", self.on_selection_button_clicked)

        # setting up the layout, putting the treeview in a scrollwindow, and the buttons in a row
        self.scrollable_treelist = Gtk.ScrolledWindow()
        self.scrollable_treelist.set_vexpand(True)
        self.grid.attach(self.scrollable_treelist, 0, 0, 8, 10)
        if filtrable:
            self.grid.attach_next_to(self.buttons[0], self.scrollable_treelist, Gtk.PositionType.BOTTOM, 1, 1)
            for i, button in enumerate(self.buttons[1:]):
                self.grid.attach_next_to(button, self.buttons[i], Gtk.PositionType.RIGHT, 1, 1)
        self.scrollable_treelist.add(self.treeview)

        # Handle selection
        selected_row = self.treeview.get_selection()
        selected_row.connect("changed", self.on_item_selected)

        self.show_all()

    # User selected row
    def on_item_selected(self, selection):
        model, row = selection.get_selected()
        if row is not None:
            print("on_item_selected:", model[row][:])

    def on_text_edited(self, widget, path, text):
        self.software_liststore[path][3] = text

    def on_soft_edited(self, widget, path, text):
        self.software_liststore[path][1] = text

    def on_year_edited(self, widget, path, text):
        self.software_liststore[path][2] = int(text)

    def on_cell_toggled(self, widget, path):
        self.software_liststore[path][0] = not self.software_liststore[path][0]

    def on_cell_radio_toggled(self, widget, path):
        selected_path = Gtk.TreePath(path)
        for row in self.software_liststore:
            row[4] = (row.path == selected_path)

    def language_filter_func(self, model, iter, data):
        """Tests if the language in the row is the one in the filter"""
        if self.current_filter_language is None or self.current_filter_language == "None":
            return True
        else:
            return model[iter][3] == self.current_filter_language

    def on_selection_button_clicked(self, widget):
        """Called on any of the button clicks"""
        # we set the current language filter to the button's label
        self.current_filter_language = widget.get_label()
        print("%s language selected!" % self.current_filter_language)
        # we update the filter, which updates in turn the view
        self.language_filter.refilter()

class CellRendererTextWindow(Gtk.Window):
    """
    17_cellRendererText.py
    """
    def __init__(self, parent = None):
        Gtk.Window.__init__(self, title="CellRendererText Example")
        self.set_modal(True)
        self.set_transient_for(parent)
        self.set_default_size(200, 200)

        self.liststore = Gtk.ListStore(str, str)
        self.liststore.append(["Fedora", "http://fedoraproject.org/"])
        self.liststore.append(["Slackware", "http://www.slackware.com/"])
        self.liststore.append(["Sidux", "http://sidux.com/"])

        treeview = Gtk.TreeView(model=self.liststore)

        renderer_text = Gtk.CellRendererText()
        column_text = Gtk.TreeViewColumn("Text", renderer_text, text=0)
        treeview.append_column(column_text)

        renderer_editabletext = Gtk.CellRendererText()
        renderer_editabletext.set_property("editable", True)

        column_editabletext = Gtk.TreeViewColumn("Editable Text",
                                                 renderer_editabletext, text=1)
        treeview.append_column(column_editabletext)

        renderer_editabletext.connect("edited", self.text_edited)

        self.add(treeview)
        self.show_all()

    def text_edited(self, widget, path, text):
        self.liststore[path][1] = text

class SortableTreeWindow(Gtk.Window):
    """
    28_treeViewSort.py
    """
    # List of tuples (this is the model, aka the data that will be displayed by the TreeView)
    people = [("Bucky Roberts", 67, "Exotic Dancer"),
              ("Jenny Blue", 21, "Shepherd"),
              ("John Smith", 55, "Programmer"),
              ("Emma Anderson", 43, "Nurse"),
              ("Emily Wilson", 28, "Teacher")]

    def __init__(self, parent = None):
        Gtk.Window.__init__(self, title="People Finder")
        self.set_modal(True)
        self.set_transient_for(parent)

        layout = Gtk.Box()
        self.add(layout)

        people_list_store = Gtk.ListStore(str, int, str)

        for item in self.people:
            people_list_store.append(list(item))

        people_tree_view = Gtk.TreeView(people_list_store)

        for i, col_title in enumerate(["Name", "Age", "Profession"]):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(col_title, renderer, text=i)

            # Make column sortable and selectable
            column.set_sort_column_id(i)

            people_tree_view.append_column(column)

        # Handle selection
        selected_row = people_tree_view.get_selection()
        selected_row.connect("changed", self.item_selected)

        layout.pack_start(people_tree_view, True, True, 0)

        self.show_all()

    # User selected row
    def item_selected(self, selection):
        model, row = selection.get_selected()
        if row is not None:
            print("Name: ", model[row][0])
            print("Age: ", model[row][1])
            print("Job: ", model[row][2])
            print("")


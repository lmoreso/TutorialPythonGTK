#!/usr/bin/env python
"""
Basado en tutorial de Bucky Robers, pero no encuentro la url de GitHub
"""

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, GObject, Gdk, GdkPixbuf

class LabelWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Label Example")
        self.set_border_width(20)
        self.set_default_size(500, 300)

        # set_homogeneous() - if True, all children get equal space
        hbox = Gtk.Box(spacing=20)
        hbox.set_homogeneous(False)
        vbox_left = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        vbox_left.set_homogeneous(False)
        vbox_right = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=20)
        vbox_right.set_homogeneous(False)

        # Make two columns
        hbox.pack_start(vbox_left, True, True, 0)
        hbox.pack_start(vbox_right, True, True, 0)

        # Normal
        label = Gtk.Label("This is a normal label")
        vbox_left.pack_start(label, True, True, 0)

        # Left justified
        label = Gtk.Label()
        label.set_text("This is a left-justified label.\nWith multiple lines.")
        label.set_justify(Gtk.Justification.LEFT)
        vbox_left.pack_start(label, True, True, 0)

        # Right justified
        label = Gtk.Label("This is a right-justified label.\nWith multiple lines.")
        label.set_justify(Gtk.Justification.RIGHT)
        vbox_left.pack_start(label, True, True, 0)

        # Line wrap
        label = Gtk.Label("This is a Text-wrapped label. Drumstick biltong chuck, tongue porchetta jerky jowl bacon pig kevin. Tail shankle cupim.")
        label.set_line_wrap(True)
        vbox_right.pack_start(label, True, True, 0)

        # Fill (newspaper)
        label = Gtk.Label("This is a Text-wrapped FILL-justified label. Drumstick biltong chuck, tongue porchetta jerky jowl bacon pig kevin. Tail shankle.")
        label.set_line_wrap(True)
        label.set_justify(Gtk.Justification.FILL)
        vbox_right.pack_start(label, True, True, 0)

        # Markup\n\n
        label = Gtk.Label()
        label.set_markup("This is a HTML label:"
                         "<small>small</small>\n "
                         "<big>big</big>\n"
                         "<b>bold</b>\n"
                         "<i>italic</i>\n"
                         "<a href=\"https://www.thenewboston.com\" title=\"Will appear on hover\">Learn Stuff</a>")
        label.set_line_wrap(True)
        vbox_right.pack_start(label, True, True, 0)
        
        #texte inclinat
        label = Gtk.Label()
        label.set_text("Text inclinat 30 graus\ni alineat Gtk.Align.END.")
        label.set_angle(30)
        label.set_halign(Gtk.Align.END)
        vbox_left.pack_start(label, True, True, 0)
    

        self.add(hbox)

        

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


def TreeViewFilterWindow(parent = None):
    return TreeViewOrderWindow(parent, False, True)
    
class TreeViewOrderWindow(Gtk.Window):
    """
    Estudio de los Tree view:
        Ejemplo principal: 
            16_tree.py.
        Añadidas funcionalidades de otros ejemplos
    """
    
    def __init__(self, parent = None, ordenable = True, filtrable = False):
        sTitulo = "Treeview Filter Demo"
        if ordenable: sTitulo = "Treeview Order Demo"
        
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

        

    # User selected row
    def item_selected(self, selection):
        model, row = selection.get_selected()
        if row is not None:
            print("Name: ", model[row][0])
            print("Age: ", model[row][1])
            print("Job: ", model[row][2])
            print("")

# ListBox is just a vertical container that you can sort, navigate with the keyboard, etc...
class ListBoxWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Cheeseburger Machine")
        self.set_border_width(10)
        listbox = Gtk.ListBox()
        listbox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.add(listbox)

        # Inside your ListBox are ListBoxRows (widgets go inside them)
        row_1 = Gtk.ListBoxRow()
        box_1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=100)
        row_1.add(box_1)
        label = Gtk.Label("Check if you love cheeseburgers:")
        check = Gtk.CheckButton()
        box_1.pack_start(label, True, True, 0)
        box_1.pack_start(check, True, True, 0)
        listbox.add(row_1)

        # Toggle switch
        row_2 = Gtk.ListBoxRow()
        box_2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=100)
        row_2.add(box_2)
        label = Gtk.Label("Burger making machine:")
        switch = Gtk.Switch()
        switch.props.valign = Gtk.Align.CENTER
        box_2.pack_start(label, True, True, 0)
        box_2.pack_start(switch, True, True, 0)
        listbox.add(row_2)
        
        

class StackWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Switcher")
        self.set_border_width(10)
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(box)

        # Stack - container that shows one item at a time
        main_area = Gtk.Stack()
        main_area.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        main_area.set_transition_duration(2000)

        # Check box
        check_button = Gtk.CheckButton("Do not fn check me")
        main_area.add_titled(check_button, "checkbox_name", "Check Box")

        # Label
        label = Gtk.Label()
        label.set_markup("<big>OMG this text is huge!</big>")
        main_area.add_titled(label, "label_big", "Big Label")

        # Label
        label = Gtk.Label()
        label.set_markup("<small>OMG this text is small!</small>")
        main_area.add_titled(label, "label_small", "Small label")

        # StackSwitcher - controller for the stack (row of buttons you can click to change items)
        stack_switcher = Gtk.StackSwitcher()
        stack_switcher.set_stack(main_area)
        box.pack_start(stack_switcher, True, True, 0)
        box.pack_start(main_area, True, True, 0)

        

class HeaderBarWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="")
        self.set_border_width(10)
        self.set_default_size(500, 400)

        header_bar = Gtk.HeaderBar()
        header_bar.set_show_close_button(True)
        header_bar.props.title = "Rippin Music Player"
        self.set_titlebar(header_bar)

        # Audio button on right
        audio_button = Gtk.Button()
        cd_icon = Gio.ThemedIcon(name="gnome-dev-cdrom-audio")
        image = Gtk.Image.new_from_gicon(cd_icon, Gtk.IconSize.BUTTON)
        audio_button.add(image)
        header_bar.pack_end(audio_button)

        # Create a box and link items together
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        Gtk.StyleContext.add_class(box.get_style_context(), "linked")

        # Left arrow
        left_arrow = Gtk.Button()
        left_arrow.add(Gtk.Arrow(Gtk.ArrowType.LEFT, Gtk.ShadowType.NONE))
        box.add(left_arrow)

        # Right arrow
        right_arrow = Gtk.Button()
        right_arrow.add(Gtk.Arrow(Gtk.ArrowType.RIGHT, Gtk.ShadowType.NONE))
        box.add(right_arrow)

        header_bar.pack_start(box)
        self.add(Gtk.TextView())

        

class NoteBook(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Notebook Demo")
        self.set_border_width(10)
        self.notebook = Gtk.Notebook()
        self.add(self.notebook)

        # First regular tab
        self.page1 = Gtk.Box()
        self.page1.set_border_width(10)
        self.page1.add(Gtk.Label('Here is the content of the first section.'))
        self.notebook.append_page(self.page1, Gtk.Label('First Tab'))

        # Second star icon tab
        self.page2 = Gtk.Box()
        self.page2.set_border_width(10)
        self.page2.add(Gtk.Label('This is what you will see when you click the star.'))
        icon = Gtk.Image.new_from_icon_name("gnome-dev-cdrom-audio", Gtk.IconSize.MENU)
        self.notebook.append_page(self.page2, icon)

        # Last regular tab
        self.page1 = Gtk.Box()
        self.page1.set_border_width(10)
        self.page1.add(Gtk.Label('Here is the content of the last section.'))
        self.notebook.append_page(self.page1, Gtk.Label('Last Tab'))        

class UserInput(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Messenger 2.0")
        self.set_border_width(10)
        self.set_size_request(200, 100)

        # Layout
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        # Username
        self.username = Gtk.Entry()
        self.username.set_text("Username")
        vbox.pack_start(self.username, True, True, 0)

        # Password
        self.password = Gtk.Entry()
        self.password.set_text("Password")
        self.password.set_visibility(False)
        vbox.pack_start(self.password, True, True, 0)

        # Sign In Button
        self.button = Gtk.Button(label="Sign In")
        self.button.connect("clicked", self.sign_in)
        vbox.pack_start(self.button, True, True, 0)
        
        

    def sign_in(self, widget):
        print(self.username.get_text())
        print(self.password.get_text())

class ToggleButtonWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="ToggleButton")
        self.set_border_width(10)
        hbox = Gtk.Box(spacing=6)
        self.add(hbox)

        button = Gtk.ToggleButton("Button 1")
        button.connect("toggled", self.on_button_toggled, "1")
        hbox.pack_start(button, True, True, 0)

        button = Gtk.ToggleButton("Button 2", use_underline=True)
        button.set_active(True)
        button.connect("toggled", self.on_button_toggled, "2")
        hbox.pack_start(button, True, True, 0)

        

    def on_button_toggled(self, button, name):
        if button.get_active():
            state = "on"
        else:
            state = "off"
        print("Button", name, "was turned", state)

class SpinButtonWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="SpinButton Demo")
        self.set_border_width(10)

        hbox = Gtk.Box(spacing=6)
        self.add(hbox)

        adjustment = Gtk.Adjustment(0, 0, 100, 1, 10, 0)
        self.spinbutton = Gtk.SpinButton()
        self.spinbutton.set_adjustment(adjustment)
        hbox.pack_start(self.spinbutton, False, False, 0)

        check_numeric = Gtk.CheckButton("Numeric")
        check_numeric.connect("toggled", self.on_numeric_toggled)
        hbox.pack_start(check_numeric, False, False, 0)

        check_ifvalid = Gtk.CheckButton("If Valid")
        check_ifvalid.connect("toggled", self.on_ifvalid_toggled)
        hbox.pack_start(check_ifvalid, False, False, 0)


    def on_numeric_toggled(self, button):
        self.spinbutton.set_numeric(button.get_active())

    def on_ifvalid_toggled(self, button):
        if button.get_active():
            policy = Gtk.SpinButtonUpdatePolicy.IF_VALID
        else:
            policy = Gtk.SpinButtonUpdatePolicy.ALWAYS
        self.spinbutton.set_update_policy(policy)

class RadioButtonWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="RadioButton Demo")
        self.set_border_width(10)

        hbox = Gtk.Box(spacing=6)
        self.add(hbox)

        button1 = Gtk.RadioButton.new_with_label_from_widget(None, "Button 1")
        button1.connect("toggled", self.on_button_toggled, "1")
        hbox.pack_start(button1, False, False, 0)

        button2 = Gtk.RadioButton.new_from_widget(button1)
        button2.set_label("Button 2")
        button2.connect("toggled", self.on_button_toggled, "2")
        hbox.pack_start(button2, False, False, 0)

        button3 = Gtk.RadioButton.new_with_mnemonic_from_widget(button1, "Button 3")
        button3.connect("toggled", self.on_button_toggled, "3")
        hbox.pack_start(button3, False, False, 0)

        

    def on_button_toggled(self, button, name):
        if button.get_active():
            state = "on"
        else:
            state = "off"
        print("Button", name, "was turned", state)

class ComboBoxWindow(Gtk.Window):
    """
    https://python-gtk-3-tutorial.readthedocs.io/en/latest/combobox.html
    """

    def __init__(self):
        Gtk.Window.__init__(self, title="ComboBox Example")

        self.set_border_width(10)

        name_store = Gtk.ListStore(int, str)
        name_store.append([1, "Billy Bob"])
        name_store.append([11, "Billy Bob Junior"])
        name_store.append([12, "Sue Bob"])
        name_store.append([2, "Joey Jojo"])
        name_store.append([3, "Rob McRoberts"])
        name_store.append([31, "Xavier McRoberts"])

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)

        name_combo = Gtk.ComboBox.new_with_model_and_entry(name_store)
        name_combo.connect("changed", self.on_name_combo_changed)
        name_combo.set_entry_text_column(1)
        vbox.pack_start(name_combo, False, False, 0)

        country_store = Gtk.ListStore(str)
        countries = ["Austria", "Brazil", "Belgium", "France", "Germany",
            "Switzerland", "United Kingdom", "United States of America",
            "Uruguay"]
        for country in countries:
            country_store.append([country])

        country_combo = Gtk.ComboBox.new_with_model(country_store)
        country_combo.connect("changed", self.on_country_combo_changed)
        renderer_text = Gtk.CellRendererText()
        country_combo.pack_start(renderer_text, True)
        country_combo.add_attribute(renderer_text, "text", 0)
        vbox.pack_start(country_combo, False, False, True)

        currencies = ["Euro", "US Dollars", "British Pound", "Japanese Yen",
            "Russian Ruble", "Mexican peso", "Swiss franc"]
        currency_combo = Gtk.ComboBoxText()
        currency_combo.set_entry_text_column(0)
        currency_combo.connect("changed", self.on_currency_combo_changed)
        for currency in currencies:
            currency_combo.append_text(currency)

        vbox.pack_start(currency_combo, False, False, 0)

        self.add(vbox)
       
    def on_name_combo_changed(self, combo):
        tree_iter = combo.get_active_iter()
        if tree_iter is not None:
            model = combo.get_model()
            row_id, name = model[tree_iter][:2]
            print("Selected: ID=%d, name=%s" % (row_id, name))
        else:
            entry = combo.get_child()
            print("Entered: %s" % entry.get_text())

    def on_country_combo_changed(self, combo):
        tree_iter = combo.get_active_iter()
        if tree_iter is not None:
            model = combo.get_model()
            country = model[tree_iter][0]
            print("Selected: country=%s" % country)

    def on_currency_combo_changed(self, combo):
        text = combo.get_active_text()
        if text is not None:
            print("Selected: currency=%s" % text)

class ProgressBarWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="ProgressBar Demo")
        self.set_border_width(10)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        self.progressbar = Gtk.ProgressBar()
        vbox.pack_start(self.progressbar, True, True, 0)

        button = Gtk.CheckButton("Show text")
        button.connect("toggled", self.on_show_text_toggled)
        vbox.pack_start(button, True, True, 0)

        button = Gtk.CheckButton("Activity mode")
        button.connect("toggled", self.on_activity_mode_toggled)
        vbox.pack_start(button, True, True, 0)

        button = Gtk.CheckButton("Right to Left")
        button.connect("toggled", self.on_right_to_left_toggled)
        vbox.pack_start(button, True, True, 0)

        self.timeout_id = GObject.timeout_add(5, self.on_timeout, None)
        self.activity_mode = False

    def on_show_text_toggled(self, button):
        show_text = button.get_active()
#        if show_text:
#            text = "some text"
#        else:
#            text = None
#        self.progressbar.set_text(text)
        self.progressbar.set_show_text(show_text)

    def on_activity_mode_toggled(self, button):
        self.activity_mode = button.get_active()
        if self.activity_mode:
            self.progressbar.pulse()
        else:
            self.progressbar.set_fraction(0.0)

    def on_right_to_left_toggled(self, button):
        value = button.get_active()
        self.progressbar.set_inverted(value)

    def on_timeout(self, user_data):
        """
        Update value on the progress bar
        """
        if self.activity_mode:
            self.progressbar.pulse()
        else:
            new_value = self.progressbar.get_fraction() + 0.001

            if new_value > 1:
                new_value = 0

            self.progressbar.set_fraction(new_value)
            self.progressbar.set_text("{0:=5.1f}%".format(new_value * 100))

        # As this is a timeout function, return True so that it
        # continues to get called
        return True

class CellRendererPixbufWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="CellRendererPixbuf Example")
        self.set_default_size(200, 200)

        self.liststore = Gtk.ListStore(str, str)
        self.liststore.append(["New", "document-new"])
        self.liststore.append(["Open", "document-open"])
        self.liststore.append(["Save", "document-save"])

        treeview = Gtk.TreeView(model=self.liststore)

        renderer_text = Gtk.CellRendererText()
        column_text = Gtk.TreeViewColumn("Text", renderer_text, text=0)
        treeview.append_column(column_text)

        renderer_pixbuf = Gtk.CellRendererPixbuf()

        column_pixbuf = Gtk.TreeViewColumn("Image", renderer_pixbuf, icon_name=1)
        treeview.append_column(column_pixbuf)

        self.add(treeview)

class CellRendererToggleWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="CellRendererToggle Example")

        self.set_default_size(200, 200)

        self.liststore = Gtk.ListStore(str, bool, bool)
        self.liststore.append(["Debian", False, True])
        self.liststore.append(["OpenSuse", True, False])
        self.liststore.append(["Fedora", False, False])

        treeview = Gtk.TreeView(model=self.liststore)

        renderer_text = Gtk.CellRendererText()
        column_text = Gtk.TreeViewColumn("Text", renderer_text, text=0)
        treeview.append_column(column_text)

        renderer_toggle = Gtk.CellRendererToggle()
        renderer_toggle.connect("toggled", self.on_cell_toggled)

        column_toggle = Gtk.TreeViewColumn("Toggle", renderer_toggle, active=1)
        treeview.append_column(column_toggle)

        renderer_radio = Gtk.CellRendererToggle()
        renderer_radio.set_radio(True)
        renderer_radio.connect("toggled", self.on_cell_radio_toggled)

        column_radio = Gtk.TreeViewColumn("Radio", renderer_radio, active=2)
        treeview.append_column(column_radio)

        self.add(treeview)

    def on_cell_toggled(self, widget, path):
        self.liststore[path][1] = not self.liststore[path][1]

    def on_cell_radio_toggled(self, widget, path):
        selected_path = Gtk.TreePath(path)
        for row in self.liststore:
            row[2] = (row.path == selected_path)

class CellRendererProgressWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="CellRendererProgress Example")

        self.set_default_size(200, 200)

        self.liststore = Gtk.ListStore(str, int, bool)
        self.current_iter = self.liststore.append(["Sabayon", 0, False])
        self.liststore.append(["Zenwalk", 0, False])
        self.liststore.append(["SimplyMepis", 0, False])

        treeview = Gtk.TreeView(model=self.liststore)

        renderer_text = Gtk.CellRendererText()
        column_text = Gtk.TreeViewColumn("Text", renderer_text, text=0)
        treeview.append_column(column_text)

        renderer_progress = Gtk.CellRendererProgress()
        column_progress = Gtk.TreeViewColumn("Progress", renderer_progress,
                                             value=1, inverted=2)
        treeview.append_column(column_progress)

        renderer_toggle = Gtk.CellRendererToggle()
        renderer_toggle.connect("toggled", self.on_inverted_toggled)
        column_toggle = Gtk.TreeViewColumn("Inverted", renderer_toggle,
                                           active=2)
        treeview.append_column(column_toggle)

        self.add(treeview)

        self.timeout_id = GObject.timeout_add(100, self.on_timeout, None)

    def on_inverted_toggled(self, widget, path):
        self.liststore[path][2] = not self.liststore[path][2]

    def on_timeout(self, user_data):
        new_value = self.liststore[self.current_iter][1] + 1
        if new_value > 100:
            self.current_iter = self.liststore.iter_next(self.current_iter)
            if self.current_iter == None:
                self.reset_model()
            new_value = self.liststore[self.current_iter][1] + 1

        self.liststore[self.current_iter][1] = new_value
        return True

    def reset_model(self):
        for row in self.liststore:
            row[1] = 0
        self.current_iter = self.liststore.get_iter_first()

class FileChooserWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="")
        self.set_border_width(30)
        layout = Gtk.Box(spacing=6)
        self.add(layout)

        button = Gtk.Button("Choose File")
        button.connect("clicked", self.on_file_clicked)
        layout.add(button)

    # User clicked open file button
    def on_file_clicked(self, widget):

        # Gtk.FileChooserAction.SELECT_FOLDER
        dialog = Gtk.FileChooserDialog("Select a file Hoss", self, Gtk.FileChooserAction.OPEN,
                                       (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            print("Open button clicked")
            print("File selected: " + dialog.get_filename())
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel button clicked")

        dialog.destroy()

class MessageDialogWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="MessageDialog Example")

        box = Gtk.Box(spacing=6)
        self.add(box)

        button1 = Gtk.Button("Information")
        button1.connect("clicked", self.on_info_clicked)
        box.add(button1)

        button2 = Gtk.Button("Error")
        button2.connect("clicked", self.on_error_clicked)
        box.add(button2)

        button3 = Gtk.Button("Warning")
        button3.connect("clicked", self.on_warn_clicked)
        box.add(button3)

        button4 = Gtk.Button("Question")
        button4.connect("clicked", self.on_question_clicked)
        box.add(button4)

    def on_info_clicked(self, widget):
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO,
                                   Gtk.ButtonsType.OK, "This is an INFO MessageDialog")
        dialog.format_secondary_text(
            "And this is the secondary text that explains things.")
        dialog.run()
        print("INFO dialog closed")

        dialog.destroy()

    def on_error_clicked(self, widget):
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR,
                                   Gtk.ButtonsType.CANCEL, "This is an ERROR MessageDialog")
        dialog.format_secondary_text(
            "And this is the secondary text that explains things.")
        dialog.run()
        print("ERROR dialog closed")

        dialog.destroy()

    def on_warn_clicked(self, widget):
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING,
                                   Gtk.ButtonsType.OK_CANCEL, "This is an WARNING MessageDialog")
        dialog.format_secondary_text(
            "And this is the secondary text that explains things.")
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("WARN dialog closed by clicking OK button")
        elif response == Gtk.ResponseType.CANCEL:
            print("WARN dialog closed by clicking CANCEL button")

        dialog.destroy()

    def on_question_clicked(self, widget):
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.QUESTION,
                                   Gtk.ButtonsType.YES_NO, "This is an QUESTION MessageDialog")
        dialog.format_secondary_text(
            "And this is the secondary text that explains things.")
        response = dialog.run()
        if response == Gtk.ResponseType.YES:
            print("QUESTION dialog closed by clicking YES button")
        elif response == Gtk.ResponseType.NO:
            print("QUESTION dialog closed by clicking NO button")

        dialog.destroy()

class CustomDialog(Gtk.Dialog):

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

class CustomDialogWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Dialog Example")
        self.set_default_size(200, 100)
        self.set_border_width(30)

        button = Gtk.Button("Open a PopUp")
        button.connect("clicked", self.button_clicked)
        self.add(button)

    def button_clicked(self, widget):
        dialog = CustomDialog(self)

        # User can't interact with main window until dialog returns something
        response = dialog.run()

        if response == Gtk.ResponseType.OK:
            print("You clicked the OK button")
        elif response == Gtk.ResponseType.CANCEL:
            print("You clicked the CANCEL button")

        dialog.destroy()

class SearchDialog(Gtk.Dialog):

    def __init__(self, parent):
        Gtk.Dialog.__init__(self, "Search", parent,
                            Gtk.DialogFlags.MODAL, buttons=(
                Gtk.STOCK_FIND, Gtk.ResponseType.OK,
                Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL))

        box = self.get_content_area()

        label = Gtk.Label("Insert text you want to search for:")
        box.add(label)

        self.entry = Gtk.Entry()
        box.add(self.entry)

        self.show_all()


class TextEditWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="TextView Example")

        self.set_default_size(-1, 350)

        self.grid = Gtk.Grid()
        self.add(self.grid)

        self.create_textview()
        self.create_toolbar()
        self.create_buttons()

    def create_toolbar(self):
        toolbar = Gtk.Toolbar()
        self.grid.attach(toolbar, 0, 0, 3, 1)

        button_bold = Gtk.ToolButton()
        button_bold.set_icon_name("format-text-bold-symbolic")
        toolbar.insert(button_bold, 0)

        button_italic = Gtk.ToolButton()
        button_italic.set_icon_name("format-text-italic-symbolic")
        toolbar.insert(button_italic, 1)

        button_underline = Gtk.ToolButton()
        button_underline.set_icon_name("format-text-underline-symbolic")
        toolbar.insert(button_underline, 2)

        button_bold.connect("clicked", self.on_button_clicked, self.tag_bold)
        button_italic.connect("clicked", self.on_button_clicked,
                              self.tag_italic)
        button_underline.connect("clicked", self.on_button_clicked,
                                 self.tag_underline)

        toolbar.insert(Gtk.SeparatorToolItem(), 3)

        radio_justifyleft = Gtk.RadioToolButton()
        radio_justifyleft.set_icon_name("format-justify-left-symbolic")
        toolbar.insert(radio_justifyleft, 4)

        radio_justifycenter = Gtk.RadioToolButton.new_from_widget(radio_justifyleft)
        radio_justifycenter.set_icon_name("format-justify-center-symbolic")
        toolbar.insert(radio_justifycenter, 5)

        radio_justifyright = Gtk.RadioToolButton.new_from_widget(radio_justifyleft)
        radio_justifyright.set_icon_name("format-justify-right-symbolic")
        toolbar.insert(radio_justifyright, 6)

        radio_justifyfill = Gtk.RadioToolButton.new_from_widget(radio_justifyleft)
        radio_justifyfill.set_icon_name("format-justify-fill-symbolic")
        toolbar.insert(radio_justifyfill, 7)

        radio_justifyleft.connect("toggled", self.on_justify_toggled,
                                  Gtk.Justification.LEFT)
        radio_justifycenter.connect("toggled", self.on_justify_toggled,
                                    Gtk.Justification.CENTER)
        radio_justifyright.connect("toggled", self.on_justify_toggled,
                                   Gtk.Justification.RIGHT)
        radio_justifyfill.connect("toggled", self.on_justify_toggled,
                                  Gtk.Justification.FILL)

        toolbar.insert(Gtk.SeparatorToolItem(), 8)

        button_clear = Gtk.ToolButton()
        button_clear.set_icon_name("edit-clear-symbolic")
        button_clear.connect("clicked", self.on_clear_clicked)
        toolbar.insert(button_clear, 9)

        toolbar.insert(Gtk.SeparatorToolItem(), 10)

        button_search = Gtk.ToolButton()
        button_search.set_icon_name("system-search-symbolic")
        button_search.connect("clicked", self.on_search_clicked)
        toolbar.insert(button_search, 11)

    def create_textview(self):
        scrolledwindow = Gtk.ScrolledWindow()
        scrolledwindow.set_hexpand(True)
        scrolledwindow.set_vexpand(True)
        self.grid.attach(scrolledwindow, 0, 1, 3, 1)

        self.textview = Gtk.TextView()
        self.textbuffer = self.textview.get_buffer()
        self.textbuffer.set_text("This is some text inside of a Gtk.TextView. "
                                 + "Select text and click one of the buttons 'bold', 'italic', "
                                 + "or 'underline' to modify the text accordingly.")
        scrolledwindow.add(self.textview)

        self.tag_bold = self.textbuffer.create_tag("bold",
                                                   weight=Pango.Weight.BOLD)
        self.tag_italic = self.textbuffer.create_tag("italic",
                                                     style=Pango.Style.ITALIC)
        self.tag_underline = self.textbuffer.create_tag("underline",
                                                        underline=Pango.Underline.SINGLE)
        self.tag_found = self.textbuffer.create_tag("found",
                                                    background="yellow")

    def create_buttons(self):
        check_editable = Gtk.CheckButton("Editable")
        check_editable.set_active(True)
        check_editable.connect("toggled", self.on_editable_toggled)
        self.grid.attach(check_editable, 0, 2, 1, 1)

        check_cursor = Gtk.CheckButton("Cursor Visible")
        check_cursor.set_active(True)
        check_editable.connect("toggled", self.on_cursor_toggled)
        self.grid.attach_next_to(check_cursor, check_editable,
                                 Gtk.PositionType.RIGHT, 1, 1)

        radio_wrapnone = Gtk.RadioButton.new_with_label_from_widget(None,
                                                                    "No Wrapping")
        self.grid.attach(radio_wrapnone, 0, 3, 1, 1)

        radio_wrapchar = Gtk.RadioButton.new_with_label_from_widget(
            radio_wrapnone, "Character Wrapping")
        self.grid.attach_next_to(radio_wrapchar, radio_wrapnone,
                                 Gtk.PositionType.RIGHT, 1, 1)

        radio_wrapword = Gtk.RadioButton.new_with_label_from_widget(
            radio_wrapnone, "Word Wrapping")
        self.grid.attach_next_to(radio_wrapword, radio_wrapchar,
                                 Gtk.PositionType.RIGHT, 1, 1)

        radio_wrapnone.connect("toggled", self.on_wrap_toggled,
                               Gtk.WrapMode.NONE)
        radio_wrapchar.connect("toggled", self.on_wrap_toggled,
                               Gtk.WrapMode.CHAR)
        radio_wrapword.connect("toggled", self.on_wrap_toggled,
                               Gtk.WrapMode.WORD)

    def on_button_clicked(self, widget, tag):
        bounds = self.textbuffer.get_selection_bounds()
        if len(bounds) != 0:
            start, end = bounds
            self.textbuffer.apply_tag(tag, start, end)

    def on_clear_clicked(self, widget):
        start = self.textbuffer.get_start_iter()
        end = self.textbuffer.get_end_iter()
        self.textbuffer.remove_all_tags(start, end)

    def on_editable_toggled(self, widget):
        self.textview.set_editable(widget.get_active())

    def on_cursor_toggled(self, widget):
        self.textview.set_cursor_visible(widget.get_active())

    def on_wrap_toggled(self, widget, mode):
        self.textview.set_wrap_mode(mode)

    def on_justify_toggled(self, widget, justification):
        self.textview.set_justification(justification)

    def on_search_clicked(self, widget):
        dialog = SearchDialog(self)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            cursor_mark = self.textbuffer.get_insert()
            start = self.textbuffer.get_iter_at_mark(cursor_mark)
            if start.get_offset() == self.textbuffer.get_char_count():
                start = self.textbuffer.get_start_iter()

            self.search_and_mark(dialog.entry.get_text(), start)

        dialog.destroy()

    def search_and_mark(self, text, start):
        end = self.textbuffer.get_end_iter()
        match = start.forward_search(text, 0, end)

        if match != None:
            match_start, match_end = match
            self.textbuffer.apply_tag(self.tag_found, match_start, match_end)
            self.search_and_mark(text, match_end)

icons = ["edit-cut", "edit-paste", "edit-copy"]


class IconViewWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self)
        self.set_default_size(200, 200)

        liststore = Gtk.ListStore(GdkPixbuf.Pixbuf, str)
        iconview = Gtk.IconView.new()
        iconview.set_model(liststore)
        iconview.set_pixbuf_column(0)
        iconview.set_text_column(1)

        for icon in icons:
            pixbuf = Gtk.IconTheme.get_default().load_icon(icon, 64, 0)
            liststore.append([pixbuf, "Label"])

        self.add(iconview)

class ClipboardWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Clipboard Example")

        table = Gtk.Table(3, 2)

        self.clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        self.entry = Gtk.Entry()
        self.image = Gtk.Image.new_from_icon_name("process-stop", Gtk.IconSize.MENU)

        button_copy_text = Gtk.Button("Copy Text")
        button_paste_text = Gtk.Button("Paste Text")
        button_copy_image = Gtk.Button("Copy Image")
        button_paste_image = Gtk.Button("Paste Image")

        table.attach(self.entry, 0, 1, 0, 1)
        table.attach(self.image, 0, 1, 1, 2)
        table.attach(button_copy_text, 1, 2, 0, 1)
        table.attach(button_paste_text, 2, 3, 0, 1)
        table.attach(button_copy_image, 1, 2, 1, 2)
        table.attach(button_paste_image, 2, 3, 1, 2)

        button_copy_text.connect("clicked", self.copy_text)
        button_paste_text.connect("clicked", self.paste_text)
        button_copy_image.connect("clicked", self.copy_image)
        button_paste_image.connect("clicked", self.paste_image)

        self.add(table)

    def copy_text(self, widget):
        self.clipboard.set_text(self.entry.get_text(), -1)

    def paste_text(self, widget):
        text = self.clipboard.wait_for_text()
        if text is not None:
            self.entry.set_text(text)
        else:
            print("No text on the clipboard.")

    def copy_image(self, widget):
        if self.image.get_storage_type() == Gtk.ImageType.PIXBUF:
            self.clipboard.set_image(self.image.get_pixbuf())
        else:
            print("No image has been pasted yet.")

    def paste_image(self, widget):
        image = self.clipboard.wait_for_image()
        if image is not None:
            self.image.set_from_pixbuf(image)

class CellRendererComboWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="CellRendererCombo Example")

        self.set_default_size(200, 200)

        liststore_manufacturers = Gtk.ListStore(str)
        manufacturers = ["Sony", "LG",
            "Panasonic", "Toshiba", "Nokia", "Samsung"]
        for item in manufacturers:
            liststore_manufacturers.append([item])

        self.liststore_hardware = Gtk.ListStore(str, str)
        self.liststore_hardware.append(["Television", "Samsung"])
        self.liststore_hardware.append(["Mobile Phone", "LG"])
        self.liststore_hardware.append(["DVD Player", "Sony"])

        treeview = Gtk.TreeView(model=self.liststore_hardware)

        renderer_text = Gtk.CellRendererText()
        column_text = Gtk.TreeViewColumn("Text", renderer_text, text=0)
        treeview.append_column(column_text)

        renderer_combo = Gtk.CellRendererCombo()
        renderer_combo.set_property("editable", True)
        renderer_combo.set_property("model", liststore_manufacturers)
        renderer_combo.set_property("text-column", 0)
        renderer_combo.set_property("has-entry", False)
        renderer_combo.connect("edited", self.on_combo_changed)

        column_combo = Gtk.TreeViewColumn("Combo", renderer_combo, text=1)
        treeview.append_column(column_combo)

        self.add(treeview)

    def on_combo_changed(self, widget, path, text):
        self.liststore_hardware[path][1] = text
(TARGET_ENTRY_TEXT, TARGET_ENTRY_PIXBUF) = range(2)
(COLUMN_TEXT, COLUMN_PIXBUF) = range(2)

DRAG_ACTION = Gdk.DragAction.COPY

class DragDropWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Drag and Drop Demo")

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        hbox = Gtk.Box(spacing=12)
        vbox.pack_start(hbox, True, True, 0)

        self.iconview = DragSourceIconView()
        self.drop_area = DropArea()

        hbox.pack_start(self.iconview, True, True, 0)
        hbox.pack_start(self.drop_area, True, True, 0)

        button_box = Gtk.Box(spacing=6)
        vbox.pack_start(button_box, True, False, 0)

        image_button = Gtk.RadioButton.new_with_label_from_widget(None,
            "Images")
        image_button.connect("toggled", self.add_image_targets)
        button_box.pack_start(image_button, True, False, 0)

        text_button = Gtk.RadioButton.new_with_label_from_widget(image_button,
            "Text")
        text_button.connect("toggled", self.add_text_targets)
        button_box.pack_start(text_button, True, False, 0)

        self.add_image_targets()

    def add_image_targets(self, button=None):
        targets = Gtk.TargetList.new([])
        targets.add_image_targets(TARGET_ENTRY_PIXBUF, True)

        self.drop_area.drag_dest_set_target_list(targets)
        self.iconview.drag_source_set_target_list(targets)

    def add_text_targets(self, button=None):
        self.drop_area.drag_dest_set_target_list(None)
        self.iconview.drag_source_set_target_list(None)

        self.drop_area.drag_dest_add_text_targets()
        self.iconview.drag_source_add_text_targets()

class DragSourceIconView(Gtk.IconView):

    def __init__(self):
        Gtk.IconView.__init__(self)
        self.set_text_column(COLUMN_TEXT)
        self.set_pixbuf_column(COLUMN_PIXBUF)

        model = Gtk.ListStore(str, GdkPixbuf.Pixbuf)
        self.set_model(model)
        self.add_item("Item 1", "image-missing")
        self.add_item("Item 2", "help-about")
        self.add_item("Item 3", "edit-copy")

        self.enable_model_drag_source(Gdk.ModifierType.BUTTON1_MASK, [],
            DRAG_ACTION)
        self.connect("drag-data-get", self.on_drag_data_get)

    def on_drag_data_get(self, widget, drag_context, data, info, time):
        selected_path = self.get_selected_items()[0]
        selected_iter = self.get_model().get_iter(selected_path)

        if info == TARGET_ENTRY_TEXT:
            text = self.get_model().get_value(selected_iter, COLUMN_TEXT)
            data.set_text(text, -1)
        elif info == TARGET_ENTRY_PIXBUF:
            pixbuf = self.get_model().get_value(selected_iter, COLUMN_PIXBUF)
            data.set_pixbuf(pixbuf)

    def add_item(self, text, icon_name):
        pixbuf = Gtk.IconTheme.get_default().load_icon(icon_name, 16, 0)
        self.get_model().append([text, pixbuf])


class DropArea(Gtk.Label):

    def __init__(self):
        Gtk.Label.__init__(self, "Drop something on me!")
        self.drag_dest_set(Gtk.DestDefaults.ALL, [], DRAG_ACTION)

        self.connect("drag-data-received", self.on_drag_data_received)

    def on_drag_data_received(self, widget, drag_context, x,y, data,info, time):
        if info == TARGET_ENTRY_TEXT:
            text = data.get_text()
            print("Received text: %s" % text)

        elif info == TARGET_ENTRY_PIXBUF:
            pixbuf = data.get_pixbuf()
            width = pixbuf.get_width()
            height = pixbuf.get_height()

            print("Received pixbuf with width %spx and height %spx" % (width,
                height))

class SpinnerAnimation(Gtk.Window):

    def __init__(self):

        Gtk.Window.__init__(self, title="Spinner")
        self.set_border_width(3)

        self.button = Gtk.ToggleButton("Start Spinning")
        self.button.connect("toggled", self.on_button_toggled)
        self.button.set_active(False)

        self.spinner = Gtk.Spinner()

        self.table = Gtk.Table(3, 2, True)
        self.table.attach(self.button, 0, 2, 0, 1)
        self.table.attach(self.spinner, 0, 2, 2, 3)

        self.add(self.table)

    def on_button_toggled(self, button):

        if button.get_active():
            self.spinner.start()
            self.button.set_label("Stop Spinning")

        else:
            self.spinner.stop()
            self.button.set_label("Start Spinning")


clases_br = {
    'DEF': SpinnerAnimation,
    '34': SpinnerAnimation,
    '33': DragDropWindow,
    '32': CellRendererComboWindow,
    '31': ClipboardWindow,
    '21': IconViewWindow,
    '22': TextEditWindow,
    '24': CustomDialogWindow,
    '25': MessageDialogWindow,
    '26': FileChooserWindow,
    '20': CellRendererProgressWindow,
    '18': CellRendererToggleWindow,
    '19': CellRendererPixbufWindow,
    '15': ProgressBarWindow,
    '10': LabelWindow,
    '27': TreeViewFilterWindow,
    '27b': TreeViewOrderWindow,
    '17': CellRendererTextWindow,
    '28': SortableTreeWindow,
    '06': ListBoxWindow,
    '07': StackWindow,
    '08': HeaderBarWindow,
    '09': NoteBook,
    '12': ToggleButtonWindow,
    '14': SpinButtonWindow,
    '30': ComboBoxWindow,
    'xx': None
}

class BuckyRobersWindow(Gtk.Window):

    def __init__(self, GtkParentWindow = None):
        Gtk.Window.__init__(self, title="Elije un Ejemplo")
        self.set_border_width(10)

        class_store = Gtk.ListStore(str, str)
        # Traspaso el diccionario a lista
        lst_clases = []
        for codigo, clase in clases_br.items():
            if codigo != 'DEF' and clase is not None:
                lst_clases.append((codigo, str(clase).replace("<class '__main__.", "")
                    .replace("<class 'tut_gtk_bucky_robers.", "")
                    .replace("'>", "")
                    .replace("Window", "")
                    .replace("<function ", "")
                    .replace(" at 0x", "_")
                ))
        # Traspaso la lista ordenada al ListStore        
        for elemento in sorted(lst_clases):
            class_store.append(elemento)
        #Visualizo el list store en la consola
        for clase in class_store:
            print(clase[:])
            
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        
        combo = Gtk.ComboBox.new_with_model(class_store)
        combo.connect("changed", self.on_combo_changed)
        renderer_text = Gtk.CellRendererText()
        combo.pack_start(renderer_text, True)
        combo.add_attribute(renderer_text, "text", 1)
        vbox.pack_start(combo, False, False, True)
        
        self.add(vbox)
        self.show_all()
        if GtkParentWindow is not None:
            self.set_modal(True)
            self.set_transient_for(GtkParentWindow)

        
    def on_combo_changed(self, combo):
        tree_iter = combo.get_active_iter()
        if tree_iter is not None:
            model = combo.get_model()
            item = model[tree_iter]
            print("Selected:", str(item[:]))
            clave = item[0]
            NuevaVentana = clases_br[clave]()
            NuevaVentana.set_modal(True)
            NuevaVentana.set_transient_for(self)
            NuevaVentana.show_all()

if __name__ == "__main__":
    print("Ejecutando tut_gtk_bucky_robers.py")
    
    BuckyRobersWindow().connect("delete-event", Gtk.main_quit)
    Gtk.main()
    
#    Clase = clases_br['DEF'] 
#    print(str(Clase))
#    Clase().connect("delete-event", Gtk.main_quit)
#    Gtk.main()
    print("tut_gtk_bucky_robers: Adiós muy buenas.")


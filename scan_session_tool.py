#!/usr/bin/env python

__version__ = '0.7.0'
__date__ = '21 Mar 2019'


import sys
import os
import platform
import time
import glob
import shutil
from tempfile import mkstemp
if sys.version[0] == '3':
    from tkinter import *
    from tkinter.ttk import *
    from tkinter import font as tkFont
    from tkinter import filedialog as tkFileDialog
    from tkinter import messagebox as tkMessageBox
    from tkinter.scrolledtext import ScrolledText
else:
    from Tkinter import *
    from ttk import *
    import tkFont
    import tkFileDialog
    import tkMessageBox
    from ScrolledText import ScrolledText

import yaml


docs = """
+ - - - - - - - - - - - - - - Scan Session Tool - - - - - - - - - - - - - - +
|                                                                           |
|        A tool for MR scan session documentation and data archiving        |
|                                                                           |
|             Authors: Florian Krause <Florian.Krause@fladd.de>             |
|                      Nikos Kogias <n.kogias@student.ru.nl>                |
|                                                                           |
+ - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - +



=================================== About ===================================

The Scan Session Tool is a graphical application for documenting (f)MRI scan
sessions and automatized data archiving. Information about the scan session
itself, used forms and documents, as well as the single measurements can be
entered and saved into a protocol file. This information can furthermore be
used to copy acquired data (DICOM images as well as optional stimulation
protocols, logfiles and Turbo-BrainVoyager files) into a specific
hierarchical folder structure for unified archiving purposes.



=================================== Usage ===================================

The user interface is organized into three different content areas, each hol-
ding different information about the scan session, as well as an additional
control area for opening and saving session information and for automatically
archiving acquired data, based on the session information.


----------------------- The "General Information" area ----------------------

This area provides input fields for basic information about the scan session.
Some of the fields allow for a selection of pre-specified values taken from a
config file (see below), while others take freely typed characters.
Fields that are marked with a red background, are mandatory and need to be
filled in. Fields that are marked with an orange background are automatically
filled in, but need to be checked.
The following fields are available:
    "Project"        - The project identifier
                       (free-type and selection)
    "Subject"        - The subject number
                       (001-999)
                     - The subject identifier
                       (free-type and selection)
    "Session"        - The session number
                       (001-999)
                     - The session identifier
                       (free-type and selection)
    "Date"           - The date of the scan session
                       (free-type, auto-filled)
    "Booked Time"    - The time period the scanner was booked
                       (free-type)
    "Actual Time"    - The time period the scanner was actually used
                       (free-type)
    "Certified User" - The responsible user
                       (free-type and selection)
    "Backup Person"  - An additional person
                       (free-type and selection)
    "Notes"          - Any additional notes about the session
                       (free-type)


--------------------------- The "Documents" area ----------------------------

This area provides input fields for additional documents that are acquired
during the session, such as logfiles and behavioural data files, as well as 
questionnaires and forms that are filled in by the participant. The following
input fields are available:
    "Files"       - A newline separated list of all session logfiles and ad-
                    ditional documents; wildcard masks (*) will be completed
                    during archiving
                    (free-type)
    "Checklist"   - Checkboxes to specify which forms and documents have been 
                    collected from the participant. Additional documents can 
                    be specified in a configuration file (see "Config File" 
                    section). The following checkboxes are available:
                    "MR Safety Screening Form"            - The (f)MRI scree-
                                                            ning from provi-
                                                            ded by the scan-
                                                            ning institution
                    "Participation Informed Consent Form" - The official MRI 
                                                            written consent 
                                                            form


------------------------- The "Measurements" area ---------------------------

This area provides several input fields for each measurement of the session.
When starting the application, only one (empty) measurement is shown. Click-
ing on "Add Measurement" will create additional measurements. Fields that are
marked with a red background, are mandatory and need to be filled in. Fields
that are marked with an orange background are automatically filled in, but
need to be checked.
The following input fields are available per measurement:
    "No"                   - The number of the measurement
                             (001-999)
    "Type"                 - "anatomical", "functional" or "misc"
                             (selection)
    "Vols"                 - The number of volumes of the measurement
                             (free-type)
    "Name"                 - The name of the measurement
                             (free-type, selection)
    "Logfiles"             - A newline separated list of all connected
                             logfiles; wildcard masks (*) will be completed
                             during archiving (please note that a stimulation
                             protocol mask will be included automatically,
                             based on the session information)
                             (free-type)
    "Comments"             - Any additional comments about the measurement
                             (free-type)


----------------------------- The control area ------------------------------

The control area consists of the following three buttons:
    "Open"    - Opens previously saved information from a text file
    "Save"    - Saves the entered session information into a text file
    "Archive" - Copies acquired data from specified location into a time-
                stamped sub-folder <~Archiveyyymmdd>. Please note that all
                data is expected to be within the specified folder. That is,
                all DICOM files (*.dcm OR *.IMA; with or without sub-folders),
                all stimulation protocols, all logfiles as well as all Turbo-
                BrainVoyager files (all *.tbv files in a folder called
                'TBVFiles').
                The data will be copied into the following folder hierarchy:
                    DICOMs -->
                      <Project>/<Subject>/<Session>/<Type>/<Name>/<DICOM>/
                    BrainVoyager files (links only) -->
                      <Project>/<Subject>/<Session>/<BV>/
                    Logfiles -->
                      <Project>/<Subject>/<Session>/<Type>/<Name>/
                    Files -->
                      <Project>/<Subject>/<Session>/
                    Turbo-BrainVoyager files (links only) -->
                      <Project>/<Subject>/<Session>/<TBV>/
                    Scan Session Protocol -->
                      <Project>/<Subject>/<Session>/



================================ Config File ================================

A configuration file can be created to pre-define the values to be used as
selection options for the "Subject", "Session", "Certified User", "Backup
Person", "Notes", the measurement "Name", "Vols" and "Comments" on a per
project basis, as well as additional items in the "Files" and "Checklist" 
fields of the "Documents" section.The Scan Session Tool will look for a con-
figuration file with the name "sst.yaml", located in the same directory as
the application itself (does not work for the OS X compiled .app) or in the
$HOME folder. 

The syntax is YAML. Here is an example:

Project 1:
    SubjectTypes:
        - Group1
        - Group2

    SessionTypes:
        - Sess1
        - Sess2

    Users:
        - User1
        - User2

    Backups:
        - User1
        - User2

    Notes: |
           Subject details
           ---------------

           Age:
           Gender: m[ ] f[ ]

    Files: 
        - "*.txt"

    Checklist: 
        - Pre-Scan Questionnaire
        - Post-Scan Questionnaire

    Measurements anatomical:
        - Name:        Localizer
          Vols:        3

        - Name:        Anatomy
          Vols:        192

    Measurements functional:
        - Name:        Run1
          Vols:        300
          Comments:    |
                       Answer 1:

        - Name:        Run2
          Vols:        400
          Comments:    |
                       Answer 2:

        - Name:        Run3
          Vols:        200
          Comments:    |
                       Answer 3:

    Measurements misc:
        - Name:        Run1incomplete
          Vols:
          Comments:


Project 2:
    SubjectTypes:
        - GroupA
        - GroupB

    SessionTypes:
        - SessA
        - SessB

    Users:
        - UserA
        - UserB

    Backups:
        - UserA
        - UserB

    Notes: |
           Subject details
           ---------------

           Age:
           Gender: m[ ] f[ ]

    Files: 
        - "*.txt"

    Checklist:
        - Participation Reimbursement Form

    Measurements anatomical:
        - Name:        Localizer
          Vols:        3

        - Name:        MPRAGE
          Vols:        192

    Measurements functional:
        - Name:        RunA
          Vols:        300
          Comments:    |
                       Answer 1:

        - Name:        RunB
          Vols:        400
          Comments:    |
                       Answer 2:

        - Name:        RunC
          Vols:        200
          Comments:    |
                       Answer 3:

    Measurements misc:
        - Name:        RunAImcomplete
          Vols:
          Comments:
"""

def replace(file_path, pattern, subst):

    #Create temp file
    fh, abs_path = mkstemp()
    new_file = open(abs_path,'w')
    old_file = open(file_path)
    for line in old_file:
        new_file.write(line.replace(pattern, subst))
    #close temp file
    new_file.close()
    os.close(fh)
    old_file.close()
    #Remove original file
    os.remove(file_path)
    #Move new file
    shutil.move(abs_path, file_path)


class FixedSizeFrame(Frame):
    def __init__(self, master, width, height, **kw):
        Frame.__init__(self, master, **kw)
        self["width"] = width
        self["height"] = height
        self.grid_propagate(False)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)


class AutoScrollbarText(Text):
    def __init__(self, master=None, **kw):
        self.frame = Frame(master)
        self.yvbar = Scrollbar(self.frame)
        #self.xvbar = Scrollbar(self.frame, orient="horizontal")
        self.yvbar.grid(row=0, column=1, sticky="NS")
        #self.xvbar.grid(row=1, column=0, sticky="WE")

        kw.update({'yscrollcommand': self.set_yvbar})
        #kw.update({'xscrollcommand': self.set_xvbar})
        Text.__init__(self, self.frame, undo=True, **kw)
        self.grid(row=0, column=0, sticky="WENS")
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        self.yvbar['command'] = self.yview
        #self.xvbar['command'] = self.xview

        self.undo_history = 0
        if platform.system() == "Darwin":
            self.bind("<Command-z>", self.undo_dummy)
            self.bind("<Command-Z>", self.redo)
        else:
            self.bind("<Control-z>", self.undo_dummy)
            self.bind("<Control-Z>", self.redo)

        # Copy geometry methods of self.frame without overriding Text
        # methods -- hack!
        text_meths = list(vars(Text).keys())
        methods = list(vars(Pack).keys()) + list(vars(Grid).keys()) + \
                list(vars(Place).keys())
        methods = set(methods).difference(text_meths)

        for m in methods:
            if m[0] != '_' and m != 'config' and m != 'configure':
                setattr(self, m, getattr(self.frame, m))

    def undo_dummy(self, *args):
        if self.edit_modified():
            self.undo_history += 1

    def redo(self, *args):
        if self.undo_history > 0:
            self.edit_redo()
            self.undo_history -= 1

    def set_yvbar(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            # grid_remove is currently missing from Tkinter!
            self.yvbar.tk.call("grid", "remove", self.yvbar)
        else:
            self.yvbar.grid()
        self.yvbar.set(lo, hi)

    # def set_xvbar(self, lo, hi):
    #     print lo, hi
    #     if float(lo) <= 0.0 and float(hi) >= 1.0:
    #         # grid_remove is currently missing from Tkinter!
    #         self.xvbar.tk.call("grid", "remove", self.xvbar)
    #     else:
    #         self.xvbar.grid()
    #     self.xvbar.set(lo, hi)

    def __str__(self):
        return str(self.frame)

    def copy_logfiles(self, source, destination):
        original = self.get(1.0, END)
        logfiles = original.split("\n")
        logfiles = [x.strip() for x in logfiles if x != ""]
        warning = ""
        new = original
        for logfile in logfiles:
            if "*" in logfile:
                replaced = []
            try:
                if logfile != "" and not os.path.isdir(logfile):
                    files = glob.glob(os.path.join(source, logfile))
                    if files == []:
                        raise Exception
                    for file_ in files:
                        if not os.path.isdir(file_):
                            if "*" in logfile:
                                replaced.append(
                                    os.path.split(file_)[-1])
                            shutil.copyfile(
                                file_,
                                os.path.join(destination,
                                             os.path.split(file_)[-1]))
                    if "*" in logfile:
                        new = new.replace(
                            logfile, "\n".join(replaced))
                        self.delete(1.0, END)
                        self.insert(1.0, new)
                
                if logfile != "" and os.path.isdir(os.path.join(source, logfile)):
                    shutil.copytree(os.path.abspath(os.path.join(source, logfile)), 
                                    os.path.abspath(os.path.join(destination, logfile)))
            except:
               warning += "\nError copying logfiles " \
                   "'{}' not found\n".format(logfile)
        return warning
        

class VerticalScrolledFrame(Frame):
    """A pure Tkinter scrollable frame that actually works!

    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling

    """
    def __init__(self, parent, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)

        # create a canvas object and a vertical scrollbar for scrolling it
        self.vscrollbar = Scrollbar(self, orient=VERTICAL)
        self.vscrollbar.pack(fill=Y, side=RIGHT, expand=TRUE)
        self.canvas = Canvas(self, bd=0, highlightthickness=0,
                        yscrollcommand=self.vscrollbar.set,
                        width=self.winfo_reqwidth(),
                        height=self.winfo_reqheight(), background="grey")
        self.canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        self.vscrollbar.config(command=self.canvas.yview)

        # reset the view
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        style = Style()
        style.configure("Grey.TFrame", background="darkgrey")
        self.interior = Frame(self.canvas, width=self.winfo_reqwidth(),
                              style="Grey.TFrame")
        self.interior.grid_rowconfigure(0, weight=1)
        self.interior.grid_columnconfigure(0, weight=1)
        self.interior_id = self.canvas.create_window(0, 0,
                                                     window=self.interior,
                                                     anchor=NW)

        #self.canvas.bind('<Configure>', self._configure_canvas)
        self.interior.bind('<Configure>', self._configure_interior)

        return

    def bind_mouse_wheel(self, *args):
        os = platform.system()
        self.bind_ids = []
        if os == "Linux":
            self.bind_ids.append(self.vscrollbar.bind_all("<4>",
                                                      self._on_mousewheel))
            self.bind_ids.append(self.vscrollbar.bind_all("<5>",
                                                      self._on_mousewheel))
        else:
            self.bind_ids.append(self.vscrollbar.bind_all("<MouseWheel>",
                                                      self._on_mousewheel))

    def unbind_mouse_wheel(self, *args):
        try:
            for x in self.bind_ids:
                os = platform.system()
                if os == "Linux":
                    self.vscrollbar.unbind("<4>", x)
                    self.vscrollbar.unbind("<5>", x)
                else:
                    self.vscrollbar.unbind("<MouseWheel>", x)
        except:
            pass

    # track changes to the canvas and frame width and sync them,
    # also updating the scrollbar
    def _configure_interior(self, event):
        # update the scrollbars to match the size of the inner frame
        if self.interior.winfo_reqheight() < self.winfo_reqheight():
            size = (self.interior.winfo_reqwidth(),
                    self.winfo_reqheight())
        else:
            size = (self.interior.winfo_reqwidth(),
                    self.interior.winfo_reqheight())
        self.canvas.config(scrollregion="0 0 %s %s" % size)
        if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
            # update the canvas's width to fit the inner frame
            #self.canvas.config(width=self.interior.winfo_reqwidth())
            pass

    def _configure_canvas(self, event):
        if self.interior.winfo_reqwidth() != self.canvas.winfo_width():
            # update the inner frame's width to fill the canvas
            self.canvas.itemconfigure(self.interior_id,
                                      width=self.canvas.winfo_width())

    def _on_mousewheel(self, event):
        os = platform.system()
        if os == "Linux":
            if event.num == 4:
                self.canvas.yview_scroll(-2, "units")
            elif event.num == 5:
                self.canvas.yview_scroll(2, "units")
        elif os == "Darwin":
            self.canvas.yview_scroll(-2*event.delta, "units")
        elif os == "Windows":
            self.canvas.yview_scroll(-2*(event.delta/120), "units")


class AutocompleteCombobox(Combobox):

    def set_completion_list(self, completion_list):
        self._completion_list = sorted(completion_list, key=str.lower)
        self._hits = []
        self._hit_index = 0
        self.position = 0
        self.bind('<KeyRelease>', self.handle_keyrelease)
        self['values'] = self._completion_list

    def autocomplete(self, delta=0):
        if delta:  # delete selection, otherwise we would fix current position
            self.delete(self.position, END)
        else:  # set position to end so selection starts where textentry ended
            self.position = len(self.get())
        # collect hits
        _hits = []
        for element in self._completion_list:
            if element.lower().startswith(self.get().lower()):
                _hits.append(element)
        # if we have a new hit list, keep this in mind
        if _hits != self._hits:
            self._hit_index = 0
            self._hits = _hits
        # only allow cycling if we are in a known hit list
        if _hits == self._hits and self._hits:
            self._hit_index = (self._hit_index + delta) % len(self._hits)
        # now finally perform the auto completion
        if self._hits:
            self.delete(0, END)
            self.insert(0, self._hits[self._hit_index])
            self.select_range(self.position, END)

    def handle_keyrelease(self, event):
        """event handler for the keyrelease event on this widget"""
        if event.keysym == "BackSpace":
            self.delete(self.index(INSERT), END)
            self.position = self.index(END)
        elif event.keysym == "Left":
            #if self.position < self.index(END):  # delete the selection
            #    self.delete(self.position, END)
            #else:
            self.position = self.position - 1  # delete one character
                #self.delete(self.position, END)
        elif event.keysym == "Right":
            self.position = self.index(END)  # go to end (no selection)
        elif len(event.keysym) == 1:
            self.autocomplete()
            # No need for up/down, we'll jump to the popup
            # list at the position of the autocompletion

class Spinbox(Entry):
    def __init__(self, master=None, **kw):
        s = Style()
        Entry.__init__(self, master, "ttk::spinbox", **kw)

    def current(self, newindex=None):
        return self.tk.call(self._w, 'current', newindex)

    def set(self, value):
        return self.tk.call(self._w, 'set', value)


class App(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)

        font = tkFont.nametofont("TkDefaultFont")
        font.config(family="Arial", size=-13)
        self.default_font = font.cget("family")
        self.default_font_size = font.cget("size")
        self.font = (self.default_font, self.default_font_size)

        style = Style()
        self.red = "#fc625d"
        self.orange = "#fdbc40"
        style.configure("Blue.TLabel", foreground="royalblue")
        style.configure("Grey.TLabel", foreground="darkgrey")
        style.configure("Header.TLabel", background="darkgrey")
        style.configure("Header.TFrame", background="darkgrey")
        style.configure("Red.TCombobox", fieldbackground=self.red)
        style.configure("Orange.TCombobox", fieldbackground=self.orange)
        style.map("Orange.TCombobox", fieldbackground=[("readonly", self.orange)])
        style.configure("Red.TEntry", fieldbackground=self.red)
        style.configure("Orange.TEntry", fieldbackground=self.orange)
        style.configure("Orange.TSpinbox", fieldbackground=self.orange)
        style.map("Orange.TSpinbox", fieldbackground=[("disabled", self.orange)])

        self.menubar = Menu(master)
        if platform.system() == "Darwin":
            modifier = "Command"
            self.apple_menu = Menu(self.menubar, name="apple")
            self.menubar.add_cascade(menu=self.apple_menu)
            self.apple_menu.add_command(
                label="About Scan Session Tool",
                command=lambda: HelpDialogue(self.master).show())
        else:
            modifier = "Control"
        self.file_menu = Menu(self.menubar)
        self.menubar.add_cascade(menu=self.file_menu, label="File")
        self.file_menu.add_command(label="Open", command=self.open,
                                   accelerator="{0}-O".format(modifier))
        self.master.bind("<{0}-o>".format(modifier), self.open)
        self.file_menu.add_command(label="Save", command=self.save,
                                   accelerator="{0}-S".format(modifier))
        self.file_menu.add_command(label="Archive", command=self.archive,
                                   accelerator="{0}-R".format(modifier))
        self.edit_menu = Menu(self.menubar)
        self.menubar.add_cascade(menu=self.edit_menu, label="Edit")
        self.edit_menu.add_command(label="Add Measurement",
                                   command=self.new_measurement,
                                   accelerator="{0}-M".format(modifier))
        self.master.bind("<{0}-m>".format(modifier), self.new_measurement)
        self.edit_menu.add_command(label="Delete Measurement",
                                   command=self.del_measurement,
                                   accelerator="{0}-D".format(modifier))
        self.master.bind("<{0}-d>".format(modifier), self.del_measurement)
        self.edit_menu.add_command(
            label="Scroll Measurements Up",
            command=lambda: app.measurements_frame.canvas.yview_scroll(
                -2, "units"),
            accelerator="{0}-Up".format(modifier))
        self.master.bind(
            "<{0}-Up>".format(modifier),
            lambda x: app.measurements_frame.canvas.yview_scroll(-2, "units"))
        self.edit_menu.add_command(
            label="Scroll Measurements Down",
            command=lambda: app.measurements_frame.canvas.yview_scroll(
                2, "units"),
            accelerator="{0}-Down".format(modifier))
        self.master.bind(
            "<{0}-Down>".format(modifier),
            lambda x: app.measurements_frame.canvas.yview_scroll(2, "units"))
        self.help_menu = Menu(self.menubar)
        self.menubar.add_cascade(menu=self.help_menu, label="Help")
        self.help_menu.add_command(
            label="Scan Session Tool Help",
            command=lambda: HelpDialogue(self.master).show(),
            accelerator="F1")
        self.master.bind("<F1>", lambda x: HelpDialogue(self.master).show())
        master["menu"] = self.menubar

        master.rowconfigure(0, weight=1)
        master.columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid(sticky="WENS")
        self.general = ("Project:",
                        "Subject:",
                        #"Group:",
                        "Session:",
                        "Date:",
                        "Time A:",
                        "Time B:",
                        "User 1:",
                        "User 2:")
        self.documents = ["MR Safety Screening Form",
                          "Participation Informed Consent Form"]

        self.measurement = ("No.", "Type", "Vols", "Name",
                            "Logfiles", "Comments")

        self.documents_vars = []
        self.additional_documents = []
        self.additional_documents_vars = []
        self.additional_documents_widgets = []
        self.measurements = []
        self.measurements_widgets = []
        self.nofocus_widgets = []
        self.prt_files = []
        self.config = {}
        self.load_config()
        self.create_widgets()

    def create_widgets(self):
        self.top_frame = Frame(self)
        self.top_frame.columnconfigure(1, weight=1)
        self.top_frame.grid(row=0, sticky="WE", padx=10, pady=10)
        self.nofocus_widgets.append(self.top_frame)
        general_label = Label(self.top_frame, text="General Information")
        general_label['font'] = (self.default_font,
                                 self.default_font_size - 2,
                                 "bold")
        self.nofocus_widgets.append(general_label)
        self.general_frame = LabelFrame(self.top_frame,
                                        text='General Information',
                                        labelwidget=general_label,
                                        width=1024)
        self.general_frame.grid_columnconfigure(1, weight=1)
        self.general_frame.grid(row=0, column=0, sticky="NSWE")
        self.nofocus_widgets.append(self.general_frame)
        self.general_labels = []
        self.general_widgets = []
        self.general_vars = []


        self.general_frame_left = Frame(self.general_frame)
        self.general_frame_left.grid(row=0, column=0, sticky="N", padx=10)
        self.general_frame_right = Frame(self.general_frame)
        self.general_frame_right.grid(row=0, column=1, padx=10, sticky="N")

        for row, x in enumerate(self.general):
            label = Label(self.general_frame_left, text=x)
            label['font'] = (self.default_font, self.default_font_size, "bold")
            label.grid(row=row, column=0, sticky="E", padx=(0, 3), pady=3)
            self.general_labels.append(label) 
            if row in (1, 2):
                width = 13  #10
                if platform.system() == "Windows":
                    width += 3
                frame = Frame(self.general_frame_left)  #, width=width) 
                var1 = StringVar()
                var1.trace("w", self.change_callback)
                var1.set("001")
                spinbox = Spinbox(frame, from_=1, to=999, format="%03.0f",
                          width=3, justify="right", textvariable=var1,
                          state="readonly", font=self.font, style="Orange.TSpinbox")
                pad = 7
                if platform.system() == "Windows":
                    pad -= 4
                spinbox.grid(row=0, column=0, sticky="W", padx=(0,pad))
                var2 = StringVar()
                var2.trace("w", self.change_callback)
                combobox = AutocompleteCombobox(frame, textvariable=var2,
                                                validate=validate, validatecommand=vcmd,
                                                font=self.font, width=width)
                combobox.grid(row=0, column=1, sticky="W")
                self.general_vars.append([var1, var2])
                self.general_widgets.append([spinbox, combobox])
                frame.grid(row=row, column=1, sticky="W")
            elif row in (0, 6, 7):
                var = StringVar()
                var.trace("w", self.change_callback)
                self.general_vars.append(var)
                validate = None
                vcmd = None
                #validate = "key"
                #vcmd = (self.master.register(self.validate),
                #[chr(x) for x in range(127)],
                #49, '%S', '%P')
                if row == 0:
                    width = 20
                    if platform.system() == "Windows":
                        width += 3
                    combobox = AutocompleteCombobox(self.general_frame_left, textvariable=var,
                                                    validate=validate, validatecommand=vcmd,
                                                    font=self.font, width=width,
                                                    style="Red.TCombobox")
                else:
                    width = 20
                    if platform.system() == "Windows":
                        width += 3
                    combobox = AutocompleteCombobox(self.general_frame_left, textvariable=var,
                                                    validate=validate, validatecommand=vcmd,
                                                    font=self.font, width=width)

                if row == 0:
                    projects = sorted(self.config.keys())
                    #projects.sort()
                    combobox.set_completion_list(projects)
                combobox.grid(row=row, column=1, sticky="W")
                self.general_widgets.append(combobox)
            elif row in (3, 4, 5):
                var = StringVar()
                var.trace("w", self.change_callback)
                self.general_vars.append(var)
                if row == 3:
                    validate = "key"
                    vcmd = (self.master.register(self.validate),
                            "0123456789-", 10, '%S', '%P')
                    width = 10
                    self.autofill_date_callback()
                elif row in (4, 5):
                    validate = "key"
                    vcmd = (self.master.register(self.validate),
                            "0123456789:-", 11, '%S', '%P')
                    width = 10
                if row == 3:
                    entry = Entry(self.general_frame_left, width=width,
                                  textvariable=var, validate=validate,
                                  validatecommand=vcmd, font=self.font,
                                  style="Orange.TEntry")
                else:
                    entry = Entry(self.general_frame_left, width=width,
                                  textvariable=var, validate=validate,
                                  validatecommand=vcmd, font=self.font)
                #if row == 4:
                    #entry.bind('<T>', self.autofill_date_callback)
                entry.grid(row=row, column=1, sticky="W")
                self.general_widgets.append(entry)

        notes_label = Label(self.general_frame_right, text="Notes:",
                            style="Green.TLabel")
        notes_label.grid(row=0, column=0, sticky="W")
        notes_label['font'] = (self.default_font, self.default_font_size, "bold")
        notes_container = FixedSizeFrame(self.general_frame_right, 299, 171)
        notes_container.grid(row=1, column=0, sticky="N")
        notes = AutoScrollbarText(notes_container, wrap=NONE)
        notes.grid(row=0, column=0, sticky="N")
        self.general_widgets.append(notes)
        notes.bind('<KeyRelease>', self.change_callback)
        for label in self.general_labels:
            self.nofocus_widgets.append(label)

        self.control_frame = Frame(self.top_frame)
        self.control_frame.grid_rowconfigure(0, weight=1)
        self.control_frame.grid(row=0, column=1, sticky="NS")
        self.nofocus_widgets.append(self.control_frame)
        self.logo = Frame(self.control_frame)
        self.logo.grid(row=0, column=0)
        self.nofocus_widgets.append(self.logo)
        self.title1 = Label(self.logo, text="Scan",
                           justify="center", style="Blue.TLabel")
        self.title1.grid(row=0)
        self.title1['font'] = (self.default_font,
                              self.default_font_size - 10,
                              "bold")
        self.nofocus_widgets.append(self.title1)
        self.title2 = Label(self.logo, text="Session",
                           justify="center", style="Blue.TLabel")
        self.title2.grid(row=1)
        self.title2['font'] = (self.default_font,
                              self.default_font_size - 10,
                              "bold")
        self.nofocus_widgets.append(self.title2)
        self.title3 = Label(self.logo, text="Tool",
                           justify="center", style="Blue.TLabel")
        self.title3.grid(row=2)
        self.title3['font'] = (self.default_font,
                              self.default_font_size - 10,
                              "bold")
        self.nofocus_widgets.append(self.title3)
        self.version1 = Label(self.logo,
                             text="Version {0}".format(__version__),
                             style="Grey.TLabel")
        self.version1.grid(row=3)
        self.version1['font'] = (self.default_font, self.default_font_size + 2)
        self.nofocus_widgets.append(self.version1)
        self.version2 = Label(self.logo,
                             text="({0})".format(__date__),
                             style="Grey.TLabel")
        self.version2.grid(row=4)
        self.version2['font'] = (self.default_font, self.default_font_size + 2)
        self.nofocus_widgets.append(self.version2)
        self.help = Button(self.logo, text="?", width=1,
                           command=lambda: HelpDialogue(self.master).show())
        self.help.grid(row=5, pady=5)

        self.button_frame = Frame(self.control_frame)
        self.button_frame.grid(row=1, column=0, padx=10)
        self.nofocus_widgets.append(self.button_frame)
        self.open_button = Button(self.button_frame, text="Open",
                                  command=self.open, state="enabled")
        self.open_button.grid(row=0, column=0, sticky="")
        self.save_button = Button(self.button_frame, text="Save",
                                  command=self.save)
        self.save_button.grid(row=1, column=0, sticky="", pady=3)
        self.go_button = Button(self.button_frame, text="Archive",
                                state="disabled", command=self.archive)
        self.go_button.grid(row=2, column=0, sticky="")
        documents_label = Label(self.top_frame, text="Documents")
        documents_label['font'] = (self.default_font,
                                   self.default_font_size - 2,
                                   "bold")
        self.nofocus_widgets.append(documents_label)
        self.documents_frame = LabelFrame(self.top_frame, text='Documents',
                                          labelwidget=documents_label)
        self.documents_frame.grid(row=0, column=2, sticky="NSE")
        self.nofocus_widgets.append(self.documents_frame)
        files_label = Label(self.documents_frame, text="Files:")
        files_label.grid(row=0, sticky="W", padx=10)
        files_label['font'] = (self.default_font, self.default_font_size, "bold")

        self.nofocus_widgets.append(files_label)
        files_container = FixedSizeFrame(self.documents_frame, 299, 53)  #68
        files_container.grid(row=1, sticky="NSEW", padx=10)
        self.nofocus_widgets.append(files_container)
        self.files = AutoScrollbarText(files_container, wrap=NONE, background=self.orange,
                                       highlightbackground=self.orange)
        self.files.bind('<KeyRelease>', self.change_callback)
        self.files.frame.bind('<Enter>',
                        lambda event: self.mouseover_callback(True))
        self.files.frame.bind('<Leave>',
                        lambda event: self.mouseover_callback(False))
        self.files.grid(sticky="NWES")
        empty_label = Label(self.documents_frame, text="")
        empty_label.grid(row=2, sticky="W", padx=10)
        self.nofocus_widgets.append(empty_label)
        checklist_label = Label(self.documents_frame, text="Checklist:")
        checklist_label.grid(row=3, sticky="W", padx=10)
        checklist_label['font'] = (self.default_font, self.default_font_size, "bold")
        self.nofocus_widgets.append(checklist_label)
        self.documents_labels = []
        self.documents_checks = []
        self.documents_vars = []
        for row, x in enumerate(self.documents):
            var = IntVar()
            var.trace("w", self.change_callback)
            check = Checkbutton(self.documents_frame, text=x, variable=var)
            check.grid(row=row+4, sticky="W", padx=10)
            self.documents_vars.append(var)
        
        self.bottom_frame = Frame(self)
        self.bottom_frame.grid_columnconfigure(0, weight=1)
        self.bottom_frame.grid(row=1, column=0, padx=10, pady=10,
                               sticky="WENS")
        self.nofocus_widgets.append(self.bottom_frame)
        measurements_label = Label(self.bottom_frame, text="Measurements")
        measurements_label['font'] = (self.default_font,
                                      self.default_font_size - 2,
                                      "bold")
        self.nofocus_widgets.append(measurements_label)
        self.measurements_frame1 = LabelFrame(self.bottom_frame,
                                              text='Measurements',
                                              labelwidget=measurements_label)
        self.measurements_frame1.grid_rowconfigure(1, weight=1)
        self.measurements_frame1.grid(row=0, sticky="WENS")
        self.nofocus_widgets.append(self.measurements_frame1)
        self.measurements_frame = VerticalScrolledFrame(
            self.measurements_frame1, height=295, width=989) #989
        self.measurements_frame.interior.grid_columnconfigure(0, weight=1)
        self.measurements_frame.interior.grid_rowconfigure(0, weight=1)
        self.measurements_frame.grid(row=1, sticky="WENS")
        self.nofocus_widgets.append(self.measurements_frame)
        self.nofocus_widgets.append(self.measurements_frame.interior)
        self.nofocus_widgets.append(self.measurements_frame.canvas)
        add_del_frame = Frame(self.measurements_frame1)
        add_del_frame.grid(row=2, pady=(10, 10))
        self.scanning_add = Button(add_del_frame,
                                   text="+", width=3,
                                   command=self.new_measurement)
        self.scanning_add.grid(row=0, column=0, padx=5)
        self.scanning_del = Button(add_del_frame,
                                   text="-", width=3,
                                   command=self.del_measurement)
        self.scanning_del.grid(row=0, column=1, padx=5)
        self.measurements_frame.canvas.bind("<Double-Button-1>",
                                            lambda x: self.new_measurement())

        label_frame = Frame(self.measurements_frame1)
        label_frame.grid(row=0, columnspan=6, sticky="W")
        for column, x in enumerate(self.measurement):
            label = Label(label_frame, text=x)
            if column == 0:
                label.grid(row=0, column=column, padx=(18, 0), pady=(3, 3))
            elif column == 1:
                p = 45
                if platform.system() == "Windows":
                    p += 1
                label.grid(row=0, column=column, padx=(p, 0))
            elif column == 2:
                label.grid(row=0, column=column, padx=(39, 0))
            elif column == 3:
                p = 76
                if platform.system() == "Windows":
                    p -= 1
                label.grid(row=0, column=column, padx=(76, 0))
            elif column == 4:
                p = 195
                if platform.system() == "Windows":
                    p += 2
                label.grid(row=0, column=column, padx=(p, 0))
            elif column == 5:
                p = 243
                if platform.system() == "Windows":
                    p += 4
                label.grid(row=0, column=column, padx=(p, 130))

            label['font'] = (self.default_font, self.default_font_size,
                             "bold")
            label.bind('<Button-1>', lambda x: app.master.focus())
        self.new_measurement()


    def new_measurement(self, *args):
        #for column, x in enumerate(self.measurement):
            #label = Label(self.measurements_frame.interior, text=x)
            #if column == 0:
                #label.grid(row=0, column=column, padx=(10, 2))
            #elif column == len(self.measurements) - 1:
                #label.grid(row=0, column=column, padx=(2, 10))
            #else:
                #label.grid(row=0, column=column, padx=2)
            #label['font'] = (self.default_font, self.default_font_size,
                             #"bold")
            #label.bind('<Button-1>', lambda x: app.master.focus())
        value = repr(len(self.measurements) + 1).zfill(3)
        scanning_vars = []
        scanning_widgets = []
        var1 = StringVar()
        scanning_vars.append(var1)
        var1.set(value)
        var1.trace("w", self.change_callback)
        spinbox = Spinbox(self.measurements_frame.interior, from_=1, to=99,
                          format="%03.0f",width=3, justify="right",
                          state="readonly", textvariable=var1, font=self.font,
                          style="Orange.TSpinbox")
        spinbox.grid(row=value, column=0, sticky="W", padx=(10, 2))
        spinbox.bind('<Enter>',
                     lambda event: self.mouseover_callback(True))
        spinbox.bind('<Leave>',
                     lambda event: self.mouseover_callback(False))
        scanning_widgets.append(spinbox)
        var2 = StringVar()
        var2.trace("w", self.change_callback)
        scanning_vars.append(var2)

        #radiobuttons = Frame(self.measurements_frame.interior)
        #radiobuttons.grid(row=value, column=1, sticky="")
        #radio_var = StringVar()
        #radio_var.set("misc")
        #Radiobutton(radiobuttons, text="anat", variable=radio_var,
        #            value="anatomical").pack(anchor="w")
        #Radiobutton(radiobuttons, text="func", variable=radio_var,
        #            value="functional").pack(anchor="w")
        #Radiobutton(radiobuttons, text="misc", variable=radio_var,
        #            value="misc").pack(anchor="w")
        width = 9 #9
        if platform.system() == "Windows":
            width += 2
        combobox = AutocompleteCombobox(self.measurements_frame.interior,
                            textvariable=var2, width=width, state="readonly",
                            font=self.font, style="Orange.TCombobox")
        combobox.set_completion_list(["anatomical", "functional", "misc"])
        combobox.current(0)
        combobox.grid(row=value, column=1, sticky="", padx=2)
        combobox.bind('<Enter>',
                      lambda event: self.mouseover_callback(True))
        combobox.bind('<Leave>',
                      lambda event: self.mouseover_callback(False))
        scanning_widgets.append(combobox)

        var3 = StringVar()
        var3.trace("w", self.change_callback)
        scanning_vars.append(var3)
        validate = "key"
        vcmd = (self.master.register(self.validate),
                "0123456789", 4, '%S', '%P')

        vols = Entry(self.measurements_frame.interior, width=4,
                       justify="right", textvariable=var3,
                       validate=validate, validatecommand=vcmd,
                       font=self.font, style="Red.TEntry")
        vols.grid(row=value, column=2, sticky="", padx=2)
        scanning_widgets.append(vols)
        var4 = StringVar()
        var4.trace("w", self.change_callback)
        scanning_vars.append(var4)
        validate = None
        vcmd = None
        #validate = "key"
        #vcmd = (self.master.register(self.validate),
        #        [chr(x) for x in range(127)],
        #        49, '%S', '%P')
        width = 20
        if platform.system() == "Windows":
            width += 3
        name = AutocompleteCombobox(self.measurements_frame.interior,
                                    textvariable=var4, validate=validate,
                                    validatecommand=vcmd, font=self.font,
                                    style="Red.TCombobox", width=width)
        name.grid(row=value, column=3, sticky="", padx=2)
        name.bind('<Enter>',
                  lambda event: self.mouseover_callback(True))
        name.bind('<Leave>',
                        lambda event: self.mouseover_callback(False))
        scanning_widgets.append(name)
        #container1 = FixedSizeFrame(self.measurements_frame.interior, 198, 53)
        #container1.grid(row=value, column=4, sticky="NSE", pady=3)
        #prt_file = AutoScrollbarText(container1, state="disabled")
        #prt_file.grid(sticky="WENS")
        #scanning_vars.append(prt_file)
        #scanning_widgets.append(prt_file)
        container2 = FixedSizeFrame(self.measurements_frame.interior, 299, 53)
        container2.grid(row=value, column=4, sticky="NSE", pady=3, padx=2)
        scanning_widgets.append(container2)
        logfiles = AutoScrollbarText(container2, wrap=NONE, background=self.orange,
                                     highlightbackground=self.orange)
        logfiles.bind('<KeyRelease>', self.change_callback)
        logfiles.frame.bind('<Enter>',
                        lambda event: self.mouseover_callback(True))
        logfiles.frame.bind('<Leave>',
                        lambda event: self.mouseover_callback(False))
        scanning_vars.append(logfiles)  # Needs to be called with START, END!
        logfiles.grid()
        scanning_widgets.append(logfiles)
        container3 = FixedSizeFrame(self.measurements_frame.interior, 299, 53)
        container3.grid(row=value, column=5, sticky="NSE", pady=3, padx=(2, 10))
        scanning_widgets.append(container3)
        text = AutoScrollbarText(container3, wrap=NONE)
        text.bind('<KeyRelease>', self.change_callback)
        text.frame.bind('<Enter>',
                        lambda event: self.mouseover_callback(True))
        text.frame.bind('<Leave>',
                        lambda event: self.mouseover_callback(False))
        scanning_vars.append(text)  # Needs to be called with START, END!
        text.grid()
        scanning_widgets.append(text)
        self.measurements.append(scanning_vars)
        self.measurements_widgets.append(scanning_widgets)
        if int(value) >= 6:
            self.measurements_frame.bind_mouse_wheel()
        else:
            self.measurements_frame.unbind_mouse_wheel()
        self.change_callback(str(var2))  # Update Names
        self.prt_files.append("")

    def del_measurement(self, *args):
        for s in self.measurements_widgets[-1]:
            s.grid_remove()
            del s
        self.measurements_widgets.pop()
        self.measurements.pop()
        self.change_callback(None)

    def add_additional_documents(self):
        current_project = self.general_widgets[0].get()
        try:
            for x in self.config[current_project]["Checklist"]:
                if not x in self.documents:
                    var = IntVar()
                    var.trace("w", self.change_callback)
                    check = Checkbutton(self.documents_frame, text=x, variable=var)
                    check.grid(sticky="W", padx=10)
                    self.documents.append(x)
                    self.documents_vars.append(var)
                    self.additional_documents.append(x)
                    self.additional_documents_vars.append(var)
                    self.additional_documents_widgets.append(check)
        except:
            pass

    def add_files(self):
        current_project = self.general_widgets[0].get()
        try:
            for x in self.config[current_project]["Files"]:
                if not x in self.files.get(1.0, END).strip("\n"):        
                    self.files.insert(END, x + '\n')  
        except:
            pass

    def del_additional_documents(self):
        self.general_widgets[1][1].set_completion_list([])
        self.general_widgets[2][1].set_completion_list([])
        self.general_widgets[6].set_completion_list([])
        self.general_widgets[7].set_completion_list([])
        self.files.delete(1.0, END)
        for index, m in enumerate(self.measurements_widgets):
            t = self.measurements[index][1].get()
            m[3].set_completion_list([])
        for w in self.additional_documents_widgets:
            w.grid_remove()
        for v in self.additional_documents_vars:
            try:
                self.documents_vars.remove(v)
            except:
                pass
        for x in self.additional_documents:
            try:
                self.documents.remove(x)
            except:
                pass
        self.additional_documents_vars = []
        self.additional_documents_widgets = []

    def autofill_date_callback(self, *args):
        date = time.strftime("%Y-%m-%d", time.localtime())
        self.general_vars[3].set(date)

    def mouseover_callback(self, mouseover):
        if len(self.measurements) >= 6:
            if mouseover:
                self.measurements_frame.unbind_mouse_wheel()
            else:
                self.measurements_frame.bind_mouse_wheel()

    def validate(self, allowed_chars, allowed_length, current_char,
                 resulting_string):
        if current_char in allowed_chars:
            if len(resulting_string) <= int(allowed_length):
                return True
            else:
                return False
        else:
            return False

    def enable_save(self):
        self.save_button["state"] = "enabled"
        self.file_menu.entryconfigure("Save", state="normal")
        if platform.system() == "Darwin":
            self.master.bind("<Command-s>", self.save)
        else:
            self.master.bind("<Control-s>", self.save)

    def disable_save(self):
        self.save_button["state"] = "disabled"
        self.file_menu.entryconfigure("Save", state="disabled")
        if platform.system() == "Darwin":
            self.master.unbind("<Command-s>")
        else:
            self.master.unbind("<Control-s>")

    def enable_archive(self):
        self.go_button["state"] = "enabled"
        self.file_menu.entryconfigure("Archive", state="normal")
        if platform.system() == "Darwin":
            self.master.bind("<Command-r>", self.archive)
        else:
            self.master.bind("<Control-r>", self.archive)

    def disable_archive(self):
        self.go_button["state"] = "disabled"
        self.file_menu.entryconfigure("Archive", state="disabled")
        if platform.system() == "Darwin":
            self.master.unbind("<Command-r>")
        else:
            self.master.unbind("<Control-r>")

    def enable_minus(self):
        self.scanning_del["state"] = "enabled"
        self.edit_menu.entryconfigure("Delete Measurement", state="normal")
        if platform.system() == "Darwin":
            self.master.bind("<Command-d>", self.del_measurement)
        else:
            self.master.bind("<Control-d>", self.del_measurement)

    def disable_minus(self):
        self.scanning_del["state"] = "disabled"
        self.edit_menu.entryconfigure("Delete Measurement", state="disabled")
        if platform.system() == "Darwin":
            self.master.unbind("<Command-d>")
        else:
            self.master.unbind("<Control-d>")

    def quit_callback(self, *args):
        if self.save_button["state"] == "enabled":
            if tkMessageBox.askyesno("Save?", "Save before quitting?"):
                self.save()
        self.master.destroy()

    def change_callback(self, *args):
        try:
            self.enable_save()
        except:
            pass

        current_project = self.general_vars[0].get()

        # Update project
        if args[0] == str(self.general_vars[0]):
            self.del_additional_documents()
            try:
                if self.config[current_project]["SubjectTypes"] is not None:
                    self.general_widgets[1][1].set_completion_list(
                        self.config[current_project]["SubjectTypes"])
            except:
                pass
            try:
                if self.config[current_project]["SessionTypes"] is not None:
                    self.general_widgets[2][1].set_completion_list(
                        self.config[current_project]["SessionTypes"])
            except:
                pass
            try:
                if self.config[current_project]["Users"] is not None:
                    self.general_widgets[6].set_completion_list(
                        self.config[current_project]["Users"])
            except:
                pass
            try:
                if self.config[current_project]["Backups"] is not None:
                    self.general_widgets[7].set_completion_list(
                        self.config[current_project]["Backups"])
            except:
                pass
            for index, m in enumerate(self.measurements_widgets):
                try:
                    t = self.measurements[index][1].get()
                    m[3].set_completion_list(
                        [x["Name"] for x in self.config[current_project]["Measurements " + t]])
                except:
                    pass
            self.add_additional_documents()
            self.add_files()
            
            # Update notes
            if current_project != "":
                try:
                    notes = self.config[current_project]["Notes"]
                    if notes is not None:
                        self.general_widgets[-1].delete(1.0, END)
                        self.general_widgets[-1].insert(END, notes)
                except:
                    pass

        # Check if archving is possible
        try:
            if current_project != "" and \
                            self.general_vars[0].get() != "" and \
                            self.general_vars[3].get()!= "":
                self.enable_archive()
            else:
                self.disable_archive()
        except:
            pass

        # Check if deleting measurement is possible
        try:
            if len(self.measurements) > 1 and \
                self.measurements[-1][2].get() == "" and \
                self.measurements[-1][3].get() == "" and \
                self.measurements_widgets[-1][5].get(
                        1.0, END).strip("\n") == "" and \
                self.measurements_widgets[-1][-1].get(
                        1.0, END).strip("\n") == "":
                self.enable_minus()
            else:
                self.disable_minus()
        except:
            pass

        # Adapt Measurement Names according to Type
        types = [str(x[1]) for x in self.measurements]
        try:
            idx = types.index(args[0])
        except:
            idx = None
        if idx is not None and current_project != "":
            try:
                t = self.measurements[idx][1].get()
                self.measurements_widgets[idx][3].set_completion_list(
                    [x["Name"] for x in self.config[current_project]["Measurements " + t]])
            except:
                pass

        # Adapt Vols, Protocol and Comments according to Measurement Name
        names = [str(x[3]) for x in self.measurements]
        try:
            idx = names.index(args[0])
        except:
            idx = None
        if idx is not None and current_project != "":
            try:
                t = self.measurements[idx][1].get()
                n = self.measurements[idx][3].get()
                if n != "":
                    try:
                        id = [name for name in self.config[current_project]["Measurements " + t] if name["Name"] == n]
                        try:
                            vols = id[0]["Vols"]
                            if vols is not None:
                                self.measurements[idx][2].set(vols)
                        except:
                            pass
                        try:
                            comments = id[0]["Comments"]
                            if comments is not None:
                                self.measurements_widgets[idx][-1].delete(1.0, END)
                                self.measurements_widgets[idx][-1].insert(END, comments)
                        except:
                            pass
                    except:
                        pass
                    if t != "anatomical":
                        e = "*"

                        prt = "_".join(self.get_filename().split("_")[1:4]) + \
                            "_" + n + "." + e
                        if prt != self.prt_files[idx]:
                            if self.prt_files[idx] == "":
                                start = 1.0
                            elif self.prt_files[idx] != "":
                                start = self.measurements[idx][4].search(self.prt_files[idx], 1.0,
                                                    stopindex=END)
                                end = ".".join([start.split(".")[0],
                                            repr(len(self.prt_files[idx]))])
                                self.measurements[idx][4].delete(start, end)
                            self.measurements[idx][4].insert(start, prt)
                            self.prt_files[idx] = prt
                    
            except:
                pass

    def load_config(self):
        """Load the config file."""

        path = None
        if os.path.exists("sst.yaml"):
            path = os.path.curdir
        elif os.path.exists(os.path.join(os.path.expanduser("~"), "sst.yaml")):
            path = os.path.expanduser("~")
        else:
            path = None
        if path is not None:
            with open(os.path.join(path, "sst.yaml")) as f:
                self.config = yaml.safe_load(f)

                # for line in f:
                #     if line.startswith("Project:"):
                #         project = line[8:].strip()
                #         self.config[project] = {"groups": [],
                #                                 "sessions": [],
                #                                 "users": [],
                #                                 "backups": [],
                #                                 "info": "",
                #                                 "measurements": {
                #                                     "anatomical": {
                #                                         "names": [],
                #                                         "comment": ""},
                #                                     "functional": {
                #                                         "names": [],
                #                                         "comment": ""},
                #                                     "misc": {
                #                                         "names": [],
                #                                         "comment": ""}},
                #                                 "documents": []}
                #     elif line.startswith("Groups:"):
                #         self.config[project]['groups'] = \
                #             [x.strip() for x in line[7:].strip().split(",")]
                #         self.config[project]["groups"].sort()
                #     elif line.startswith("Sessions:"):
                #         self.config[project]["sessions"] = \
                #             [x.strip() for x in line[9:].strip().split(",")]
                #         self.config[project]["sessions"].sort()
                #     elif line.startswith("Users:"):
                #         self.config[project]["users"] = \
                #             [x.strip() for x in line[6:].strip().split(",")]
                #         self.config[project]["users"].sort()
                #     elif line.startswith("Backups:"):
                #         self.config[project]["backups"] = \
                #             [x.strip() for x in line[8:].strip().split(",")]
                #         self.config[project]["backups"].sort()
                #     elif line.startswith("Measurements Anatomical:"):
                #         self.config[project]["measurements"]["anatomical"]["names"] = \
                #             [x.strip() for x in line[24:].strip().split(",")]
                #         self.config[project]["measurements"]["anatomical"]["names"].sort()
                #         self.config[project]["measurements"]["anatomical"]["comment"] = line[9:].strip()
                #     elif line.startswith("Measurements Functional:"):
                #         self.config[project]["measurements"]["functional"]["names"] = \
                #             [x.strip() for x in line[24:].strip().split(",")]
                #         self.config[project]["measurements"]["functional"]["names"].sort()
                #         self.config[project]["measurements"]["functional"]["comment"] = line[9:].strip()
                #     elif line.startswith("Measurements Incomplete:"):
                #         self.config[project]["measurements"]["misc"]["names"] = \
                #             [x.strip() for x in line[24:].strip().split(",")]
                #         self.config[project]["measurements"]["misc"]["names"].sort()
                #         self.config[project]["measurements"]["misc"]["comment"] = line[9:].strip()
                #     elif line.startswith("Documents:"):
                #         self.config[project]["documents"] = \
                #             [x.strip() for x in line[10:].strip().split(",")]

    def get_filename(self):
        proj = self.general_vars[0].get()
        if proj == "":
            proj = "Project" 
        subj_nr = self.general_vars[1][0].get()
        subj = "sub-" + repr(int(subj_nr)).zfill(3)
        subj_type = self.general_vars[1][1].get()
        if subj_type != "":
            subj = "{0}-{1}".format(subj, subj_type)
        ses_nr = self.general_vars[2][0].get()
        ses = "ses-" + repr(int(ses_nr)).zfill(3)
        ses_type = self.general_vars[2][1].get()
        if ses_type != "":
            ses = "{0}-{1}".format(ses, ses_type)
        date = self.general_vars[3].get()
        if date == "":
            date = "Date"
        else:
            date = "".join(date.split("-"))
        filename = "ScanProtocol_{0}_{1}_{2}_{3}".format(proj, subj, ses,
                                                         date)
        return filename

    def save(self, filename=None, *args):
        """Save the data."""

        if filename is None:
            filename = self.get_filename()
            f = tkFileDialog.asksaveasfile(mode='w', defaultextension='.txt',
                                           initialfile=filename)
        else:
            f = open(filename, 'w')
        if f is None:
            return
        f.write("General Information\n")
        f.write("===================\n")
        f.write("\n")
        for pos, label in enumerate(self.general):
            if pos in (1,2):
                try:
                    value1 = self.general_vars[pos][0].get().zfill(3)
                    value2 = " " + self.general_vars[pos][1].get()
                except:
                    value1 = "000"
                    value2 = ""
                f.write("{0}{1}{2}\n".format(label, " "*(24-len(label)),
                                             value1 + value2))
            else:
                try:
                    value = self.general_vars[pos].get()
                except:
                    value = ""
                f.write("{0}{1}{2}\n".format(label, " "*(24-len(label)),
                                             value))

        f.write("\nNotes:")
        notes = self.general_widgets[-1].get(1.0, END).split("\n")
        notes_lines = [x.strip() for x in notes]
        try:
            for line_nr, line in enumerate(notes_lines):
                if line_nr == 0:
                    f.write("{0}{1}".format(" "*(24-len("Notes:")), line))
                else:
                    f.write("\n{0}{1}".format(" "*24, line))
        except:
            pass
        f.write("\n")
        f.write("\n")
        f.write("\n")
        f.write("Documents\n")
        f.write("=========\n")

        f.write("\nFiles:")
        files = self.files.get(1.0, END).split("\n")
        file_lines = [x.strip() for x in files if x != ""] 
        try:
            for line_nr, line in enumerate(file_lines):
                if line_nr == 0:
                    f.write("{0}{1}".format(" "*(24-len("Files:")), line))
                else:
                    f.write("\n{0}{1}".format(" "*24, line))
        except:
            pass

        f.write("\n\nChecklist:")
        states = ("[ ]", "[x]")
        for pos, label in enumerate(self.documents):
            try:
                value = int(self.documents_vars[pos].get())
            except:
                value = 0
            if pos == 0:
                f.write("{0}{1} {2}".format(" "*(24-len("Checklist:")), 
                                            states[value], label))
            else:
                f.write("\n{0}{1} {2}".format(" "*24, states[value], label))

        f.write("\n")
        f.write("\n")
        f.write("\n")
        f.write("Measurements\n")
        f.write("============")
        f.write("\n")
        for m in self.measurements:
            f.write("\nNo. {0}\n".format(int(m[0].get())))
            f.write("-----\n\n")
            for elem in range(1, len(self.measurement)-1):
                if elem == 4:
                    try:
                        logfiles = m[elem].get(1.0, END).split("\n")
                        logfile_lines = [x.strip() for x in logfiles if x != ""]
                        l = [" "*23 + x if index > 0 \
                                 else x for index, x in enumerate(logfile_lines)]
                        value = "\n".join(l)
                    except:
                        value = ""
                else:
                    try:
                        value = m[elem].get()
                    except:
                        value = ""
                f.write("{0}:{1}{2}\n".format(
                    self.measurement[elem],
                    " "*(23-len(self.measurement[elem])),
                    value))

            f.write("\nComments:")
            
            comments = m[-1].get(1.0, END).split("\n")
            comment_lines = [x.strip() for x in comments if x != ""] 
            try:
                for line_nr, line in enumerate(comment_lines):
                    if line_nr == 0:
                        f.write("{0}{1}".format(" "*(24-len("Comments:")), line))
                    else:
                        f.write("\n{0}{1}".format(" "*24, line))
            except:
                pass
            f.write("\n\n")
        f.close()
        self.disable_save()

    def open(self, *args):
        """Load data."""

        f = tkFileDialog.askopenfile("r", filetypes=[("text files", ".txt")])
        if f is not None:
            current_document = 0
            measurement = False
            measurement_starts = []
            notes_block = False
            comments_block = False
            files_block = False
            if len(self.measurements) == 0:
                self.new_measurement()
            while len(self.measurements) > 1:
                self.del_measurement()
            for m in self.measurements:
                m[-1].delete(1.0, END)
            for linenr, line in enumerate(f):
                if 3 <= linenr <= 10:
                    if linenr in (4,5):
                        self.general_vars[linenr-3][0].set((line[24:27]))
                        self.general_vars[linenr-3][1].set(line[28:].strip())
                    else:
                        self.general_vars[linenr-3].set(line[24:].strip())
                    if linenr == 3:
                        self.del_additional_documents()
                elif not measurement:
                    if line.startswith("Notes:"):
                        notes_block = True
                        self.general_widgets[-1].delete(1.0, END)
                    if line.startswith("Files:"):
                        files_block = True
                        self.files.delete(1.0, END)
                    if line.startswith("Checklist:"):
                        files_block = False
                    if notes_block:
                        if line.startswith("Documents"):
                            notes_block = False
                        else:
                            if self.general_widgets[-1].get(1.0, END).strip("\n") == "":
                                self.general_widgets[-1].insert(END,
                                                                line[24:].strip())
                            else:
                                self.general_widgets[-1].insert(END,
                                                                "\n" + line[24:].strip())
                    elif files_block:
                        if self.files.get(1.0, END).strip("\n") == "":
                            self.files.insert(END, line[24:].strip())
                        else:
                            self.files.insert(END, "\n" + line[24:].strip())
                    elif line.startswith("Measurements"):
                        measurement = True
                    else:
                        try:
                            #self.add_additional_documents()
                            check = line[25]
                            if check == " ":
                                value = 0
                            elif check == "x":
                                value = 1

                            x = line[27:].strip()
                            if line[24:].startswith("[") and not x in self.documents:
                                var = IntVar()
                                var.trace("w", self.change_callback)
                                check = Checkbutton(self.documents_frame, text=x, variable=var)
                                check.grid(sticky="W", padx=10)
                                self.documents.append(x)
                                self.documents_vars.append(var)
                                self.additional_documents.append(x)
                                self.additional_documents_vars.append(var)
                                self.additional_documents_widgets.append(check)

                            self.documents_vars[current_document].set(value)
                            current_document += 1
                        except:
                            pass

                elif measurement:
                    if line.startswith("===") or line.strip() == "":
                        pass
                    elif line.startswith("No. "):
                        if measurement_starts != []:
                            self.new_measurement()
                        self.measurements[len(measurement_starts)][0].set(
                            line[4:].strip().zfill(3))
                        measurement_starts.append(linenr)
                        comments_block = False
                    elif linenr >= measurement_starts[-1]+3:
                        if line.startswith("Type:") or\
                                line.startswith("Vols:") or\
                                line.startswith("Name:"):
                            self.measurements[
                                len(measurement_starts)-
                                1][linenr-measurement_starts[-1]-
                                   2].set(line[24:].strip())
                        elif line.startswith("Logfiles:"):
                            widget = self.measurements[
                                len(measurement_starts)-
                                1][-2]
                            widget.delete(1.0, END)
                            widget.insert(END, line[24:].strip())
                        elif line.startswith(" " * 24) and comments_block == False:
                            widget = self.measurements[
                                len(measurement_starts)-
                                1][-2]
                            widget.insert(END, "\n" + line[24:].strip())
                    if line.startswith("Comments:"):
                        if comments_block is False:
                            comments_block = True
                            self.measurements[len(measurement_starts)-
                                              1][-1].delete(1.0, END)
                        
                    if comments_block:
                        if self.measurements[len(measurement_starts)-
                                1][-1].get( 1.0, END).strip("\n") == "":
                            self.measurements[len(measurement_starts)-
                                              1][-1].insert(END,
                                                            line[24:].strip())
                        else:
                            self.measurements[len(measurement_starts)-
                                              1][-1].insert(END,
                                                            "\n" + line[24:].strip())
                
            self.disable_save()

    def set_title(self, status=None):
        if status is None:
            self.master.title('Scan Session Tool {0}'.format(__version__))
        else:
            self.master.title('Scan Session Tool {0} ({1})'.format(
                __version__, status))

    def _archive_run(self, d, dialogue):
        warnings = "\n\n\n"
        project = self.general_vars[0].get()
        subject_no = int(self.general_vars[1][0].get())
        subject_type = self.general_vars[1][1].get()
        session_no = int(self.general_vars[2][0].get())
        session_type = self.general_vars[2][1].get()
        timestamp = time.strftime("%Y%m%d%H%M%S", time.localtime())
        folder = os.path.join(d, "~Archive"+timestamp)
        if not os.path.exists(folder):
            try:
                os.makedirs(folder)
            except:
                warnings += "\nError creating project directory\n"
        for measurement in self.measurements:
            number = int(measurement[0].get())
            type = measurement[1].get()
            try:
                vols = int(measurement[2].get())
            except:
                vols = 0
            name = measurement[3].get()
            scans = []
            
            try:
                for subfolder in os.listdir(d):
                    if os.path.isdir(os.path.join(d, subfolder)) and "-" in subfolder and\
                    int(subfolder.split("-")[0]) == number:
                        for image in glob.glob(os.path.join(d, subfolder, "*.dcm")):
                            if int(os.path.split(image)[-1].split("_")[1]) == number:
                                scans.append(image)
                        if len(scans) == 0:
                            for image in glob.glob(os.path.join(d, subfolder, "*.IMA")):
                                if int(os.path.split(image)[-1].split(".")[3]) == number:
                                    scans.append(image)
                                elif len(os.path.split(image)[-1].split(".")) > 11:
                                    if int(os.path.split(image)[-1].split(".")[-11]) == number:
                                        scans.append(image)
            except:
                pass    

            if len(scans) == 0:
                try:
                    for image in glob.glob(os.path.join(d, "*.dcm")):
                        if int(os.path.split(image)[-1].split("_")[1]) == number:
                            scans.append(image)
                    if len(scans) == 0:
                        for image in glob.glob(os.path.join(d, "*.IMA")):
                            if int(os.path.split(image)[-1].split(".")[3]) == number:
                                scans.append(image)
                            elif len(os.path.split(image)[-1].split(".")) > 11:
                                if int(os.path.split(image)[-1].split(".")[-11]) == number:
                                    scans.append(image)
                except:
                    pass

            if name == "":
                warnings += "\nError copying images for measurement {0}:\n" \
                           "    'Name' not specified\n".format(number)
            if vols == 0:
                warnings += "\nError copying images for measurement {0}:\n" \
                           "    'Vols' not specified\n".format(number)
            elif scans == []:
                warnings += "\nError copying images for measurement {0}:\n" \
                            "    No images found\n".format(number)
            elif len(scans) != vols:
                warnings += "\nError copying images for measurement {0}:" \
                            "    'Vols' unequals number of images\n".format(number)
            else:
                try:
                    project_folder = os.path.join(folder, project)
                    if not os.path.exists(project_folder):
                        os.makedirs(project_folder)
                    #group_folder = os.path.join(project_folder, group)
                    #if not os.path.exists(group_folder):
                    #    os.makedirs(group_folder)
                    if subject_type == "":
                        subject_folder = os.path.join(project_folder,
                                                  "sub-" + repr(
                                                      subject_no).zfill(3))
                    else:
                        subject_folder = os.path.join(project_folder,
                                                  "sub-" + repr(
                                                      subject_no).zfill(3) + "-" + subject_type)
                    if not os.path.exists(subject_folder):
                        os.makedirs(subject_folder)
                    
                    if session_type == "":
                        session_folder = os.path.join(subject_folder, "ses-" + repr(session_no).zfill(3))
                    else:
                        session_folder = os.path.join(subject_folder, 
                                         "ses-" + repr(session_no).zfill(3) + "-" + session_type)

                    if not os.path.exists(session_folder):
                        os.makedirs(session_folder)
                    
                    type_folder = os.path.join(session_folder, type)
                    if not os.path.exists(type_folder):
                        os.makedirs(type_folder)
                    name_folder = os.path.join(type_folder, repr(number).zfill(3) + "-" + name)
                    if not os.path.exists(name_folder):
                        os.makedirs(name_folder)
                except:
                    warnings += "\nError creating directory structure for " \
                                "measurement {0}\n".format(number)
                    shutil.rmtree(dicom_folder)
                
                # DICOMs
                dialogue.status.set(
                "Archiving measurement {0} of {1}\n\n".format(
                   measurement[0].get(), len(self.measurements)) +
                "(Copying images...)")
                dialogue.update()
                try:
                    dicom_folder = os.path.join(name_folder, "DICOM")
                    if not os.path.exists(dicom_folder):
                        os.makedirs(dicom_folder)
                    for image in scans:
                        dialogue.update()
                        shutil.copyfile(
                            image, os.path.join(dicom_folder,
                                            os.path.split(image)[-1]))
                except:
                    warnings += "\nError copying images for measurement " \
                                "{0}:\n    Filesystem error\n".format(number)
                    shutil.rmtree(dicom_folder)
               

                #BV Files                       
                dialogue.status.set("(Copying BV files...)")
                dialogue.update() 
                try:
                    bv_folder = os.path.join(session_folder, "BV")
                    if not os.path.exists(bv_folder):
                        os.makedirs(bv_folder)
               
                    if type == "functional" or name == "Anatomy":
                        for image in os.listdir(dicom_folder):
                            if image.split(".")[-1] == "dcm":
                                target_name = "{}-{:04d}-0001-{:05d}.dcm".format(image.split("_")[0], 
                                                int(image.split("_")[1]), int(image.split("_")[2].split(".")[0]))  
                                os.link(os.path.join(dicom_folder, image) , os.path.join(bv_folder, target_name))
                            if image.split(".")[-1] == "IMA":
                                target_name = "{}-{:04d}-0001-{:05d}.dcm".format(image.split(".")[0], 
                                                int(image.split(".")[3]), int(image.split(".")[4]))  
                                os.link(os.path.join(dicom_folder, image) , os.path.join(bv_folder, target_name))
                except:
                    warnings += "\nError creating Brain Voyager links "


            # Logfiles
            if type != "anatomical":
                dialogue.status.set(
                       "Archiving measurement {0} of {1}\n\n".format(
                           measurement[0].get(), len(self.measurements)) +
                       "(Copying logfiles...)")
                dialogue.update()
                try:
                    warning = measurement[4].copy_logfiles(d, name_folder)
                    if warning != None:
                        warnings += warning
                
                except:
                    warnings += "\nError copying logfiles " \
                               "for measurement {0}\n".format(number)


        # TBV Files
        if os.path.isdir(os.path.join(d, "TBVFiles")):
            dialogue.status.set(
               "(Copying TBV files...)")
            dialogue.update()
            try:
                tbv_folder = os.path.join(session_folder, "TBV",)
                shutil.copytree(os.path.abspath(os.path.join(d, "TBVFiles")), 
                                os.path.abspath(os.path.join(tbv_folder, "TBVFiles")))
            except:
                warnings += "\nError copying Turbo Brain Voyager files "
                         
            # Create dcm links
            try:
                for filename in glob.glob(os.path.join(tbv_folder, "TBVFiles", "*.tbv")):
                    with open(filename) as f:
                        for line in f.readlines():
                            if line.startswith("DicomFirstVolumeNr"):
                                run_nr = line.split(" ")[-1]
                            
                    dcm_files = []
                    session_raw = os.path.join(session_folder, "functional")
                    
                    for run in os.listdir(session_raw):                        
                        if int(run.split("-")[0]) == int(run_nr):
                            source_folder = os.path.abspath(os.path.join(session_raw, run, "DICOM"))
                            for image in os.listdir(source_folder):
                                
                                if image.split(".")[-1] == "IMA" and int(image.split(".")[3]) == int(run_nr):
                                    target_name = "001_{:06d}_{:06d}.dcm".format(int(image.split(".")[3]),
                                                                             int(image.split(".")[4]))

                                if image.split(".")[-1] == "dcm" and int(image.split("_")[1]) == int(run_nr):
                                    target_name = "001_{:06d}_{:06d}.dcm".format(int(image.split("_")[1]),
                                                                             int(image.split("_")[2].split(".")[0]))
            
                                os.link(os.path.join(source_folder, image), os.path.join(tbv_folder, target_name))
            except:
                warnings += "\nError creating dcm links for Turbo Brain Voyager "


        #Session Files
        dialogue.status.set(
               "Archiving Files" +
               "(Copying Files...)")
        dialogue.update()
        try:
            warning = self.files.copy_logfiles(d, session_folder)
            if warning != None:
                warnings += warning
        except:
            warnings += "\nError copying Files "
                               
    
        # Try general documents
        dialogue.status.set("Archiving general documents\n\n(Copying...)")
        dialogue.update()
        try:
            all_documents = 0
            total_logs = []

            for measurement in self.measurements:
                original = measurement[4].get(1.0, END)
                logfiles = original.split("\n")
                logfiles = [x.strip() for x in logfiles if x != ""]
                total_logs.extend(logfiles)
            for file in glob.glob(os.path.join(d, "*")):
                if os.path.split(file)[-1] not in total_logs and \
                    os.path.splitext(file)[-1] in (".txt",
                                                   ".pdf",
                                                   ".odt"
                                                   ".doc",
                                                   ".docx"):
                    dialogue.update()
                    all_documents += 1
                    shutil.copy(os.path.abspath(file), session_folder)
            
            if all_documents == 0:
                warnings += "\nNo general documents found\n"
        except:
            warnings += "\nError copying general documents\n"

        dialogue.status.set("Done")
        dialogue.update()

        # Save scan protocol
        try:
            path = os.path.join(session_folder, self.get_filename() + ".txt")
            self.save(path)
        except:
            warnings += "\nError saving scan protocol\n"
        # Confirm archiving
        message = "Archived to: {0}".format(os.path.abspath(folder))
        message += warnings
        return message


    def archive(self, *args):
        """Archive the data."""

        d = tkFileDialog.askdirectory(
            title="Select directory containing all data")
        if d is not "":
            self.master.protocol("WM_DELETE_WINDOW", lambda x: None)
            self.set_title("Busy")
            dialogue = BusyDialogue(self.master)
            dialogue.status.set("Busy")
            dialogue.top.update()
            message = self._archive_run(d, dialogue)
            dialogue.destroy()
            self.set_title()
            self.master.protocol("WM_DELETE_WINDOW", app.quit_callback)
            #tkMessageBox.showinfo(title="Done", message=message)
            errors = MessageDialogue(self.master, message)
            errors.show()


class BusyDialogue:

    def __init__(self, master):
        self.master = master
        top = self.top = Toplevel(master)
        top.transient(master)
        top.grab_set()
        top.focus_set()
        top.protocol("WM_DELETE_WINDOW", lambda x: None)
        top.overrideredirect(1)
        style = Style()
        style.configure("Black.TFrame", background="#49d042")
        style.configure("White.TLabel", background="#49d042")
        self.frame = FixedSizeFrame(top, width=300, height=100,
                                    style="Black.TFrame")
        self.frame.grid()
        self.status = StringVar()
        self.label = Label(self.frame, textvariable=self.status,
                           style="White.TLabel", justify=CENTER)
        self.label['font'] = (app.default_font, app.default_font_size, "bold")
        self.label.grid(padx=10, pady=10)

        top.update_idletasks()
        dx = master.winfo_width() / 2 - top.winfo_width() / 2
        dy = master.winfo_height() / 2 - top.winfo_height() / 2
        top.geometry("+%d+%d" % (master.winfo_rootx() + dx,
                                 master.winfo_rooty() + dy))

    def update(self):
        self.top.update()

    def destroy(self):
        self.top.destroy()


class MessageDialogue:

    def __init__(self, master, message):
        self.master = master
        top = self.top = Toplevel(master, background="grey85")
        top.title("Archiving Report")
        top.transient(master)
        top.grab_set()
        top.focus_set()

        self.text = ScrolledText(top, width=77)
        self.text.pack()
        self.text.insert(END, message)
        self.text["state"] = "disabled"

        b = Button(top, text="OK", command=self.ok)
        b.pack(pady=10)

        #top.update_idletasks()
        #dx = master.winfo_width() / 2 - top.winfo_width() / 2
        #dy = master.winfo_height() / 2 - top.winfo_height() / 2
        #top.geometry("+%d+%d" % (master.winfo_rootx() + dx,
        #                         master.winfo_rooty() + dy))

    def show(self):
        self.master.wait_window(self.top)

    def ok(self):
        self.top.destroy()


class HelpDialogue:

    def __init__(self, master):
        self.master = master
        top = self.top = Toplevel(master, background="grey85")
        top.title("Help")
        self.text = ScrolledText(top, width=77)
        self.text.pack()
        self.text.insert(END, docs)
        self.text["state"] = "disabled"

        b = Button(top, text="OK", command=self.ok)
        b.pack(pady=5)

        #top.update_idletasks()
        #dx = master.winfo_width() / 2 - top.winfo_width() / 2
        #dy = master.winfo_height() / 2 - top.winfo_height() / 2
        #top.geometry("+%d+%d" % (master.winfo_rootx() + dx,
        #                         master.winfo_rooty() + dy))

    def ok(self):
        self.top.destroy()

    def show(self):
        self.master.wait_window(self.top)


if __name__ == "__main__":
    root = Tk()
    style = Style()
    style.theme_use("default")
    root.resizable(False, False)
    root.option_add('*tearOff', FALSE)
    app = App(master=root)
    app.set_title()
    if platform.system() == "Darwin":
        root.bind('<Command-q>', app.quit_callback)
    root.bind('<Escape>', lambda x: app.master.focus())
    app.bind('<Button-1>', lambda x: app.master.focus())
    for label in app.nofocus_widgets:
        label.bind('<Button-1>', lambda x: app.master.focus())
    root.protocol("WM_DELETE_WINDOW", app.quit_callback)
    app.general_widgets[0].focus()
    app.disable_save()
app.mainloop()
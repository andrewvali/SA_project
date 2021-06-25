from tkinter import *
from tkinter import ttk

import cv2
from PIL import Image, ImageTk
from queries import EventForShip, InterdictionArea, ProtectedArea, TrajectoryAndGap, CustomQuery
import tkinter.font as font
from explained_queries import *
from tkinter.messagebox import showinfo

class gui():
    def __init__(self):
        self.initialize()

    def initialize(self):

        self.root = Tk()
        self.root.geometry("600x500")

        self.root.title("Knowledge Base")

        choices = ('Event per vessel', 'Vessels in interdicted fishing area', 'Vessels in protected area',
                   'Vessel trajectory with highlighted Gap event')

        self.label = ttk.Label(text="Please select a query",font=font.BOLD)
        self.label.pack(fill='x', padx=5, pady=5, side=TOP)

        selected_choice=StringVar()
        self.choice_cb = ttk.Combobox(self.root, textvariable=selected_choice)
        self.choice_cb['values'] = choices
        self.choice_cb['state'] = 'readonly'
        self.choice_cb.pack(fill='x', padx=50, pady=5)
        self.choice_cb.bind('<<ComboboxSelected>>')

        self.query = Button(text="Submit", command=self.analysis, bg="white", fg="black", font=font.BOLD)
        self.query.pack(fill='x',padx=50,pady=5)
        img = cv2.imread("Immagine1.png")
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        height, width, _ = img.shape
        self.canvas = Canvas(self.root, width=width, height=height)
        self.canvas.pack(pady=40)
        photo = ImageTk.PhotoImage(master=self.canvas, image=Image.fromarray(img))
        self.canvas.create_image(0, 0, image=photo, anchor=NW)

        self.expert = Button(text="Custom Query", command=self.expert_mode, bg="white", fg="black", font=font.BOLD)

        self.expert.pack(fill='x',padx = 20, pady=30, side=RIGHT, ipadx=28)

        self.label2 = ttk.Label(text="...or write your query", font=font.BOLD)
        self.label2.pack(fill='x', padx=5, pady=5, side=RIGHT)


        self.root.mainloop()

    def expert_mode(self):


        self.gui = Tk()
        self.gui.geometry('700x500')
        self.gui.title("Query editor")
        scrollbar = Scrollbar(self.gui, orient=VERTICAL)
        scrollbar.pack(side="right", fill='y')
        self.text = Text(self.gui, yscrollcommand=scrollbar.set)

        prefixes = "@prefix geof: <http://www.opengis.net/def/function/geosparql/> .\n"
        prefixes += "@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n"
        prefixes += "@prefix strdf: <http://strdf.di.uoa.gr/ontology#> .\n@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n"
        prefixes += "@prefix ogc: <http://www.opengis.net/ont/geosparql#> .\n@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n"
        prefixes += "@prefix : <http://www.datacron-project.eu/ais_dataset#> .\n@prefix unit: <http://www.datacron-project.eu/unit#> ."
        prefixes += "\n\nSELECT COUNT(*) WHERE {?s ?p ?o}"

        self.text.insert("end", prefixes)
        close = Button(self.gui, text="Back", command=self.gui.destroy, bg="white", fg="black")
        close.pack(fill='x', pady=5, side=BOTTOM, ipadx=28)

        run = Button(self.gui, text="Run", command=self.custom_query, bg="white", fg="black")
        run.pack(fill='x', pady=5, side=BOTTOM, ipadx=28)

        self.text.pack(side="left", fill="y")

        scrollbar.config(command=self.text.yview)
        self.gui.mainloop()

    def custom_query(self):
        CustomQuery(self.text.get("1.0", "end-1c"))


    def analysis(self):
        self.choice = str(self.choice_cb.get())
        self.label2.destroy()
        self.canvas.destroy()
        self.query.destroy()
        self.expert.destroy()
        if self.choice == "Event per vessel":
            self.analysis_event_per_vessel()
        elif self.choice=='Vessels in interdicted fishing area':
            self.analysis_interdiction_area()
        elif self.choice == 'Vessels in protected area':
            self.analysis_protected_area()
        elif self.choice == 'Vessel trajectory with highlighted Gap event':
            self.analysis_traj_gap()

    def analysis_traj_gap(self):
        self.label.destroy()
        self.choice_cb.destroy()
        # self.event_cb.destroy()
        self.query.destroy()
        self.root.title("Analysis of vessels trajectory")
        self.label_vessel = ttk.Label(text="Write vessel code:", font=font.BOLD)
        self.label_vessel.pack(fill='x', padx=5, pady=5)
        vessel = StringVar()

        self.vesselEntry = Entry(textvariable=vessel)

        self.vesselEntry.pack(fill='x', padx=5, pady=5)

        self.query = Button(text="Run Query", command=self.run_query, bg="white", fg="black", font=font.BOLD)
        self.query.pack(fill='x', padx=5, pady=5)
        self.query = Button(text="Show Query", command=self.show_query, bg="white", fg="black", font=font.BOLD)
        self.query.pack(fill='x', padx=5, pady=5)
        self.button_back = Button(text="Back", command=self.back, bg="white", fg="black", font=font.BOLD)
        self.button_back.pack(fill='x', padx=5, pady=5)


    def analysis_protected_area(self):
        self.label.destroy()
        self.choice_cb.destroy()
        # self.event_cb.destroy()
        self.query.destroy()
        self.root.title("Analysis of vessels activity in a protected area")
        self.label_area = ttk.Label(text="Select protected area code:", font=font.BOLD)
        self.label_area.pack(fill='x', padx=5, pady=5)
        protected_area = ('natura_FR5302006', 'natura_FR5300019', 'natura_FR5300046', 'natura_FR5300020', 'natura_FR5302007', 'natura_FR5300021',
                         'natura_FR5300048', 'natura_FR5300031', 'natura_FR5300059', 'natura_FR5300027', 'natura_FR5300032', 'natura_FR5300024',
                          'natura_FR5300045', 'natura_FR5300017', 'natura_FR5300043', 'natura_FR5300009', 'natura_FR5300008')

        selected_choice_protected = StringVar()
        self.protected_area_cb = ttk.Combobox(self.root, textvariable=selected_choice_protected)
        self.protected_area_cb['values'] = protected_area
        self.protected_area_cb['state'] = 'readonly'
        self.protected_area_cb.pack(fill='x', padx=5, pady=5)
        self.protected_area_cb.bind('<<ComboboxSelected>>')

        self.label_vessel = ttk.Label(text="Write vessel code (write 'All' for every vessel): ", font=font.BOLD)
        self.label_vessel.pack(fill='x', padx=5, pady=5)

        vessel = StringVar()
        self.vesselEntry = Entry(textvariable=vessel)

        self.vesselEntry.pack(fill='x', padx=5, pady=5)


        self.label_event = ttk.Label(text="Select event code (select 'All' for every event): ", font=font.BOLD)
        self.label_event.pack(fill='x', padx=5, pady=5)
        event_choices = ('All','StoppedInit', 'StoppedEnd', 'HeadingChange', 'SpeedChangeStart', 'SpeedChangeEnd',
                  'SlowMotionStart', 'SlowMotionEnd', 'GapEnd')

        selected_choice = StringVar()
        self.event_choices_cb = ttk.Combobox(self.root, textvariable=selected_choice)
        self.event_choices_cb['values'] = event_choices
        self.event_choices_cb['state'] = 'readonly'
        self.event_choices_cb.pack(fill='x', padx=5, pady=5)
        self.event_choices_cb.bind('<<ComboboxSelected>>')

        self.query = Button(text="Run Query", command=self.run_query, bg="white", fg="black", font=font.BOLD)
        self.query.pack(fill='x', padx=5, pady=5)
        self.query = Button(text="Show Query", command=self.show_query, bg="white", fg="black", font=font.BOLD)
        self.query.pack(fill='x', padx=5, pady=5)
        self.button_back = Button(text="Back", command=self.back, bg="white", fg="black", font=font.BOLD)
        self.button_back.pack(fill='x', padx=5, pady=5)

    def analysis_interdiction_area(self):
        self.label.destroy()
        self.choice_cb.destroy()
        # self.event_cb.destroy()
        self.query.destroy()
        self.root.title("Analysis of vessels sopped in interdicted fishing area")
        self.label_vessel = ttk.Label(text="Write vessel code (write 'All' for every vessel): ", font=font.BOLD)
        self.label_vessel.pack(fill='x', padx=5, pady=5)
        vessel = StringVar()

        self.vesselEntry = Entry(textvariable=vessel)

        self.vesselEntry.pack(fill='x', padx=5, pady=5)

        self.query = Button(text="Run Query", command=self.run_query, bg="white", fg="black", font=font.BOLD)
        self.query.pack(fill='x', padx=5, pady=5)
        self.query = Button(text="Show Query", command=self.show_query, bg="white", fg="black", font=font.BOLD)
        self.query.pack(fill='x', padx=5, pady=5)
        self.button_back = Button(text="Back", command=self.back, bg="white", fg="black", font=font.BOLD)
        self.button_back.pack(fill='x', padx=5, pady=5)

    def analysis_event_per_vessel(self):

        self.choice = str(self.choice_cb.get())
        self.label.destroy()
        self.choice_cb.destroy()
        #self.event_cb.destroy()
        self.query.destroy()

        self.root.title("Analysis of Event per vessel")
        events = ('StoppedInit', 'StoppedEnd', 'HeadingChange', 'SpeedChangeStart', 'SpeedChangeEnd',
                  'SlowMotionStart', 'SlowMotionEnd', 'GapEnd')

        self.label_vessel = ttk.Label(text="Write vessel code (write 'All' for every vessel): ", font=font.BOLD)
        self.label_vessel.pack(fill='x', padx=5, pady=5)
        vessel = StringVar()

        self.vesselEntry = Entry(textvariable=vessel)

        self.vesselEntry.pack(fill='x', padx=5, pady=5)

        self.label_event_for_ship = ttk.Label(text="Please select an event of interest:", font=font.BOLD)
        self.label_event_for_ship.pack(fill='x', padx=5, pady=5)

        selected_event = StringVar()
        self.event_cb = ttk.Combobox(textvariable=selected_event)
        self.event_cb['values'] = events
        self.event_cb['state'] = 'readonly'
        self.event_cb.pack(fill='x', padx=5, pady=5)
        self.event_cb.bind('<<ComboboxSelected>>')

        self.query = Button(text="Run Query", command=self.run_query, bg="white", fg="black", font=font.BOLD)
        self.query.pack(fill='x', padx=5, pady=5)
        self.query = Button(text="Show Query", command=self.show_query, bg="white", fg="black", font=font.BOLD)
        self.query.pack(fill='x', padx=5, pady=5)
        self.button_back = Button(text="Back", command=self.back, bg="white", fg="black",font=font.BOLD)
        self.button_back.pack(fill='x', padx=5, pady=5)

    def show_query(self):
        query_window = Tk()
        query_window.title("Query")
        text = Text(query_window)
        if self.choice == 'Event per vessel':
            text.insert("end", EVENT_FOR_SHIP_QUERY)
        elif self.choice=='Vessels in interdicted fishing area':
            scrollbar = Scrollbar(query_window, orient=VERTICAL)
            scrollbar.pack(side="right", fill='y')
            text = Text(query_window, yscrollcommand=scrollbar.set)
            text.insert("end", QUERY_INTERDICTION_AREA)
            scrollbar.config(command=text.yview)
        elif self.choice=='Vessels in protected area':
            scrollbar = Scrollbar(query_window, orient=VERTICAL)
            scrollbar.pack(side="right", fill='y')
            text = Text(query_window, yscrollcommand=scrollbar.set)
            text.insert("end", PROTECTED_AREA_CONSTRUCT + PROTECTED_AREA_QUERY)
            scrollbar.config(command=text.yview)
        elif self.choice=='Vessel trajectory with highlighted Gap event':
            scrollbar = Scrollbar(query_window, orient=VERTICAL)
            scrollbar.pack(side="right", fill='y')
            text = Text(query_window, yscrollcommand=scrollbar.set)
            text.insert("end", TRAJ_GAP_QUERY_1+TRAJ_GAP_QUERY_2)
            scrollbar.config(command=text.yview)

        text.tag_config("explaination", foreground="blue")
        #text.tag_config("prefix", foreground="orange")
        self.text_search(text,"# EXPLAINATION:","explaination")
        #self.text_search(text, "@prefix", "prefix")
        text.configure(state=DISABLED)
        text.pack(side="left", fill="y")


    def text_search(self, text_widget, keyword, tag):
        pos = '1.0'
        while True:
            idx = text_widget.search(keyword, pos, END)
            if not idx:
                break
            pos = '{}+{}c'.format(idx, len(keyword))
            text_widget.tag_add(tag, idx, str(idx)+" lineend")

    def run_query(self):
        print(self.choice)
        if self.choice == 'Event per vessel':
            EventForShip(self.event_cb.get(),self.vesselEntry.get())
        elif self.choice=='Vessels in interdicted fishing area':
            InterdictionArea(self.vesselEntry.get())
        elif self.choice=='Vessels in protected area':
            ProtectedArea(self.protected_area_cb.get(),self.vesselEntry.get(),self.event_choices_cb.get())
        elif self.choice=='Vessel trajectory with highlighted Gap event':
            TrajectoryAndGap(self.vesselEntry.get())


    def back(self):
        self.root.destroy()
        self.initialize()

if __name__ == "__main__":
    gui()
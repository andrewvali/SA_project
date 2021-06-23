from tkinter import *
from tkinter import ttk

import cv2
from PIL import Image, ImageTk
from queries import EventForShip, InterdictionArea, ProtectedArea, TrajectoryAndGap, CustomQuery
import tkinter.font as font


class gui():
    def __init__(self):
        self.flag = False
        self.initialize()

    def initialize(self):

        self.root = Tk()
        self.root.geometry("600x500")

        self.root.title("Knowledge Base")

        choices = ('Event for ship', 'Interdiction Fishing Area', 'Protected Area',
                   'Trajectory with Gap')

        self.label = ttk.Label(text="Please select a choice:",font=font.BOLD)
        self.label.pack(fill='x', padx=5, pady=5, side=TOP)

        selected_choice=StringVar()
        self.choice_cb = ttk.Combobox(self.root, textvariable=selected_choice)
        self.choice_cb['values'] = choices
        self.choice_cb['state'] = 'readonly'
        self.choice_cb.pack(fill='x', padx=50, pady=5)
        self.choice_cb.bind('<<ComboboxSelected>>')

        self.query = Button(text="Submit", command=self.analysis, bg="green", fg="white", font=font.BOLD)
        self.query.pack(fill='x',padx=50,pady=5)

        img = cv2.imread("Immagine1.png")
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

        height,width, _ = img.shape
        self.canvas = Canvas(self.root, width=width, height=height)
        self.canvas.pack(pady=40)
        photo = ImageTk.PhotoImage(master=self.canvas, image=Image.fromarray(img))
        self.canvas.create_image(0, 0, image=photo, anchor=NW)
        print(self.flag)

        self.expert = Button(text="Expert", command=self.expert_mode, bg="blue", fg="white", font=font.BOLD)
        self.expert.pack(fill='x',padx = 20, pady=30, side=RIGHT, ipadx=28)



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
        close = Button(self.gui, text="Back", command=self.gui.destroy)
        close.pack(fill='x', pady=5, side=BOTTOM, ipadx=28)

        run = Button(self.gui, text="Run", command=self.custom_query)
        run.pack(fill='x', pady=5, side=BOTTOM, ipadx=28)

        self.text.pack(side="left", fill="y")

        scrollbar.config(command=self.text.yview)
        self.gui.mainloop()

    def custom_query(self):
        CustomQuery(self.text.get("1.0", "end-1c"))


    def analysis(self):
        self.choice = str(self.choice_cb.get())
        self.canvas.destroy()
        self.query.destroy()
        self.expert.destroy()
        if self.choice == "Event for ship":
            self.analysis_event_for_ship()
        elif self.choice=='Interdiction Fishing Area':
            self.analysis_interdiction_area()
        elif self.choice == 'Protected Area':
            self.analysis_protected_area()
        elif self.choice == 'Trajectory with Gap':
            self.analysis_traj_gap()

    def analysis_traj_gap(self):
        self.label.destroy()
        self.choice_cb.destroy()
        # self.event_cb.destroy()
        self.query.destroy()

        self.label_vessel = ttk.Label(text="Write vessel code:")
        self.label_vessel.pack(fill='x', padx=5, pady=5)
        vessel = StringVar()

        self.vesselEntry = Entry(textvariable=vessel)

        self.vesselEntry.pack(fill='x', padx=5, pady=5)

        self.query = Button(text="Run Query", command=self.run_query)
        self.query.pack(fill='x', padx=5, pady=5)
        self.button_back = Button(text="Back", command=self.back)
        self.button_back.pack(fill='x', padx=5, pady=5)


    def analysis_protected_area(self):
        self.label.destroy()
        self.choice_cb.destroy()
        # self.event_cb.destroy()
        self.query.destroy()

        self.label_area = ttk.Label(text="Write protected area code:", font=font.BOLD)
        self.label_area.pack(fill='x', padx=5, pady=5)
        protected_area = StringVar()

        self.protectedAreaEntry = Entry(textvariable=protected_area)

        self.protectedAreaEntry.pack(fill='x', padx=5, pady=5)
        self.label_vessel = ttk.Label(text="Write vessel code:", font=font.BOLD)
        self.label_vessel.pack(fill='x', padx=5, pady=5)

        vessel = StringVar()
        self.vesselEntry = Entry(textvariable=vessel)

        self.vesselEntry.pack(fill='x', padx=5, pady=5)

        self.label_event = ttk.Label(text="Write event code:", font=font.BOLD)
        self.label_event.pack(fill='x', padx=5, pady=5)

        event = StringVar()
        self.eventEntry = Entry(textvariable=event)

        self.eventEntry.pack(fill='x', padx=5, pady=5)

        self.query = Button(text="Run Query", command=self.run_query)
        self.query.pack(fill='x', padx=5, pady=5)
        self.button_back = Button(text="Back", command=self.back)
        self.button_back.pack(fill='x', padx=5, pady=5)

    def analysis_interdiction_area(self):
        self.label.destroy()
        self.choice_cb.destroy()
        # self.event_cb.destroy()
        self.query.destroy()

        self.label_vessel = ttk.Label(text="Write vessel code:")
        self.label_vessel.pack(fill='x', padx=5, pady=5)
        vessel = StringVar()

        self.vesselEntry = Entry(textvariable=vessel)

        self.vesselEntry.pack(fill='x', padx=5, pady=5)

        self.query = Button(text="Run Query", command=self.run_query)
        self.query.pack(fill='x', padx=5, pady=5)
        self.button_back = Button(text="Back", command=self.back)
        self.button_back.pack(fill='x', padx=5, pady=5)

    def analysis_event_for_ship(self):

        self.choice = str(self.choice_cb.get())
        self.label.destroy()
        self.choice_cb.destroy()
        #self.event_cb.destroy()
        self.query.destroy()

        self.root.title("Analysis of Event for ship")
        events = ('GapEnd', 'HeadingChange', 'StoppedInit', 'SpeedChangeStart', 'SlowMotionEnd',
                  'SpeedChangeEnd', 'StoppedEnd', 'SlowMotionStart', 'fishing_area')

        self.label_vessel = ttk.Label(text="Write vessel code:", font=font.BOLD)
        self.label_vessel.pack(fill='x', padx=5, pady=5)
        vessel = StringVar()

        self.vesselEntry = Entry(textvariable=vessel)

        self.vesselEntry.pack(fill='x', padx=5, pady=5)

        self.label_event_for_ship = ttk.Label(text="Please select an event:")
        self.label_event_for_ship.pack(fill='x', padx=5, pady=5)

        selected_event = StringVar()
        self.event_cb = ttk.Combobox(textvariable=selected_event)
        self.event_cb['values'] = events
        self.event_cb['state'] = 'readonly'
        self.event_cb.pack(fill='x', padx=5, pady=5)
        self.event_cb.bind('<<ComboboxSelected>>')

        self.query = Button(text="Run Query", command=self.run_query, bg="green", fg="white", font=font.BOLD)
        self.query.pack(fill='x', padx=5, pady=5)
        self.button_back = Button(text="Back", command=self.back, bg="black", fg="white",font=font.BOLD)
        self.button_back.pack(fill='x', padx=5, pady=5)

    def run_query(self):
        print(self.choice)
        if self.choice == 'Event for ship':
            EventForShip(self.event_cb.get(),self.vesselEntry.get())
        elif self.choice=='Interdiction Fishing Area':
            InterdictionArea(self.vesselEntry.get())
        elif self.choice=='Protected Area':
            ProtectedArea(self.protectedAreaEntry.get(),self.vesselEntry.get(),self.eventEntry.get())
        elif self.choice=='Trajectory with Gap':
            TrajectoryAndGap(self.vesselEntry.get())


    def back(self):
        self.root.destroy()
        self.initialize()

if __name__ == "__main__":
    gui()
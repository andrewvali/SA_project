from tkinter import *
from tkinter import ttk
from SPARQLWrapper import SPARQLWrapper, JSON
from tkinter.messagebox import showinfo

from construct_handler import ConstructQuery
from pltMap import pltMap
from PIL import Image, ImageTk
from math import *
from explained_queries import *

# IP SERVER
IP_PORT = "79.35.17.201:8890"

class CustomQuery():
    def __init__(self,query):
        self.query= query
        self.run_query()

    def run_query(self):

        sparql = SPARQLWrapper("http://" + IP_PORT + "/sparql/")
        sparql.setQuery(self.query)
        sparql.setReturnFormat(JSON)
        result = sparql.query().convert()
        triples = result["results"]["bindings"]
        t = result["head"]["vars"]
        self.res = ""
        for triple in triples:
            msg = ""
            for i in t:
                msg += " " + str(triple[i]["value"]).split("/")[-1].split("#")[-1]
            self.res += msg + "\n"

        self.gui_result()


    def gui_result(self):
        self.gui = Tk()
        # self.gui.geometry('700x500')
        self.gui.title("Results of query ")
        scrollbar = Scrollbar(self.gui, orient=VERTICAL)
        scrollbar.pack(side="right", fill='y')
        text = Text(self.gui, yscrollcommand=scrollbar.set)
        text.insert("end", self.res)
        text.pack(side="left", fill="y")

        scrollbar.config(command=text.yview)
        self.gui.mainloop()



class EventForShip():
    def __init__(self,event,vessel):
        self.event = str(event)
        self.vessel = str(vessel)
        self.run_query()

    def run_query(self):
        if self.event != "" and self.vessel != "":
            if self.vessel == "All":
                ves = "?vessel"
            else:
                ves = ":" + self.vessel
            sparql = SPARQLWrapper("http://"+IP_PORT+"/sparql/")

            self.query = EVENT_FOR_SHIP_QUERY.replace("[EVENT]",":"+self.event).replace("[VESSEL]",ves)

            '''self.query= """@prefix geof: <http://www.opengis.net/def/function/geosparql/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix strdf: <http://strdf.di.uoa.gr/ontology#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix ogc: <http://www.opengis.net/ont/geosparql#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix : <http://www.datacron-project.eu/ais_dataset#> .
@prefix unit: <http://www.datacron-project.eu/unit#> .

SELECT DISTINCT ?vessel ?event (COUNT(?event) as ?num_event)
WHERE{
?event :occurs ?node.
?node :ofMovingObject ?vessel
FILTER(?event = :""" + self.event + """ && ?vessel = """ + ves + """)
}GROUP BY ?vessel ?event HAVING(COUNT(?event)>2)
ORDER BY DESC(?num_event)"""
            '''

            sparql.setQuery(self.query)

            sparql.setReturnFormat(JSON)
            result = sparql.query().convert()
            triples = result["results"]["bindings"]
            t = result["head"]["vars"]
            self.res = ""
            for triple in triples:
                msg = ""
                for i in t:
                    msg += " " + str(triple[i]["value"]).split("/")[-1].split("#")[-1]
                self.res += msg + "\n"

            self.gui_result()
        else:
            showinfo('Warning!', 'Complete all fields! ')

    def gui_result(self):
        self.gui = Tk()
        #self.gui.geometry('700x500')
        self.gui.title("Results of events: " +self.vessel)
        scrollbar = Scrollbar(self.gui, orient=VERTICAL)
        scrollbar.pack(side="right", fill='y')
        text = Text(self.gui, yscrollcommand=scrollbar.set)
        text.insert("end", self.res)
        show_query = Button(self.gui, text="Show Query", command=self.show_query)
        show_query.pack(fill='x', padx=5, pady=5, side=BOTTOM)
        text.pack(side="left", fill="y")

        scrollbar.config(command=text.yview)
        self.gui.mainloop()

    def show_query(self):
        def event_button():
            query_window.destroy()
            self.gui_result()

        self.gui.destroy()
        query_window = Tk()
        query_window.title("Query")
        text = Text(query_window)
        text.insert("end", self.query)
        btn = Button(query_window, text="Back", command=event_button)
        btn.pack(fill='x', padx=5, pady=5, side=BOTTOM)
        text.pack(side="left", fill="y")


class InterdictionArea():

    def __init__(self,vessel):
        self.vessel = str(vessel)
        #self.map = pltMap(XMIN, YMIN, XMAX, YMAX)
        self.run_query()

    def run_query(self):
        if self.vessel != "":
            if self.vessel == "All":
                ves = "?vessel"
            else:
                ves = ":" + self.vessel
            sparql = SPARQLWrapper("http://"+IP_PORT+"/sparql/")
            #sparql.setTimeout(30)

            self.query = QUERY_INTERDICTION_AREA.replace("[VESSEL]", ves)

            '''    self.query = """
            @prefix geof: <http://www.opengis.net/def/function/geosparql/> .
            @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
            @prefix strdf: <http://strdf.di.uoa.gr/ontology#> .
            @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
            @prefix ogc: <http://www.opengis.net/ont/geosparql#> .
            @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
            @prefix : <http://www.datacron-project.eu/ais_dataset#> .
            @prefix unit: <http://www.datacron-project.eu/unit#> .
                            
            SELECT DISTINCT ?vessel ?tstart ?point
            WHERE{
            
            ?area a :Fishing_Interdiction_area.
            
            :StoppedInit :occurs ?obj.
            ?obj :ofMovingObject ?vessel.
            ?obj :hasTemporalFeature ?timestamp_start.
            ?timestamp_start :TimeStart ?tstart.
            
            ?area :hasGeometry ?geom2 .
            ?geom2 ogc:asWKT ?zone .
            
            ?obj :hasGeometry ?geom .
            ?geom ogc:asWKT ?point .
            
            
            FILTER (geof:sfWithin(?point, ?zone) && ?vessel = """+ves+""")
            } LIMIT 10""" '''

            sparql.setQuery(self.query)

            sparql.setReturnFormat(JSON)
            result = sparql.query().convert()
            triples = result["results"]["bindings"]
            t = result["head"]["vars"]
            self.res = ""
            #points = []
            for triple in triples:
                msg = ""
                for i in t:
                    msg += " " + str(triple[i]["value"]).split("/")[-1].split("#")[-1]
                #points.append([float(coord) for coord in msg.split(";")[-1].split("(")[-1].split(")")[0].split(" ")])
                self.res += msg + "\n"


            self.gui_result()
        else:
            showinfo('Warning!', 'Complete all fields! ')

    def gui_result(self):
        self.gui = Tk()
        #self.gui.geometry('700x500')
        self.gui.title("Results of events: " +self.vessel)
        scrollbar = Scrollbar(self.gui, orient=VERTICAL)
        scrollbar.pack(side="right", fill='y')
        text = Text(self.gui, yscrollcommand=scrollbar.set)
        text.insert("end", self.res)
        show_query = Button(self.gui, text="Show Query", command=self.show_query)
        show_query.pack(fill='x', padx=5, pady=5, side=BOTTOM)
        text.pack(side="left", fill="y")

        scrollbar.config(command=text.yview)
        self.gui.mainloop()

    def show_query(self):
        def event_button():
            query_window.destroy()
            self.gui_result()

        self.gui.destroy()
        query_window = Tk()
        query_window.title("Query")
        text = Text(query_window)
        text.insert("end", self.query)
        btn = Button(query_window, text="Back", command=event_button)
        btn.pack(fill='x', padx=5, pady=5, side=BOTTOM)
        text.pack(side="left", fill="y")

class ProtectedArea():
    def __init__(self,protected_area_code,vessel,event):
        self.protectedArea = str(protected_area_code)
        #self.map = pltMap(XMIN, YMIN, XMAX, YMAX)
        self.vessel = str(vessel)
        self.event = str(event)
        self.run_query()

    def run_query(self):
        if self.protectedArea != "" and self.vessel!="" and self.event!="":
            if self.protectedArea == "All":
                area_code = "?area"
            else:
                area_code = ":" + self.protectedArea
            if self.vessel == "All":
                ves = "?vessel"
            else:
                ves = ":" + self.vessel
            if self.event=="All":
                eve = "?event"
            else:
                eve = ":" + self.event
            sparql = SPARQLWrapper("http://" + IP_PORT + "/sparql/")

            self.query_construct= PROTECTED_AREA_CONSTRUCT.replace("[AREA]",area_code)

            '''self.query_construct = """
@prefix geof: <http://www.opengis.net/def/function/geosparql/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix strdf: <http://strdf.di.uoa.gr/ontology#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix ogc: <http://www.opengis.net/ont/geosparql#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix : <http://www.datacron-project.eu/ais_dataset#> .
@prefix unit: <http://www.datacron-project.eu/unit#> .
CONSTRUCT {?vessel ?event ?date}
WHERE{
SELECT ?vessel ?event ?date 
WHERE {
?event :occurs ?obj .
?obj :ofMovingObject ?vessel .
?obj :hasGeometry ?geom1 .
?geom1 ogc:asWKT ?point .
?obj :hasTemporalFeature ?time.
?time a :Instant.
?time :TimeStart ?date.

?area a :Natura2000_zone .
?area :hasGeometry ?geom2 .
?geom2 ogc:asWKT ?zone .

FILTER(geof:sfWithin(?point ,?zone ) && ?area = """+area_code+""")
}
} LIMIT 10"""'''
            con = ConstructQuery('http://79.35.17.201:8890/DAV/provolone', 'http://79.35.17.201:8890/sparql/',
                                 'http://79.35.17.201:8890/sparql-auth/', 'operator',
                                 'operator')  # user #pw

            con.construct_initializer(self.query_construct)

            self.area_query = PROTECTED_AREA_QUERY.replace("[VESSEL]",ves).replace("[EVENT]",eve)


            result = con.construct_query(self.area_query)

            ''' result = con.construct_query(
              """
            @prefix geof: <http://www.opengis.net/def/function/geosparql/> .
            @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
            @prefix strdf: <http://strdf.di.uoa.gr/ontology#> .
            @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
            @prefix ogc: <http://www.opengis.net/ont/geosparql#> .
            @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
            @prefix : <http://www.datacron-project.eu/ais_dataset#> .
            @prefix unit: <http://www.datacron-project.eu/unit#> .            
            SELECT DISTINCT ?vessel ?event ?date 
            WHERE {
            ?vessel ?event ?date.
            FILTER(?vessel="""+ves+""" && ?event="""+eve+""").}""")'''

            print(result)
            triples = result["results"]["bindings"]
            #triples.sort(key=lambda x:x['o']['value'])
            t = result["head"]["vars"]
            self.res = ""
            for triple in triples:
                msg = ""
                for i in t:
                    print(msg)
                    msg += " " + str(triple[i]["value"]).split("/")[-1].split("#")[-1]

                self.res += msg + "\n"
            #self.res = self.res.replace("T"," ")

            self.gui_result()
        else:
            showinfo('Warning!', 'Complete all fields! ')

    def gui_result(self):
        self.gui = Tk()
        #self.gui.geometry('700x500')
        self.gui.title("Results of protected zone: " +self.protectedArea)
        scrollbar = Scrollbar(self.gui, orient=VERTICAL)
        scrollbar.pack(side="right", fill='y')
        text = Text(self.gui, yscrollcommand=scrollbar.set)
        text.insert("end", self.res)
        show_query = Button(self.gui, text="Show Query", command=self.show_query)
        show_query.pack(fill='x', padx=5, pady=5, side=BOTTOM)
        text.pack(side="left", fill="y")

        scrollbar.config(command=text.yview)
        self.gui.mainloop()

    def show_query(self):
        def event_button():
            query_window.destroy()
            self.gui_result()

        self.gui.destroy()
        query_window = Tk()
        query_window.title("Query")
        scrollbar = Scrollbar(query_window, orient=VERTICAL)
        scrollbar.pack(side="right", fill='y')
        text = Text(query_window,yscrollcommand=scrollbar.set)
        text.insert("end", self.query_construct+"\n"+self.area_query)
        btn = Button(query_window, text="Back", command=event_button)
        btn.pack(fill='x', padx=5, pady=5, side=BOTTOM)
        text.pack(side="left", fill="y")

# Geografic zone (default Brest and Northern Brittany)
XMIN = -8.26
YMIN = 44.9
XMAX = -0.4
YMAX = 49.9

class TrajectoryAndGap():

    def __init__(self, vessel):
        self.vessel = str(vessel)
        self.map = pltMap(XMIN, YMIN, XMAX, YMAX)
        self.run_query()

    def run_query(self):
        if self.vessel != "":
            if self.vessel == "All":
                ves = "?vessel"
            else:
                ves = ":" + self.vessel
            sparql = SPARQLWrapper("http://" + IP_PORT + "/sparql/")
            '''  sparql.setQuery("""
            @prefix geof: <http://www.opengis.net/def/function/geosparql/> .
            @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
            @prefix strdf: <http://strdf.di.uoa.gr/ontology#> .
            @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
            @prefix ogc: <http://www.opengis.net/ont/geosparql#> .
            @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
            @prefix : <http://www.datacron-project.eu/ais_dataset#> .
            @prefix unit: <http://www.datacron-project.eu/unit#> .
            
            SELECT DISTINCT ?port_point ?instance_port ?name
            WHERE{
            
            ?port a ?instance_port .
            ?port :hasPlaceName ?name.
            ?port :hasGeometry ?geom1 .
            ?geom1 ogc:asWKT ?port_point
            FILTER (?instance_port = :Port || ?instance_port = :FishingPort).
            }""")'''
            sparql.setQuery(TRAJ_GAP_QUERY_1)

            sparql.setReturnFormat(JSON)
            result = sparql.query().convert()
            triples = result["results"]["bindings"]
            t = result["head"]["vars"]
            result = ""
            points = []
            mydict = {}
            for triple in triples:
                msg = ""
                for i in t:
                    msg += " " + str(triple[i]["value"]).split("/")[-1].split("#")[-1]
                    c = msg.split("(")
                    c = c[1].split(" ")
                    points.append((float(c[0]), float(c[1][:-1])))
                # points.append([float(coord) for coord in msg.split(";")[-1].split("(")[-1].split(")")[0].split(" ")])

                result += msg + "\n"

            # print(points)

            # points = np.array(points)

            self.query = TRAJ_GAP_QUERY_2.replace("[VESSEL]", ves)

            '''self.query = """
            @prefix geof: <http://www.opengis.net/def/function/geosparql/> .
            @prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
            @prefix strdf: <http://strdf.di.uoa.gr/ontology#> .
            @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
            @prefix ogc: <http://www.opengis.net/ont/geosparql#> .
            @prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
            @prefix : <http://www.datacron-project.eu/ais_dataset#> .
            @prefix unit: <http://www.datacron-project.eu/unit#> .
            
            SELECT DISTINCT ?time ?timestamp ?point
            WHERE{
            ?node :ofMovingObject ?vessel .
            ?node :hasTemporalFeature ?time.
            ?time :TimeStart ?timestamp .
            
            ?node :hasGeometry ?geom .
            ?geom ogc:asWKT ?point .
            FILTER (?vessel = """+ves+""").
            }
            ORDER BY ASC(?time)
            LIMIT 500"""'''

            sparql.setQuery(self.query)
            sparql.setReturnFormat(JSON)
            result = sparql.query().convert()
            triples = result["results"]["bindings"]
            t = result["head"]["vars"]
            self.result = ""
            self.points_vessel = []
            timestamp_vessel_point = []

            for triple in triples:
                msg = ""
                for i in t:
                    msg += " " + str(triple[i]["value"]).split("/")[-1].split("#")[-1]
                c = msg.split(" ")
                c = c[1].split("t")
                self.result += msg+"\n"

                timestamp_vessel_point.append(int(c[1]))
                self.points_vessel.append(
                    [float(coord) for coord in msg.split(";")[-1].split("(")[-1].split(")")[0].split(" ")])

            # points_vessel =np.array(points_vessel)

            R = 6373.0
            dist = []
            self.gap_points = []
            k = 0
            for i in range(0, len(timestamp_vessel_point) - 1):
                for p in points:
                    lat1 = radians(self.points_vessel[i][0])
                    lon1 = radians(self.points_vessel[i][1])
                    lat2 = radians(p[0])
                    lon2 = radians(p[1])
                    dlon = lon2 - lon1
                    dlat = lat2 - lat1
                    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
                    c = 2 * atan2(sqrt(a), sqrt(1 - a))
                    dist.append(R * c)

                if min(dist) < 2 and abs(timestamp_vessel_point[i] - timestamp_vessel_point[i + 1]) >= 500000:
                    print(self.points_vessel[i], points[dist.index(min(dist))])
                    print("NO Event Gap")

                elif min(dist) > 2 and abs(timestamp_vessel_point[i] - timestamp_vessel_point[i + 1]) >= 500000:
                    print("YES Event Gap")
                    self.gap_points.append(self.points_vessel[i])
                    self.gap_points.append(self.points_vessel[i + 1])

            self.show_map()

        else:
            showinfo('Warning!', 'Complete all fields! ')

    def gui_result(self):
        def event_button():
            self.gui.destroy()
            self.show_map()
        self.gui = Tk()
        self.gui.geometry('700x500')
        self.gui.title("Result Trajectory Points")
        scrollbar = Scrollbar(self.gui, orient=VERTICAL)
        scrollbar.pack(side="right", fill='y')
        text = Text(self.gui, yscrollcommand=scrollbar.set)
        text.insert("end", self.result)
        traj = Button(self.gui, text="Back", command=event_button)
        traj.pack(fill='x', padx=5, pady=5, side=BOTTOM)
        text.pack(side="left", fill="y")

        scrollbar.config(command=text.yview)
        self.gui.mainloop()

    def gui_result_query(self):
        def event_button():
            self.gui.destroy()
            self.show_map()
        self.gui = Tk()
        self.gui.geometry('700x500')
        self.gui.title("Result Gap Event")
        scrollbar = Scrollbar(self.gui, orient=VERTICAL)
        scrollbar.pack(side="right", fill='y')
        text = Text(self.gui, yscrollcommand=scrollbar.set)
        text.insert("end", TRAJ_GAP_QUERY_1+"\n"+self.query)
        traj = Button(self.gui, text="Back", command=event_button)
        traj.pack(fill='x', padx=5, pady=5, side=BOTTOM)
        text.pack(side="left", fill="y")

        scrollbar.config(command=text.yview)
        self.gui.mainloop()
    def show_map(self):
        def event_button():
            self.map = pltMap(XMIN, YMIN, XMAX, YMAX)
            window.destroy()
            self.gui_result()

        def event_button_query():
            self.map = pltMap(XMIN, YMIN, XMAX, YMAX)
            window.destroy()
            self.gui_result_query()

        try:
            self.gui.destroy()
        except:
            pass
        img = self.map.plot_gap_points_with_traj(points=self.points_vessel, gap_points=self.gap_points)
        height, width, no_channels = img.shape
        window = Tk()
        window.title("Trajectory")
        canvas = Canvas(window, width=width, height=height)
        canvas.pack()
        photo = ImageTk.PhotoImage(master=canvas, image=Image.fromarray(img))
        canvas.create_image(0, 0, image=photo, anchor=NW)

        btn_show_points = Button(window, text="Show Points", command=event_button)
        btn_show_points.pack(fill='x', padx=5, pady=5, side=BOTTOM)

        btn = Button(window, text="Show Query", command=event_button_query)
        btn.pack(fill='x', padx=5, pady=5, side=BOTTOM)



        window.mainloop()


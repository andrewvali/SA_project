from tkinter import *
from tkinter import ttk
from SPARQLWrapper import SPARQLWrapper, JSON
from tkinter.messagebox import showinfo

from construct_handler import ConstructQuery
from pltMap import pltMap
from PIL import Image, ImageTk
from math import *
from explained_queries import *
import os
import csv
import datetime

# IP SERVER
with open('Address Settings.txt') as f:
    IP_PORT = f.readlines()[0]
f.close()
if IP_PORT is None:
    print("Insert an address in Address Settings.txt")
    exit(1)


PATH_VESSEL_CODE = "dataset_vessel_type\\nari_static.csv"
PATH_VESSEL_TYPE = "dataset_vessel_type\\vessel_type.CSV"

"""
This dict will be formed by:

KEY = Vessel MMSI
Value = Type code 
"""
my_dict = {}

with open(os.path.abspath(PATH_VESSEL_CODE) ,mode="r") as csv_file:
    csv_reader = csv.reader((csv_file), delimiter=",")
    for row in csv_reader:
        my_dict[row[0]] = row[4]

"""
This dict will be formed by:

KEY = Type code 
Value = Type description 
"""

my_dict2 = {}

with open(os.path.abspath(PATH_VESSEL_TYPE) ,mode="r") as csv_file2:
    csv_reader2 = csv.reader((csv_file2), delimiter=";")

    for row2 in csv_reader2:
        my_dict2[row2[0]] = row2[1]

class CustomQuery():
    """
    This class is invoked when user wants to launch a custom query
    """
    def __init__(self,query):
        """
        :param query: query written by user
        """
        self.query= query
        self.run_query()

    def run_query(self):
        """
        This function is called to launch the query, to acquire the query result and
        to call gui_result function to show the result
        """
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
        """
        This function is called to show the query result. It implements a new window to show result.
        """
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
    """
    This class is invoked to run event per vessel query
    """
    def __init__(self,event,vessel, datetime_start, datetime_end):
        """
        :param event: event to analize chosen by user
        :param vessel: vessel to analize chosen by user
        :param datetime_start: start date chosen by user
        :param datetime_end: end date chosen by user
        """
        if str(event) != "" and str(datetime_start)!="" and str(datetime_end)!="":
            if check_parameters(datetime_start,datetime_end,vessel):
                self.event = str(event)
                self.vessel = str(vessel)
                self.datetime_start=datetime_convert(datetime_start)
                self.datetime_end = datetime_convert(datetime_end)
                self.run_query()
        else:
            showinfo('Warning!', 'Complete all fields! ')


    def run_query(self):
        """
        This function is called to run the query. It replaces the parameters chosen by user in the basic query.
        The query result is obtained by server and it calls the gui_result function to show the result.
        """

        if self.vessel == "All":
            ves = "?vessel"
        else:
            ves = ":ves" + self.vessel
        if self.event=="All":
            self.event="?event"
        else:
            self.event=":"+self.event
        print(self.event)
        sparql = SPARQLWrapper("http://"+IP_PORT+"/sparql/")

        self.query = EVENT_FOR_SHIP_QUERY.replace("[EVENT]",self.event).replace("[VESSEL]",ves)
        self.query = self.query.replace("[DATE_START]",self.datetime_start).replace("[DATE_END]",self.datetime_end)

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
            msg = msg.split(" ")
            try:
                self.res += "VESSEL MMSI: "+msg[1][3:]+" TYPE: "+my_dict2[my_dict[msg[1][3:]]]+"\n" +" EVENT: "+msg[2]+" OCCURENCES: "+msg[3]+ "\n" +"\n"
            except:
                self.res += "VESSEL MMSI: "+msg[1][3:]+"\n"+"TYPE: not found"+" EVENT: "+msg[2]+" OCCURENCES: "+msg[3]+ "\n"+"\n"

        self.gui_result()

    def gui_result(self):
        """
        This function is called to show the query result. It implements a new window to show the result
        """
        self.gui = Tk()
        #self.gui.geometry('700x500')
        self.gui.title("Result of event per vessel: " +self.vessel)
        scrollbar = Scrollbar(self.gui, orient=VERTICAL)
        scrollbar.pack(side="right", fill='y')
        text = Text(self.gui, yscrollcommand=scrollbar.set)
        if self.res!="":
            text.insert("end", "TIME INTERVAL: " + self.datetime_start[1:17].replace("T", " ") +
                        " / " + self.datetime_end[1:17].replace("T", " ") + "\n" + "\n" + self.res)

            text.tag_config("time_interval", foreground="blue")
            # text.tag_config("prefix", foreground="orange")
            text_search(text, "TIME INTERVAL:", "time_interval", True)

            text.tag_config("vessel_mmsi", foreground="blue")
            # text.tag_config("prefix", foreground="orange")
            text_search(text, "VESSEL MMSI:", "vessel_mmsi",True)

            text.tag_config("type", foreground="blue")
            # text.tag_config("prefix", foreground="orange")
            text_search(text, "TYPE:", "type", True)

            text.tag_config("event", foreground="blue")
            # text.tag_config("prefix", foreground="orange")
            text_search(text, "EVENT:", "event",True)


            text.tag_config("occurences", foreground="blue")
            # text.tag_config("prefix", foreground="orange")
            text_search(text, "OCCURENCES:", "occurences", True)
        else:
            text.insert("end",
                        "There is no result for the requested query!" + "\n" + "\n" + "Try change the parameters you choose.")

            text.tag_config("error", foreground="red")
            # text.tag_config("prefix", foreground="orange")
            text_search(text, "There", "error")
        text.configure(state=DISABLED)
        show_query = Button(self.gui, text="Show Query", bg = "deep sky blue",fg="black", command=self.show_query)
        show_query.pack(fill='x', padx=5, pady=5, side=BOTTOM)
        text.pack(side="left", fill="y")

        scrollbar.config(command=text.yview)
        self.gui.mainloop()

    def show_query(self):
        """
        This function is called when user click on "Show Query" button from result window.
        It shows the query launched.
        """
        def event_button():
            query_window.destroy()
            self.gui_result()

        self.gui.destroy()
        query_window = Tk()
        query_window.title("Query of event per vessel")
        text = Text(query_window)
        text.insert("end", self.query)
        text.tag_config("explaination", foreground="blue")
        # text.tag_config("prefix", foreground="orange")
        text_search(text, "# EXPLAINATION:", "explaination")
        text.configure(state=DISABLED)
        btn = Button(query_window, text="Back", command=event_button)
        btn.pack(fill='x', padx=5, pady=5, side=BOTTOM)
        text.pack(side="left", fill="y")


class InterdictionArea():
    """
    This class is invoked to run vessels stopped in a fishing interdicted area query
    """

    def __init__(self,vessel, datetime_start, datetime_end):
        """
        :param vessel: vessel to analize chosen by user
        :param datetime_start: start date chosen by user
        :param datetime_end: end date chosen by user
        """
        if str(vessel)!="" and str(datetime_start)!="" and str(datetime_end)!="":
            if check_parameters(datetime_start,datetime_end,vessel):
                self.vessel = str(vessel)
                self.datetime_start = datetime_convert(datetime_start)
                self.datetime_end = datetime_convert(datetime_end)
                self.run_query()
        else:
            showinfo('Warning!', 'Complete all fields! ')

    def run_query(self):
        """
        This function is called to run the query. It replaces the parameters chosen by user in the basic query.
        The query result is obtained by server and it calls the gui_result function to show the result.
        """

        if self.vessel == "All":
            ves = "?vessel"
        else:
            ves = ":ves" + self.vessel
        sparql = SPARQLWrapper("http://"+IP_PORT+"/sparql/")
        #sparql.setTimeout(30)

        self.query = QUERY_INTERDICTION_AREA.replace("[VESSEL]", ves)
        self.query = self.query.replace("[DATE_START]",self.datetime_start).replace("[DATE_END]",self.datetime_end)
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
            msg = msg.replace("T"," ")
            msg = msg.replace("POIN","POINT:")
            msg = msg.replace("SRID=4322;","")
            msg = msg.split(" ")
            try:
                self.res += "VESSEL MMSI: "+ msg[1][3:]+" TYPE: "+my_dict2[my_dict[msg[1][3:]]]+"\n"+" DATE and TIME: "+msg[2]+" "+msg[3]+" "+msg[4]+" "+msg[5]+ " "+msg[6]+"\n" +"\n"
            except:
                self.res += "VESSEL MMSI: " + msg[1][3:] + " TYPE: not found" + "\n" + " DATE and TIME: " + \
                            msg[2] + " " + msg[3] + " " + msg[4] + " " + msg[5] + " "+msg[6]+ "\n" + "\n"
        self.gui_result()

    def gui_result(self):
        """
        This function is called to show the query result. It implements a new window to show the result.
        """
        self.gui = Tk()
        #self.gui.geometry('700x500')
        self.gui.title("Result of events in an interdicted fishing area. MMSI: " +self.vessel)
        scrollbar = Scrollbar(self.gui, orient=VERTICAL)
        scrollbar.pack(side="right", fill='y')
        text = Text(self.gui, yscrollcommand=scrollbar.set)
        if self.res!="":

            text.insert("end", "TIME INTERVAL: "+self.datetime_start[1:17].replace("T"," ")+
                        " / "+self.datetime_end[1:17].replace("T"," ")+"\n"+"\n"+self.res)

            text.tag_config("time_interval", foreground="blue")
            # text.tag_config("prefix", foreground="orange")
            text_search(text, "TIME INTERVAL:", "time_interval", True)
            text.tag_config("vessel", foreground="blue")
            # text.tag_config("prefix", foreground="orange")
            text_search(text, "VESSEL MMSI:", "vessel", True)

            text.tag_config("type", foreground="blue")
            # text.tag_config("prefix", foreground="orange")
            text_search(text, "TYPE:", "type", True)

            text.tag_config("date_and_time", foreground="blue")
            # text.tag_config("prefix", foreground="orange")
            text_search(text, "DATE and TIME:", "date_and_time", True)

            text.tag_config("point", foreground="blue")
            # text.tag_config("prefix", foreground="orange")
            text_search(text, "POINT:", "point", True)
        else:
            text.insert("end",
                        "There is no result for the requested query!" + "\n" + "\n" + "Try change the parameters you choose.")

            text.tag_config("error", foreground="red")
            # text.tag_config("prefix", foreground="orange")
            text_search(text, "There", "error")

        text.configure(state=DISABLED)

        show_query = Button(self.gui, text="Show Query", bg="deep sky blue", fg="black", command=self.show_query)
        show_query.pack(fill='x', padx=5, pady=5, side=BOTTOM)
        text.pack(side="left", fill="y")

        scrollbar.config(command=text.yview)
        self.gui.mainloop()

    def show_query(self):
        """
        This function is called when user click on "Show Query" button from result window.
        It shows the query launched.
        """
        def event_button():
            query_window.destroy()
            self.gui_result()

        self.gui.destroy()
        query_window = Tk()
        query_window.title("Query")
        text = Text(query_window)
        text.insert("end", self.query)
        text.tag_config("explaination", foreground="blue")
        # text.tag_config("prefix", foreground="orange")
        text_search(text, "# EXPLAINATION:", "explaination")

        btn = Button(query_window, text="Back", command=event_button)
        btn.pack(fill='x', padx=5, pady=5, side=BOTTOM)
        text.pack(side="left", fill="y")

class ProtectedArea():
    """
    This class is invoked to run analysis in a protected area query
    """
    def __init__(self,protected_area_code,vessel,event,datetime_start, datetime_end):
        """
        :param protected_area_code: area code of Natura2000 chosen by user
        :param event: event to analize chosen by user
        :param vessel: vessel to analize chosen by user
        :param datetime_start: start date chosen by user
        :param datetime_end: end date chosen by user
        """
        if str(datetime_start)!="" and str(datetime_end) and str(vessel)!="":
            if check_parameters(datetime_start,datetime_end,vessel):
                self.protectedArea = str(protected_area_code)
                self.datetime_start = datetime_convert(datetime_start)
                self.datetime_end = datetime_convert(datetime_end)
                self.vessel = str(vessel)
                self.event = str(event)
                self.run_query()
        else:
            showinfo('Warning!', 'Complete all fields! ')

    def run_query(self):
        """
        This function is called to run the query. It replaces the parameters chosen by user in the basic query.
        The query result is obtained by server and it calls the gui_result function to show the result.
        It is launched construct query and then another query on triples generated by construct
        """

        if self.protectedArea[:16] == "All":
            area_code = "?area"
        else:
            area_code = ":" + self.protectedArea[:16]
        if self.vessel == "All":
            ves = "?vessel"
        else:
            ves = ":ves" + self.vessel
        if self.event=="All":
            eve = "?event"
        else:
            eve = ":" + self.event
        sparql = SPARQLWrapper("http://" + IP_PORT + "/sparql/")

        self.query_construct= PROTECTED_AREA_CONSTRUCT.replace("[AREA]",area_code)

        con = ConstructQuery('http://'+IP_PORT+'/DAV/contructeDataset', 'http://'+IP_PORT+'/sparql/',
                             'http://'+IP_PORT+'/sparql-auth/', 'operator',
                             'operator')  # user #pw

        con.construct_initializer(self.query_construct)

        self.area_query = PROTECTED_AREA_QUERY.replace("[VESSEL]",ves).replace("[EVENT]",eve)

        self.area_query = self.area_query.replace("[DATE_START]",self.datetime_start).replace("[DATE_END]",self.datetime_end)
        result = con.construct_query(self.area_query)

        triples = result["results"]["bindings"]
        #triples.sort(key=lambda x:x['o']['value'])
        t = result["head"]["vars"]
        self.res = ""
        for triple in triples:
            msg = ""
            for i in t:
                print(msg)
                msg += " " + str(triple[i]["value"]).split("/")[-1].split("#")[-1]
            msg = msg.replace("T"," ")
            msg = msg.split(" ")

            try:
                self.res += "VESSEL MMSI: "+ msg[1][3:]+" TYPE: "+my_dict2[my_dict[msg[1][3:]]]+"\n"+" EVENT: "+msg[2]+" DATE and TIME: "+msg[3]+" " +msg[4]+ "\n"+"\n"
            except:
                self.res += "VESSEL MMSI: "+ msg[1][3:]+" TYPE: not found"+"\n"+" EVENT: "+msg[2]+" DATE and TIME: "+msg[3]+" " +msg[4]+ "\n"+"\n"

        #self.res = self.res.replace("T"," ")

        self.gui_result()

    def gui_result(self):
        """
        This function is called to show the query result. It implements a new window to show the result.
        """
        self.gui = Tk()
        #self.gui.geometry('700x500')
        self.gui.title("AREA: " +self.protectedArea[19:]
                       +" - MMSI: "+self.vessel+" - EVENT: "+self.event)
        scrollbar = Scrollbar(self.gui, orient=VERTICAL)
        scrollbar.pack(side="right", fill='y')
        text = Text(self.gui, yscrollcommand=scrollbar.set)
        if self.res!="":
            text.insert("end", "TIME INTERVAL: " + self.datetime_start[1:17].replace("T", " ") +
                        " / " + self.datetime_end[1:17].replace("T", " ") + "\n" + "\n" + self.res)

            text.tag_config("time_interval", foreground="blue")
            # text.tag_config("prefix", foreground="orange")
            text_search(text, "TIME INTERVAL:", "time_interval", True)

            text.tag_config("vessel", foreground="blue")
            # text.tag_config("prefix", foreground="orange")
            text_search(text, "VESSEL MMSI:", "vessel", True)

            text.tag_config("type", foreground="blue")
            # text.tag_config("prefix", foreground="orange")
            text_search(text, "TYPE:", "type", True)

            text.tag_config("event", foreground="blue")
            # text.tag_config("prefix", foreground="orange")
            text_search(text, "EVENT:", "event", True)

            text.tag_config("date_and_time", foreground="blue")
            # text.tag_config("prefix", foreground="orange")
            text_search(text, "DATE and TIME:", "date_and_time", True)
        else:
            text.insert("end", "There is no result for the requested query!"+"\n"+"\n"+"Try change the parameters you choose.")

            text.tag_config("error", foreground="red")
            # text.tag_config("prefix", foreground="orange")
            text_search(text, "There", "error")
        text.configure(state=DISABLED)
        show_query = Button(self.gui, text="Show Query", bg="deep sky blue", fg="black",command=self.show_query)
        show_query.pack(fill='x', padx=5, pady=5, side=BOTTOM)
        text.pack(side="left", fill="y")

        scrollbar.config(command=text.yview)
        self.gui.mainloop()

    def show_query(self):
        """
        This function is called when user click on "Show Query" button from result window.
        It shows the query launched.
        """
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
        text.tag_config("explaination", foreground="blue")
        # text.tag_config("prefix", foreground="orange")
        text_search(text, "# EXPLAINATION:", "explaination")
        text.configure(state=DISABLED)
        btn = Button(query_window, text="Back", command=event_button)
        btn.pack(fill='x', padx=5, pady=5, side=BOTTOM)
        scrollbar.config(command=text.yview)
        text.pack(side="left", fill="y")

# Geografic zone (default Brest and Northern Brittany)
XMIN = -8.26
YMIN = 44.9
XMAX = -0.4
YMAX = 49.9

class TrajectoryAndGap():
    """
    This class is invoked to run analysis of thrajectory and gap event query
    """
    def __init__(self, vessel,datetime_start,datetime_end):
        """
        :param vessel: vessel to analize chosen by user
        :param datetime_start: start date chosen by user
        :param datetime_end: end date chosen by user
        """
        if str(vessel)!="" and str(datetime_start)!="" and str(vessel)!="":
            if check_parameters(datetime_start, datetime_end, vessel):
                self.vessel = str(vessel)
                self.map = pltMap(XMIN, YMIN, XMAX, YMAX)
                self.datetime_start = datetime_convert(datetime_start)
                self.datetime_end = datetime_convert(datetime_end)
                self.run_query()
        else:
            showinfo('Warning!', 'Complete all fields! ')

    def run_query(self):
        """
        This function is called to run the query. It replaces the parameters chosen by user in the basic query.
        The query result is obtained by server and it calls the gui_result function to show the result.
        """

        if self.vessel == "All":
            ves = "?vessel"
        else:
            ves = ":ves" + self.vessel
        sparql = SPARQLWrapper("http://" + IP_PORT + "/sparql/")

        sparql.setQuery(TRAJ_GAP_QUERY_1)

        sparql.setReturnFormat(JSON)
        result = sparql.query().convert()
        triples = result["results"]["bindings"]
        t = result["head"]["vars"]
        result = ""

        # points list contains the position of all ports
        points = []

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
        self.query = self.query.replace("[DATE_START]", self.datetime_start)
        self.query = self.query.replace("[DATE_END]", self.datetime_end)

        sparql.setQuery(self.query)
        sparql.setReturnFormat(JSON)
        result = sparql.query().convert()
        triples = result["results"]["bindings"]
        t = result["head"]["vars"]
        self.result = ""

        # points_vessel contains all points of vessel trajectory
        self.points_vessel = []

        #timestamp_vessel_point contains the timestamp of each point
        timestamp_vessel_point = []

        for triple in triples:
            msg = ""
            for i in t:
                msg += " " + str(triple[i]["value"]).split("/")[-1].split("#")[-1]
            c = msg.split(" ")
            c = c[1].split("t")
            m = msg
            m = m.replace("T", " ")
            m = m.replace("POIN", "POINT:")
            m = m.replace("SRID=4322;", "")
            m = m.split(" ")
            self.result += "DATE and TIME: "+m[3]+" "+m[4]+" "+m[5]+" "+m[6]+"\n"

            timestamp_vessel_point.append(int(c[1]))
            self.points_vessel.append(
                [float(coord) for coord in msg.split(";")[-1].split("(")[-1].split(")")[0].split(" ")])


        R = 6373.0

        # This list contains all distance between vessel and nearest port
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

            # if the min distance is less than 5 km and more than half an hour has passed
            # between two successive communications, the gap event is not detected
            if min(dist) < 2 and abs(timestamp_vessel_point[i] - timestamp_vessel_point[i + 1]) >= 500000:
                print(self.points_vessel[i], points[dist.index(min(dist))])
                print("NO Event Gap")

            # if the min distance is greater than 5 km and more than half an hour has passed
            # between two successive communications, the gap event is detected
            elif min(dist) > 2 and abs(timestamp_vessel_point[i] - timestamp_vessel_point[i + 1]) >= 500000:
                print("YES Event Gap")
                self.gap_points.append(self.points_vessel[i])
                self.gap_points.append(self.points_vessel[i + 1])

        self.show_map()

    def gui_result(self):
        """
        This function is called to show the query result. It implements a new window to show the result.
        """
        def event_button():
            self.gui.destroy()
            self.show_map()
        self.gui = Tk()
        #self.gui.geometry('700x500')
        try:
            self.gui.title("Points Trajectory of vessel: "+self.vessel+" type: "+my_dict2[my_dict[self.vessel]])
        except:
            self.gui.title("Points Trajectory of vessel: " + self.vessel + " type: not found")
        scrollbar = Scrollbar(self.gui, orient=VERTICAL)
        scrollbar.pack(side="right", fill='y')
        text = Text(self.gui, yscrollcommand=scrollbar.set)
        text.insert("end", "TIME INTERVAL: " + self.datetime_start[1:17].replace("T", " ") +
                    " / " + self.datetime_end[1:17].replace("T", " ") + "\n" + "\n" + self.result)

        text.tag_config("time_interval", foreground="blue")
        # text.tag_config("prefix", foreground="orange")
        text_search(text, "TIME INTERVAL:", "time_interval", True)
        text.tag_config("point", foreground="blue")
        # text.tag_config("prefix", foreground="orange")
        text_search(text, "POINT:", "point", True)

        text.tag_config("date_and_time", foreground="blue")
        # text.tag_config("prefix", foreground="orange")
        text_search(text, "DATE and TIME:", "date_and_time", True)
        text.configure(state=DISABLED)
        traj = Button(self.gui, text="Back", bg="darkgray", fg="black",command=event_button)
        traj.pack(fill='x', padx=5, pady=5, side=BOTTOM)
        text.pack(side="left", fill="y")

        scrollbar.config(command=text.yview)
        self.gui.mainloop()

    def show_query(self):
        """
        This function is called when user click on "Show Query" button from result window.
        It shows the query launched.
        """
        def event_button():
            self.gui.destroy()
            self.show_map()
        self.gui = Tk()
        #self.gui.geometry('700x500')
        self.gui.title("Query of vessel trajectory with highlighted Gap event. MMSI: "+self.vessel)
        scrollbar = Scrollbar(self.gui, orient=VERTICAL)
        scrollbar.pack(side="right", fill='y')
        text = Text(self.gui, yscrollcommand=scrollbar.set)
        text.insert("end", TRAJ_GAP_QUERY_1+"\n"+self.query)
        text.tag_config("explaination", foreground="blue")
        # text.tag_config("prefix", foreground="orange")
        text_search(text, "# EXPLAINATION:", "explaination")
        text.configure(state=DISABLED)
        traj = Button(self.gui, text="Back", command=event_button)
        traj.pack(fill='x', padx=5, pady=5, side=BOTTOM)
        text.pack(side="left", fill="y")

        scrollbar.config(command=text.yview)
        self.gui.mainloop()

    def show_map(self):
        """
        This function is called to show the map with trajectory and Gap event
        """
        def event_button():
            self.map = pltMap(XMIN, YMIN, XMAX, YMAX)
            window.destroy()
            self.gui_result()

        def event_button_query():
            self.map = pltMap(XMIN, YMIN, XMAX, YMAX)
            window.destroy()
            self.show_query()

        try:
            self.gui.destroy()
        except:
            pass
        img = self.map.plot_gap_points_with_traj(points=self.points_vessel, gap_points=self.gap_points)
        height, width, no_channels = img.shape
        window = Tk()
        try:
            window.title("Trajectory. MMSI: "+self.vessel+" TYPE: "+my_dict2[my_dict[self.vessel]])
        except:
            window.title("Trajectory. MMSI: " + self.vessel + " TYPE: not found")
        canvas = Canvas(window, width=width, height=height)
        canvas.pack()
        photo = ImageTk.PhotoImage(master=canvas, image=Image.fromarray(img))
        canvas.create_image(0, 0, image=photo, anchor=NW)

        btn_show_points = Button(window, text="Show Points", command=event_button)
        btn_show_points.pack(fill='x', padx=5, pady=5, side=BOTTOM)

        btn = Button(window, text="Show Query", command=event_button_query)
        btn.pack(fill='x', padx=5, pady=5, side=BOTTOM)

        window.mainloop()

def text_search(text_widget, keyword, tag, flag=False):
    pos = '1.0'

    while True:
        idx = text_widget.search(keyword, pos, END)
        if not idx:
            break
        pos = '{}+{}c'.format(idx, len(keyword))
        if flag:
            s = pos
        else:
            s = str(idx) + " lineend"
        text_widget.tag_add(tag, idx, s)

def datetime_convert(datetime):
    """
    :param datetime: datetime chosen by user
    :return: corrected format of datetime to launch the query
    """
    datetime = str(datetime).replace(" ", "T")
    datetime = '"' + datetime + ":00" + '"' + "^^xsd:dateTime"
    print(datetime)
    return datetime

def check_parameters(datetime_start,datetime_end, vessel_mmsi):
    try:
        datetime.datetime.strptime(str(datetime_start), "%Y-%m-%d %H:%M")
    except:
        showinfo("Warning", "Start date incorrect form!")
        return False
    try:
        datetime.datetime.strptime(str(datetime_end), "%Y-%m-%d %H:%M")
    except:
        showinfo("Warning", "End date incorrect form!")
        return False

    if str(vessel_mmsi)!="All" and (len(str(vessel_mmsi))!=9 or not str(vessel_mmsi).isdigit()):
        showinfo("Warning", "Vessel MMSI incorrect form!")
        return False

    return True
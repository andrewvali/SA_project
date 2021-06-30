from http.server import HTTPServer, BaseHTTPRequestHandler
from explained_queries import *
import json
from SPARQLWrapper import SPARQLWrapper, JSON
from construct_handler import ConstructQuery

with open('Address Settings.txt') as f:
    IP_PORT = f.readlines()[0]
f.close()
if IP_PORT is None:
    print("Insert an address in Address Settings.txt")
    exit(1)

class HTTPRequestHandler(BaseHTTPRequestHandler):
    """
    This class is used to handle post requests server
    """
    def do_POST(self):
        """
        Function called once Post service has been called by client
        """

        #Getting user data
        content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
        data_string = self.rfile.read(content_length)  # <--- Gets the data itself

        #EXPECTING THIS FORMAT:
        # {type: WICH QUERY
        # query: {DICTIONARY WITH INPUTS}}

        json_data = json.loads(data_string.decode())
        print(str(json_data))

        # Handling queries, choosing between 3 different types of queries
        # If received data is not a correct JSON or needed input is not given
        # it returns to client and error message with 400 as code
        # If received data does not have an avialbel type it returns an error code
        # with 500 as code

        # Inside every if statement, code is similar to the one used in gui mode
        try:
            res = {}
            if json_data["type"] == "event per ship":
                event = json_data["query"]["event"]
                vessel = json_data["query"]["vessel"]
                datetime_start = json_data["query"]["date1"]
                datetime_end = json_data["query"]["date2"]

                if event == "" or vessel == "" or datetime_start == "" or datetime_end == "":
                    raise KeyError

                datetime_start = self.datetime_from_html_to_sparql(datetime_start)
                datetime_end = self.datetime_from_html_to_sparql(datetime_end)

                if vessel.lower() == "all":
                    ves = "?vessel"
                else:
                    ves = ":" + vessel

                query = EVENT_FOR_SHIP_QUERY.replace("[EVENT]", ":" + event).replace("[VESSEL]", ves).\
                    replace("[DATE_START]", datetime_start).replace("[DATE_END]", datetime_end)

                res = self.do_query(query)

            elif json_data["type"] == "interdiction area":
                vessel = json_data["query"]["vessel"]
                datetime_start = json_data["query"]["date1"]
                datetime_end = json_data["query"]["date2"]

                if vessel == "" or datetime_start == "" or datetime_end == "":
                    raise KeyError

                datetime_start = self.datetime_from_html_to_sparql(datetime_start)
                datetime_end = self.datetime_from_html_to_sparql(datetime_end)

                if vessel.lower() == "all":
                    ves = "?vessel"
                else:
                    ves = ":" + vessel

                query = QUERY_INTERDICTION_AREA.replace("[VESSEL]", ves).\
                    replace("[DATE_START]", datetime_start).replace("[DATE_END]", datetime_end)

                res = self.do_query(query)

            elif json_data["type"] == "protected area":
                protectedArea = json_data["query"]["protectedArea"]
                event = json_data["query"]["event"]
                vessel = json_data["query"]["vessel"]
                datetime_start = json_data["query"]["date1"]
                datetime_end = json_data["query"]["date2"]

                if protectedArea == "" or vessel=="" or event == "" or datetime_start == "" or datetime_end == "":
                    raise KeyError

                area_code = ":" + protectedArea

                datetime_start = self.datetime_from_html_to_sparql(datetime_start)
                datetime_end = self.datetime_from_html_to_sparql(datetime_end)

                if vessel.lower() == "all":
                    ves = "?vessel"
                else:
                    ves = ":" + vessel
                if event.lower() == "all":
                    eve = "?event"
                else:
                    eve = ":" + event

                query_construct = PROTECTED_AREA_CONSTRUCT.replace("[AREA]", area_code)

                con = ConstructQuery('http://'+IP_PORT+'/DAV/provolone', 'http://'+IP_PORT+'/sparql/',
                                     'http://'+IP_PORT+'/sparql-auth/', 'operator',
                                     'operator')  # user #pw

                con.construct_initializer(query_construct)

                area_query = PROTECTED_AREA_QUERY.replace("[VESSEL]", ves).replace("[EVENT]", eve).\
                    replace("[DATE_START]", datetime_start).replace("[DATE_END]", datetime_end)

                result = con.construct_query(area_query)

                res = self.dict_from_query_result(result)
            else:
                res = None


            if res is None:
                print("NO QUERY AVAILABLE")
                self.send_response(500)
                to_send = {"received": "error, query type not available"}
            else:
                print("SENT BACK " + str(len(res)) + " result(s)")
                self.send_response(200)
                to_send = {'received': 'ok', 'result': res}
        except (KeyError, TypeError):
            print("Wrong data passed")
            self.send_response(400)
            to_send = {"received":"error, bad data format"}

        json_data = json.dumps(to_send)

        self.end_headers()
        self.send_header('Content-type', 'application/json')
        self.wfile.write(json_data.encode('utf-8'))

        return


    def do_query(self,query):
        """
        :param query: string representing query to launch
        it returns query result dictionary

        """
        sparql = SPARQLWrapper("http://" + IP_PORT + "/sparql/")
        sparql.setQuery(query)

        sparql.setReturnFormat(JSON)
        result = sparql.query().convert()
        return self.dict_from_query_result(result)

    def dict_from_query_result(self,query_data):
        """
        :param query_data: query result dictionary
        it returns query result dictionary in a more clear version

        """
        triples = query_data["results"]["bindings"]
        t = query_data["head"]["vars"]
        res = []
        for triple in triples:
            msg = {}
            for i in t:
                msg[i] = str(triple[i]["value"]).split("/")[-1].split("#")[-1]
            res.append(msg)
        return res

    def datetime_from_html_to_sparql(self,datetime):
        """
        :param datetime: date and time string in "AAAA-MM-DD HH:MM" format
        it returns datetime string translated in sparql standard

        """
        datetime = str(datetime).replace(" ", "T")
        datetime = '"' + datetime + ":00" + '"' + "^^xsd:dateTime"
        return datetime


# Initializing server and keeping it online until CTRL+C or being turned off by user
httpd = HTTPServer(('localhost', 8000), HTTPRequestHandler)
print("serving at port: 8000")
httpd.serve_forever()

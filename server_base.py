from http.server import HTTPServer, BaseHTTPRequestHandler
from explained_queries import *
import json
from SPARQLWrapper import SPARQLWrapper, JSON
from construct_handler import ConstructQuery

IP_PORT = "localhost:8890"

class HTTPRequestHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
        data_string = self.rfile.read(content_length)  # <--- Gets the data itself

        #EXPECTING THIS FORMAT:
        # {type: WICH QUERY
        # query: {DICTIONARY WITH INPUTS}}

        json_data = json.loads(data_string.decode())
        print(str(json_data))
        try:
            res = {}
            #GESTIONE A GRANDI LINEE CON VARI IF
            if json_data["type"] == "event per ship":
                event = json_data["query"]["event"]
                vessel = json_data["query"]["vessel"]

                if event == "" or vessel == "":
                    raise KeyError
                if vessel.lower() == "all":
                    ves = "?vessel"
                else:
                    ves = ":" + vessel

                query = EVENT_FOR_SHIP_QUERY.replace("[EVENT]", ":" + event).replace("[VESSEL]", ves)
                res = self.do_query(query)

            elif json_data["type"] == "interdiction area":
                vessel = json_data["query"]["vessel"]

                if vessel == "":
                    raise KeyError

                if vessel.lower() == "all":
                    ves = "?vessel"
                else:
                    ves = ":" + vessel

                query = QUERY_INTERDICTION_AREA.replace("[VESSEL]", ves)
                res = self.do_query(query)

            elif json_data["type"] == "protected area":
                protectedArea = json_data["query"]["protectedArea"]
                event = json_data["query"]["event"]
                vessel = json_data["query"]["vessel"]


                if protectedArea == "" or vessel=="" or event == "" :
                    raise KeyError

                area_code = ":" + protectedArea

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

                area_query = PROTECTED_AREA_QUERY.replace("[VESSEL]", ves).replace("[EVENT]", eve)

                result = con.construct_query(area_query)

                res = self.dict_from_query_result(result)
            else:
                res = None
            #FINE GESTIONE A GRANDI LINEE CON VARI IF


            if res is None:
                print("NO QUERY AVAILABLE")
                self.send_response(500)
                to_send = {"received": "error, query type not available"}
            else:
                print("SENT BACK " + str(len(res)) + " result(s)")
                self.send_response(200)
                to_send = {'received': 'ok', 'result': res}
        except KeyError:
            print("Wrong data passed")
            self.send_response(400)
            to_send = {"received":"error, bad data format"}

        json_data = json.dumps(to_send)

        self.end_headers()
        self.send_header('Content-type', 'application/json')
        self.wfile.write(json_data.encode('utf-8'))

        return


    def do_query(self,query):
        sparql = SPARQLWrapper("http://" + IP_PORT + "/sparql/")
        sparql.setQuery(query)

        sparql.setReturnFormat(JSON)
        result = sparql.query().convert()
        return self.dict_from_query_result(result)

    def dict_from_query_result(self,query_data):
        triples = query_data["results"]["bindings"]
        t = query_data["head"]["vars"]
        res = []
        for triple in triples:
            msg = {}
            for i in t:
                msg[i] = str(triple[i]["value"]).split("/")[-1].split("#")[-1]
            res.append(msg)
        return res



httpd = HTTPServer(('localhost', 8000), HTTPRequestHandler)

print("serving at port: 8000")

httpd.serve_forever()
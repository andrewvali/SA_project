from http.server import HTTPServer, BaseHTTPRequestHandler
from explained_queries import *
import json
from SPARQLWrapper import SPARQLWrapper, JSON

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
            if json_data["type"] == "event for ship":
                event = json_data["query"]["event"]
                vessel = json_data["query"]["vessel"]

                if event != "" and vessel != "":
                    if vessel.lower() == "all":
                        ves = "?vessel"
                    else:
                        ves = ":" + vessel

                    query = EVENT_FOR_SHIP_QUERY.replace("[EVENT]", ":" + event).replace("[VESSEL]", ves)

                    res = self.do_query(query)
            #FINE GESTIONE A GRANDI LINEE CON VARI IF

            print("SENT BACK " + str(len(res)) + " result(s)")
            to_send = {'received': 'ok', 'result': res}

            self.send_response(200)
        except KeyError:
            print("Wrong data passed")
            self.send_response(400)
            to_send = {"received":"error"}

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
        triples = result["results"]["bindings"]
        t = result["head"]["vars"]
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

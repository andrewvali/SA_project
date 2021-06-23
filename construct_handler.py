import requests
from requests.auth import HTTPDigestAuth
import rdflib
from SPARQLWrapper import SPARQLWrapper, TURTLE, JSON

class ConstructQuery:
    def __init__(self,construct_uri, endpoint, endpoint_auth, user, passwd):
        self.user = user
        self.passwd = passwd
        self.construct_uri = construct_uri #per comodità si inserisce un uri di un grafo diverso dove caricare i dati del construct
        self.endpoint = endpoint
        self.endpoint_auth = endpoint_auth

    def construct_initializer(self,constr ):

        sparql = SPARQLWrapper(self.endpoint)
        sparql.setQuery(constr)
        sparql.setReturnFormat(TURTLE)
        results = sparql.query().convert().decode()

        g = rdflib.Graph()
        g.parse(data=results, format='turtle')

        triples = ''
        for s, p, o in g.triples((None, None, None)):
            triple = "%s %s %s . " % (s.n3(), p.n3(), o.n3())
            triples += triple

            query = 'INSERT IN GRAPH <%s> { %s }' % (self.construct_uri, triples)

            r = requests.post(self.endpoint_auth, data=query, headers={'Content-type': 'application/sparql-query'},
                              auth=HTTPDigestAuth(self.user, self.passwd))

        if r.status_code != 200:
            print("CODICE: " + str(r.status_code))
            print(r.content.decode())
            raise Exception("Update failed")
        else:
            print("Update DONE.")

    def construct_query(self, query):

        sparql = SPARQLWrapper(self.endpoint, defaultGraph=self.construct_uri)
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        result = sparql.query().convert()
        return result

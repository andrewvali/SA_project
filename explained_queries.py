EVENT_FOR_SHIP_QUERY = """
# EXPLAINATION: RETURNS ALL EVENT FOR SHIP

@prefix geof: <http://www.opengis.net/def/function/geosparql/> .
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
?node :ofMovingObject ?vessel.
?node :hasTemporalFeature ?timestamp.
?timestamp :TimeStart ?datetime.
FILTER(?event = [EVENT] && ?vessel = [VESSEL] && ?datetime >= [DATE_START] && ?datetime <= [DATE_END])
}GROUP BY ?vessel ?event HAVING(COUNT(?event)>2)
ORDER BY DESC(?num_event)"""


TRAJ_GAP_QUERY_1 = """
# EXPLAINATION: RETURNS ALL PORT'S POINTS 

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
}
"""


TRAJ_GAP_QUERY_2 = """# EXPLAINATION: RETURNS TRAJECTORY POINT OF A SPECIFIC VESSEL

@prefix geof: <http://www.opengis.net/def/function/geosparql/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix strdf: <http://strdf.di.uoa.gr/ontology#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix ogc: <http://www.opengis.net/ont/geosparql#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix : <http://www.datacron-project.eu/ais_dataset#> .
@prefix unit: <http://www.datacron-project.eu/unit#> .

SELECT DISTINCT ?timestamp ?datetime ?point
WHERE{
?node a :RawPosition.
?node :ofMovingObject ?vessel .
?node :hasTemporalFeature ?timestamp.
?timestamp :TimeStart ?datetime .

?node :hasGeometry ?geom .
?geom ogc:asWKT ?point .
FILTER (?vessel = [VESSEL] && ?datetime >= [DATE_START] && ?datetime <= [DATE_END]).
}
ORDER BY ASC(?timestamp)
"""

QUERY_INTERDICTION_AREA = """# EXPLAINATION: RETURNS VESSEL STOPPED IN AN INTERDICTION FISHING AREA

@prefix geof: <http://www.opengis.net/def/function/geosparql/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix strdf: <http://strdf.di.uoa.gr/ontology#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix ogc: <http://www.opengis.net/ont/geosparql#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix : <http://www.datacron-project.eu/ais_dataset#> .
@prefix unit: <http://www.datacron-project.eu/unit#> .

SELECT DISTINCT ?vessel ?datetime ?point
WHERE{

?area a :Fishing_Interdiction_area.

:StoppedInit :occurs ?obj.
?obj :ofMovingObject ?vessel.
?obj :hasTemporalFeature ?timestamp_start.
?timestamp_start :TimeStart ?datetime.

?area :hasGeometry ?geom2 .
?geom2 ogc:asWKT ?zone .

?obj :hasGeometry ?geom .
?geom ogc:asWKT ?point .


FILTER (geof:sfWithin(?point, ?zone) && ?vessel = [VESSEL] && ?datetime >= [DATE_START] && ?datetime <= [DATE_END])
} LIMIT 10"""


PROTECTED_AREA_CONSTRUCT ="""# EXPLAINATION: CREATES A NEW TRIPLE COMPOSED BY VESSEL-EVENT-DATE DETECTED IN A PROTECTED AREA

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

FILTER(geof:sfWithin(?point ,?zone ) && ?area = [AREA])
}
} LIMIT 10
"""


PROTECTED_AREA_QUERY = """

# EXPLAINATION: RETURNS VESSEL-EVENT-DATE OF NEW DATASET FROM CONSTRUCT

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
FILTER(?vessel= [VESSEL] && ?event= [EVENT]).}"""
from rdflib import Graph, RDF, URIRef
from SPARQLWrapper import SPARQLWrapper, XML, JSON
from xml.etree import ElementTree

from preprocess import preprocess, match

"""
IMPORT DISEASE ONTOLOGY
"""
sparql = SPARQLWrapper("http://dbpedia.org/sparql")
sparql.setReturnFormat(XML)
sparql.setQuery("""
    select distinct ?disease where {
        ?disease rdf:type dbo:Disease .
    }
    limit 300
""")

results = sparql.query().convert()
graph = Graph()

root = ElementTree.fromstring(results.toxml())

"""DELETE ALL DUPLICATED INSTANCES"""
for result in root.findall(".//{http://www.w3.org/2005/sparql-results#}result"):
    uri = result.find(".//{http://www.w3.org/2005/sparql-results#}uri")
    if uri is not None:
        disease_uri = URIRef(uri.text)
        graph.add((disease_uri, RDF.type, URIRef("http://dbpedia.org/ontology/Disease")))

def searchDBPedia(query):
	results = []
	for iri, predicate, obj in graph.triples((None, RDF.type, None)):
		name = preprocess(iri.split('/')[-1])
		if (match(name, query)) >= 75.0:
			results.append({'iri': iri, 'name': name})
	return results

def storeData(query):
	sparql.setReturnFormat(JSON)
	sparql.setQuery(f"""
		PREFIX dbo: <http://dbpedia.org/ontology/>
		PREFIX dbr: <http://dbpedia.org/resource/>
		PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
		PREFIX dbp: <http://dbpedia.org/property/>

		SELECT *
		WHERE {{?{query} a 
					dbo:Disease ;
					rdfs:label ?name .
			FILTER(CONTAINS(LCASE(?name), "{query}") && langMatches(lang(?name), "es"))}}
		LIMIT 10
	""")
	results = sparql.query().convert()['results']
	print("Resultados obtenidos: ", results)

storeData("tumor")

from SPARQLWrapper import SPARQLWrapper, JSON

from preprocess import preprocess, match

"""
IMPORT DISEASE ONTOLOGY
"""

graph = SPARQLWrapper("http://dbpedia.org/sparql")
graph.setReturnFormat(JSON)

graph.setQuery("""
	select distinct ?disease where {{
		?disease rdf:type dbo:Disease . 
	}}
	limit 500
""")

results = graph.query().convert()['results']
ontology = [{'iri': result['disease']['value'], 'name': result['disease']['value'].split('/')[-1]} for result in results['bindings']]

def searchDBPedia(query):
	results = []
	for element in ontology:
		if match(preprocess(element['name']), query) >= 0.5:
			results.append(element)
	return results
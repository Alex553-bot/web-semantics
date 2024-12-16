from SPARQLWrapper import SPARQLWrapper, JSON

from preprocess import preprocess, match

"""
IMPORT DISEASE ONTOLOGY
"""

graph = SPARQLWrapper("http://dbpedia.org/sparql")
graph.setReturnFormat(JSON)
graph.setQuery(f"""
	select distinct ?disease where {{
		?disease rdf:type dbo:Disease .
	}}
	limit 500
""")

results = graph.query().convert()['results']
ontology = [{'iri': result['disease']['value'], 'name': result['disease']['value'].split('/')[-1]} for result in results['bindings']]
print('ayuda')
def searchDBPedia(query):
	#graph.setQuery(f"""
	#	select distinct ?disease ?value where {{
	#		?disease rdf:type dbo:Disease .
	#		filter(lcase(str(?value)) = lcase("{query}")) 
	#	}}
	#	limit 300
	#""")
	#ontology = graph.query().convert()['results']['bindings']
	results = []
	for element in ontology:
		if match(''.join(preprocess(element['name'])), query) >= 90.0:
			results.append(element)
	return results
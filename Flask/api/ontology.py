from owlready2 import *
from pathlib import Path
from restructure import *

path = Path(__file__).parent.resolve()
path = path.parent.parent
path = path/"oncology.rdf"

ontologie = get_ontology(str(path)).load()
# get_ontology("C:/Users/USER/Documents/WebSemantica/web-semantics/oncology.rdf").load()

def search(queries): 
	results = {}
	for class_ in ontologie.classes():
		for individual in class_.instances():
			for propertie in individual.get_properties():
				for query in queries:
					if contains(query, getattr(individual, propertie.name)):
						if class_.name not in results:
							results[class_.name] = []
						results[class_.name].append({'name':getNombreProp(individual, individual.get_properties()), 'iri': (individual.iri)})
	return results

def contains(element_:str, list_): 
    for element in list_: 
        element = str(element)
        x = element.find(element_)
        if x!=-1: 
            return True
    return False

def get(iri): 
	return ontologie[iri[iri.find('#'):]] # aqui deberia estar el cuerpo completo de un item basado en su iri

def getInstancesByClass(name): 
	class_ = getattr(ontologie, name, None)
	if class_ is None: 
		return []
	instances = []
	for individual in class_.instances():
		instances.append({
			"iri" : individual.iri,
			"individual" : struct_individuals(individual)
		})
	return instances

def getInstancessByNameClassStructured(name:str):
	pass

def getClassesOntologie():
	clasess = []
	for classOntology in ontologie.classes():
		if classOntology.name not in str(clasess) :
			clasess.append({
				"name_class" : classOntology.name,
				"sub_clasess": struct_class(classOntology),
			})
	return clasess

print(ontologie.base_iri)

from rdflib import Graph, Namespace #, URIRef, Literal
g = Graph()
g.parse(str(path), format='xml')
ns = Namespace(ontologie.base_iri)
query = """
PREFIX : <http://www.semanticweb.org/ontologies/oncology-ontology/>

SELECT  ?Cancer
WHERE {
  ?Cancer a :Cancer .
  ?Cancer :nombre "Cancer de pancreas" .
}
"""

results = g.query(query)
for row in results: 
	print(row)

# Prueba de instancias de clases
	

# print(f"Instancias de la clase Cancer: {getInstancesByClass("Cancer")}")

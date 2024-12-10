from owlready2 import *
from pathlib import Path
from rapidfuzz import fuzz

from restructure import *
from preprocess import preprocess

path = Path(__file__).parent.resolve()
path = path.parent.parent
print(path)
path = path/"resourse/ontology.owx"

ontologie = get_ontology(str(path)).load()
# get_ontology("C:/Users/USER/Documents/WebSemantica/web-semantics/oncology.rdf").load()

def search(query):
	query = preprocess(query)
	results = {}
	for individual in ontologie.individuals():
		#print(f"Searching within : {individual}")
		for propertie in individual.get_properties(): 
			for value in getattr(individual, propertie.name, None): 
				match = fuzzy_match(preprocess(str(value)), query)
				if match>=40.0: 
					class_name = str(list(individual.is_a)[0])
					if class_name not in results: 
						results[class_name] = []
					results[class_name].append({'name': individual.name, 'iri': individual.iri})
	return results

def fuzzy_match(s, t): 
	return fuzz.partial_ratio(s, t)

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

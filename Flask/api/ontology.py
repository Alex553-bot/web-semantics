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
	"""
	Search within the ontology for individuals whose properties contain the query string, and return a dictionary of matches, where the keys are the class names of the individuals and the values are lists of dictionaries containing the name of the property and the iri of the individual.

	Parameters
	----------
	query : str
		The string to search for

	Returns
	-------
	dict
		A dictionary of matches, where the keys are the class names of the individuals and the values are lists of dictionaries containing the name of the property and the iri of the individual
	"""
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
					results[class_name].append({'name': getNombreProp(individual, individual.get_properties())[0], 'iri': individual.iri})
	return results

def fuzzy_match(s, t): 
	"""
	Calculates the fuzzy match between two strings.

	Parameters:
		s (str): The string to match against.
		t (str): The string to match.

	Returns:
		float: The fuzzy match score (0-100) between the strings.
	"""
	return fuzz.partial_ratio(s, t)

def get(iri): 
	"""
	Retrieve an item from the ontology by its IRI.

	Parameters:
		iri (str): The IRI of the item to retrieve.

	Returns:
		An instance of the item in the ontology with the given IRI.
	"""
	return ontologie[iri[iri.find('#'):]] # aqui deberia estar el cuerpo completo de un item basado en su iri

def getInstancesByClass(name): 
	"""
	Retrieve instances of a specified class from the ontology.

	Parameters:
		name (str): The name of the class in the ontology to retrieve instances for.

	Returns:
		list: A list of dictionaries, each representing an instance of the specified class.
			Each dictionary contains the 'iri', 'name_class', 'name_individual', and 'properties'
			of the individual. Returns an empty list if the class is not found.
	"""
	class_ = getattr(ontologie, name, None)
	if class_ is None: 
		return []
	return struct_individuals(class_.instances(), class_)

def getClassesOntologie():
	"""
	Retrieve all classes and their subclasses from the ontology.

	Returns:
		list: A list of dictionaries, each representing a class in the ontology.
			Each dictionary contains the 'name_class' and 'sub_clasess' of the class.
			'sub_clasess' is a list of dictionaries, each representing a subclass of the class.
			Each of these dictionaries contains the 'name_class' and 'sub_clasess' of the subclass.
	"""
	clasess = []
	for classOntology in ontologie.classes():
		if classOntology.name not in str(clasess) :
			clasess.append({
				"name_class" : classOntology.name,
				"sub_clasess": struct_class(classOntology),
			})
	return clasess

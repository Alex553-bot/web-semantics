from owlready2 import *
from pathlib import Path
from mtranslate import translate

from restructure import *
from preprocess import preprocess, match as fuzzymatch

path = Path(__file__).parent.resolve()
path = path.parent.parent
path = path/"resourse/ontology.owx"

ontologie = get_ontology(str(path)).load()
# get_ontology("C:/Users/USER/Documents/WebSemantica/web-semantics/oncology.rdf").load()

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
			clasess.append(classOntology.name)
	return clasess

name_classes = getClassesOntologie()

def search(query: str):
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
	# if query not in name_classes:
	# 	return {"error" : 400,"message ": "No existe la entidad en la ontologia local"}
	
	results = {}
	for individual in ontologie.individuals():
		#print(f"Searching within : {individual}")
		for propertie in individual.get_properties():
			ok = 0 
			for value in getattr(individual, propertie.name, None): 
				match = fuzzymatch(preprocess(str(value)), query)
				if match>=50.0: 
					class_name = str(list(individual.is_a)[0])
					if class_name not in results: 
						results[class_name] = []
					results[class_name].append({
						'name': translate(getNombreProp(individual, individual.get_properties())[0], dest='es'), 
						'iri': individual.iri,
						'name_individual': getNombreProp(individual, individual.get_properties())[0], 
						'sample_name': individual.name
					})
					ok = 1
					break
			if ok == 1: break
	return results

def get(iri: str):
	"""
	Retrieve an item from the ontology by its IRI.

	Parameters:
		iri (str): The IRI of the item to retrieve.

	Returns:
		An instance of the item in the ontology with the given IRI.
	"""
	return ontologie[iri[iri.find('#'):]] # aqui deberia estar el cuerpo completo de un item basado en su iri

def getInstancesByClass(name: str, lang: str): 
	"""
	Retrieve instances of a specified class from the ontology.

	Parameters:
		name (str): The name of the class in the ontology to retrieve instances for.
		lang (str): Language to translate the results

	Returns:
		list: A list of dictionaries, each representing an instance of the specified class.
			Each dictionary contains the 'iri', 'name_class', 'name_individual', and 'properties'
			of the individual. Returns an empty list if the class is not found.
	"""
	class_ = getattr(ontologie, name, None)
	if class_ is None: 
		return []
	return struct_individuals(class_.instances(), class_, lang)

def store_in_ontology(items_list, query):
	class_mapping = {
		"drug": {
			"class": "Tratamiento_medico",
			"name_prop": "nombre_tratamiento_medico",
			"desc_prop": "funcion_tratamiento_medico"
		},
		"disease": {
			"class": "Cancer",
			"name_prop": "cancer_nombre",
			"desc_prop": "fases_del_cancer"
		},
		"organization": {
			"class": "Centro_medico",
			"name_prop": "nombre_centro_medico",
			"desc_prop": "descripcion_centro_medico"
		},
		"food": {
			"class": "Alimento_Permitido",
			"name_prop": "alimento_nombre",
			"desc_prop": "descripcion_alimento"
		}
	}

	try:
		with ontologie: 
			for item in items_list:
				item_type = str(item.get('type', {}).get('value', '')).lower()
				
				if item_type in class_mapping:
					mapping = class_mapping[item_type]
					
					onto_class = ontologie.search_one(iri=f"*#{mapping['class']}")
					if not onto_class:
						print(f"Clase no encontrada: {mapping['class']}")
						continue
					
					try:
						new_individual = onto_class()
						
						if 'name' in item and mapping['name_prop']:
							setattr(new_individual, mapping['name_prop'], 
									item['name']['value'])
						
						if 'comment' in item and mapping['desc_prop']:
							setattr(new_individual, mapping['desc_prop'], 
									item['comment']['value'])
							
						print(f"Creado individuo de tipo {item_type}: {item.get('name', {}).get('value', 'Sin nombre')}")
					
					except Exception as e:
						print(f"Error al crear individuo de tipo {item_type}: {str(e)}")
				else:
					print(f"Tipo no reconocido: {item_type}")
					
		ontologie.save(file=str(path))
	except Exception as e:
		return {"error": 500, "message": f"Error al guardar en la ontología: {str(e)}"}

	return search(query);
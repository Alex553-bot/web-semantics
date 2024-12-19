from owlready2 import *
from preprocess import preprocess

def struct_class(ontoClass):
    """
    Recursively constructs a hierarchy of subclasses for a given ontology class.

    Parameters:
    ontoClass (owlready2.entity.ThingClass): The ontology class for which to construct the hierarchy.

    Returns:
    list: A list of dictionaries representing the hierarchy. Each dictionary contains:
        - 'name_class': The name of the subclass.
        - 'sub_class': The hierarchical structure of the subclass.
    """
    herarchy = []
    for subclass in ontoClass.subclasses() :
        herarchy.append({
            "name_class" : subclass.name,
            "sub_class" : struct_class(subclass)
            })
    return herarchy

def struct_individuals(individual, classOntology, lang, translator):
    """
    Retrieve instances of a specified class from the ontology and structure them into a list of dictionaries.
    
    Parameters:
    individual (owlready2.individual.Individual): An individual of the class to retrieve instances for.
    classOntology (owlready2.class_construct.ClassConstruct): The class to retrieve instances for.
    
    Returns:
    list: A list of dictionaries, each representing an instance of the specified class.
        Each dictionary contains the 'iri', 'name_class', 'name_individual', and 'properties'
        of the individual.
    """
    instances = []
    
    for individual in classOntology.instances():
        instances.append({
            "iri" : individual.iri,
            "name_class": translator.translate(preprocess(classOntology.name), dest=lang).text,
            "name_individual": translator.translate(preprocess(getNombreProp(individual, individual.get_properties())[0]), dest=lang).text,
            "properties" : struct_properties(individual, lang, translator)})
    return instances

def struct_properties(ontoIndividual, lang, translator):
    """
    Funcion recursiva para obtener todas las propiedades de una instancia de una clase
    
    Parameters
    ----------
    ontoIndividual : owlready2.entity.ThingClass
        Instancia de una clase
    
    Returns
    -------
    list
        lista de propiedades de la instancia
    """
    properties = ontoIndividual.get_properties() if  ontoIndividual else None

    herarchy = []

    if properties == None:
        return []

    for value in properties:
        if "object"  in str.lower(str(type(value))):
            individual_temp = getattr(ontoIndividual, value.name, None)[0]
            herarchy.append({
                "relationship" : {
                    "iri" : value.iri,
                    "name_object": translator.translate(preprocess(getNombreProp(individual_temp, individual_temp.get_properties())[0]), dest=lang).text,
                    "properties": struct_properties(individual_temp, lang, translator)
                }})
        else :
            if "nombre" not in str(value.name):
                herarchy.append({
                value.name : translator.translate(preprocess(str(getattr(ontoIndividual, value.name, None)[0])), dest=lang).text})
    return herarchy

def getNombreProp(individual, properties):
    """
    Retrieves the value of a property with "nombre" in its name from an individual's properties.

    Args:
        individual: The ontology individual whose properties are being inspected.
        properties: A collection of properties belonging to the individual.

    Returns:
        The value of the property containing "nombre" in its name if found, otherwise returns "No se encontro".
        If properties is None, returns an empty list.
    """
    if properties == None:
        return []
    for propertie in properties:
        if "nombre" in str.lower(str(propertie.name)):
            return getattr(individual, propertie.name, None)
    return "No se encontro"
    
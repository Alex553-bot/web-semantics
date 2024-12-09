def struct_class(ontoClass):
    herarchy = []
    for subclass in ontoClass.subclasses() :
        herarchy.append({
            "name_class" : subclass.name,
            "sub_class" : struct_class(subclass)
            })
    return herarchy

def struct_individuals(ontoIndividual):
    herarchy = []
    properties = ontoIndividual.get_properties() if  ontoIndividual else None
    name_propertie = getNombreProp(ontoIndividual, properties)
    if properties == None:
        return herarchy
    
    herarchy.append({
            "name_individual" : name_propertie[0],
            "properties" : [{value.name: str(getattr(ontoIndividual, value.name, None)[0])} for value in properties]
        })
    return herarchy 

def getNombreProp(individual, properties):
    if properties == None:
        return []
    for propertie in properties:
        if "nombre" in str.lower(str(propertie.name)):
            return getattr(individual, propertie.name, None)
    return "No se encontro"
    
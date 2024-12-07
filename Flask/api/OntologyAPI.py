# # # from owlready2 import Ontology -> para la obtencion directa de una ontologia solo con el path
from owlready2 import *
# Para los decoradores de rutas de api
from flask import Flask, request
# Para la obtencion en json de las rutas en navegador y react
from flask import jsonify
# Para procesar el texto y que sea mas versatil 
from preprocess import preprocess
# Para las operaciones con la ontologia lo movi a otro archivo con las funciones de las queries:
import ontology
# Obtencion de una ontologia mediante su absolute path
# Tambien se puede usar el uri solo si este esta en la web (teoricamente)

def create_app():
    app = Flask(__name__)
    return app

app = create_app()

# Mostrar la owl para una ontologia
# Ruta de la ontologia local: C:\Users\USER\Documents\WebSemantica\web-semantics\oncology.rdf
@app.route('/api/v1/ontologie', methods=['GET'])
def getOntology(path:str):
    global new_path
    new_path = path
    return get_ontology(new_path).load()

# methods=['GET']
# methods=['POST']
# methods=['PUT']
# methods=['DELETE']
@app.route('/api/v1/ontologie/classes/<path>', methods=['GET'])
def getClassesOntologie(path:str):
    ontology = get_ontology(path).load()
    json_return = []
    for classOntology in ontology.classes():
        json_return.append({
            "class":classOntology
        })
    
    return json_return

@app.route('/item')
def getItemOntology():
    iri = request.args.get('iri') 
    item = ontology.get(iri)
    print(item)# -> get a item based on its iri.
    return []

@app.route('/searchClass', methods=['GET'])
def searchClass(): 
    query = request.args['query']
    if query is None: 
        abort(404, f"Class {query} not exists")

    instances = ontology.getInstancesByClass(query)
    return [{'iri': instance.iri, 'name': instance.name} for instance in instances]

@app.route('/search', methods=['GET'])
def search():
    queries = preprocess(request.args['query'])
    if queries is [] or queries is None:
        return jsonify({'error': 'Must have a query'}) # this must redirect the frontend
    return ontology.search(queries)

# # # from owlready2 import Ontology -> para la obtencion directa de una ontologia solo con el path
from owlready2 import *
# Para los decoradores de rutas de api
from flask import Flask, abort, request
# Para la obtencion en json de las rutas en navegador y react
from flask import jsonify
# Para procesar el texto y que sea mas versatil 
from preprocess import preprocess, match
# Para las operaciones con la ontologia lo movi a otro archivo con las funciones de las queries:
import ontology
# Cambio de idioma (utilizando google translate) -> necesita internet
from googletrans import Translator
# Obtencion de una ontologia mediante su absolute path
# Tambien se puede usar el uri solo si este esta en la web (teoricamente)

from restructure import struct_class
import dbpedia

from flask_cors import CORS

def create_app():

    app = Flask(__name__)
    return app

# ontology = get_ontology("C:/Users/USER/Documents/WebSemantica/web-semantics/oncology.rdf").load()
app = create_app()

CORS(app)
translator = Translator()
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
@app.route('/api/v1/ontologie/classes', methods=['GET'])
def getClassesOntologie():
    return jsonify(ontology.getClassesOntologie())

@app.route('/item', methods=['GET'])
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

    return jsonify(ontology.getInstancesByClass(query))

@app.route('/search', methods=['GET'])
def search():
    query = ' '.join(preprocess(request.args['query']))
    lang = request.args['lang']
    if query is None:
        return jsonify({'error': 'Must have a query'}) # this must redirect the frontend
    result_dbpedia = dbpedia.searchDBPedia(query)
    result = ontology.search(query)
    if len(result_dbpedia)!=0:
        result['DOID.dbpedia.Disease'] = result_dbpedia
    if len(result) == 0:
        result['No existen busquedas encontradas'] = []
    return translate(result, lang)

def translate(result, lang):
    for class_ in result.keys():
        class_instances = result[class_]
        for i in range(len(class_instances)):
            instance = class_instances[i]
            for key in instance.keys():
                if key=='iri': continue
                result[class_][i][key] = translator.translate(result[class_][i][key], dest=lang).text
    return result

if __name__ == '__main__' :
    app.run(debug=True)

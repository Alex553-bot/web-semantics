# Decorators for api routes
from flask import Flask, abort, request
# JSON format for responses
from flask import jsonify
# NLP processing 
from preprocess import preprocess
# Ontology searches: local and external (DBPedia)
import ontology
import dbpedia
# Google Translator API
from translator import translate as translate_
# Structure output format
from restructure import struct_class
# CORS web
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    return app

app = create_app()
CORS(app)

""" API ROUTES """
@app.route('/searchClass', methods=['GET'])
def searchClass(): 
    query = translate_(request.args['query'], dest='es')
    lang = request.args['lang']
    if query is None: 
        abort(404, f"Class {query} not exists")
    return jsonify(ontology.getInstancesByClass(query, lang))

@app.route('/search', methods=['GET'])
def search():
    query = preprocess(request.args['query'])
    lang = request.args['lang']

    if query is None:
        return jsonify({'error': 'Must have a query'}) # this must redirect the frontend
    
    result_dbpedia = dbpedia.searchDBPedia(preprocess(translate_(query, dest='en')))
    
    result = ontology.search(preprocess(translate_(query, dest='es')))
    
    if len(result_dbpedia) != 0: result['DOID.dbpedia.Disease'] = result_dbpedia

    if len(result) == 0:
        msg = translate_('No existen busquedas encontradas', dest=lang)
        result[msg] = []

    return translate(result, lang)

def translate(result, lang):
    for class_ in result.keys():
        class_instances = result[class_]
        for i in range(len(class_instances)):
            instance = class_instances[i]
            for key in instance.keys():
                if key=='iri' or key=='name_individual' or key=='sample_name': continue
                result[class_][i][key] = translate_(result[class_][i][key], dest=lang)    
    return result

if __name__ == '__main__' :
    app.run(debug=True)

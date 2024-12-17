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
from googletrans import Translator
# Structure output format
from restructure import struct_class
# CORS web
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    return app

app = create_app()
translator = Translator()
CORS(app)

""" API ROUTES """
@app.route('/searchClass', methods=['GET'])
def searchClass(): 
    query = request.args['query']
    if query is None: 
        abort(404, f"Class {query} not exists")

    return jsonify(ontology.getInstancesByClass(query))

@app.route('/search', methods=['GET'])
def search():
    query = preprocess(request.args['query'])
    lang = 'en'

    if query is None:
        return jsonify({'error': 'Must have a query'}) # this must redirect the frontend
    
    result_dbpedia = dbpedia.searchDBPedia(preprocess(translator.translate(query, dest='en').text))
    
    result = ontology.search(preprocess(translator.translate(query, dest='es').text))
    
    if len(result_dbpedia)!=0: result['DOID.dbpedia.Disease'] = result_dbpedia

    if len(result) == 0:
        msg = translator.translate('No existen busquedas encontradas', dest=lang).text
        result[msg] = []

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

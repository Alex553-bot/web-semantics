# Decorators for api routes
from flask import Flask, abort, request, render_template, send_from_directory
# JSON format for responses
from flask import jsonify
# NLP processing 
from preprocess import preprocess
# Ontology searches: local and external (DBPedia)
import ontology
import dbpedia
from translator import translate as translate_
# CORS web
from flask_cors import CORS

def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    return app

app = create_app()
CORS(app)

""" API ROUTES """
@app.route('/', methods=['GET'])
def index(): 
    return render_template('index.html')
@app.route('/<locale>/class/<class_>/individual/<name_individual>', methods=['GET'])
def indexIndividual(locale, class_, name_individual): 
    return render_template('index.html')

@app.route('/searchClass', methods=['GET'])
def searchClass(): 
    query=  request.args['query']
    #query = translate_(request.args['query'], dest='es')
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
    print('termine el primero')
    result = ontology.search(preprocess(translate_(query, dest='es')), lang)
    print('termine el segundo')
    if len(result_dbpedia) != 0: result['DOID.dbpedia.Disease'] = result_dbpedia

    if len(result) == 0:
        msg = translate_('No existen busquedas encontradas', dest=lang)
        result[msg] = []

    return result

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

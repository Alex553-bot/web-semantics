# # # from owlready2 import Ontology -> para la obtencion directa de una ontologia solo con el path
from owlready2 import *
# Para los decoradores de rutas de api
from flask import Flask
# Para la obtencion en json de las rutas en navegador y react
from flask import jsonify

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
# ontology = Ontology("ontology.rdf")

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
    # if new_path :
        

ontologie = getClassesOntologie("C:/Users/USER/Documents/WebSemantica/web-semantics/oncology.rdf")

print(f"Lista de clases de ontologia: {ontologie}")

# for class_ in ontology.classes():
#     print(class__.name)

# Obtencion de clase como un arreglo convencional solo se puede acceder por el nombre de la clase
# 
# print(f"Impresion de clase: {ontology["Cancer"]}")
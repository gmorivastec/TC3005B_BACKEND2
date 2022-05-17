# para poder incluir código de otras fuentes en este 
# es necesario incluirlo en el path 
# 2 opciones para incluir un folder en el path de python 
# 1 - insertarlo manualmente (sys.path.insert)
# 2 - declarar la variable PYTHONPATH a nivel SO
#       linux / mac - export PYTHONPATH=’path/to/directory’
#       windows - SET PYTHONPATH=’path/to/directory’
import sys
#sys.path.insert(0, "./source")
from flask import Flask
from source.Ejemplo import suma, Vector, endPointFuncion

print(sys.path, file=sys.stdout)


app = Flask(__name__)

# en este archivos hacemos link entre ruta - lógica 
@app.route("/")
def hello_world():
    vectorcito = Vector(2, 3, 4);
    vectorzote = vectorcito.sum(1, 1, 1);
    print(str(vectorzote), file=sys.stdout)
    print(suma(2, 3), file=sys.stdout)
    return "<p>Hello, World!</p>"

app.add_url_rule("/funcion", view_func=endPointFuncion, methods=['GET'])
app.add_url_rule("/clase", view_func=Vector.endPointClase)
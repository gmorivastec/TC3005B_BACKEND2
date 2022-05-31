# para poder incluir código de otras fuentes en este 
# es necesario incluirlo en el path 
# 2 opciones para incluir un folder en el path de python 
# 1 - insertarlo manualmente (sys.path.insert)
# 2 - declarar la variable PYTHONPATH a nivel SO
#       linux / mac - export PYTHONPATH=’path/to/directory’
#       windows - SET PYTHONPATH=’path/to/directory’
#sys.path.insert(0, "./source")


import sys
import flask_login
import secrets

from flask import Flask
from flask_cors import CORS

from source.Ejemplo import suma, Vector, endPointFuncion
from source.handlers.Flask_Login_Handlers import request_loader, unauthorized_handler
from source.api.Flask_Endpoints import raiz, protegido,login

# ESTO SE VA A IR DESPUÉS, AHORITA SÓLO PARA PRUEBA
from source.db.DBManager import DBManager
from source.db.Usuario import Usuario
from sqlalchemy import select

print(sys.path, file=sys.stdout)


app = Flask(__name__)

# manejo de Cross-Origin Resource Sharing (CORS)
# resources es diccionario de entradas de políticas de acceso
# llave -> valor
# expresión regular para especificar URLs -> sitio de acceso
#CORS(app, resources={r"/*", "http://localhost:19006"})
CORS(app, resources={r"/*", "*"})

# código para manejo de sesiones
app.secret_key = secrets.token_urlsafe(16)
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

# especificar handlers con funciones
login_manager.unauthorized_handler(unauthorized_handler)
login_manager.request_loader(request_loader)

# en este archivos hacemos link entre ruta - lógica
app.add_url_rule("/", view_func=raiz)
#app.add_url_rule("/protected", view_func=protegido)
#app.add_url_rule("/login", view_func=login, methods=['POST'])


# cuando haces un singleton todos estos son la misma instancia
db = DBManager.getInstance()
db2 = DBManager.getInstance()
db3 = DBManager.getInstance()

# hagamos un query sencillo 
stmt = select(Usuario)
for user in db.session.scalars(stmt):
    print(user.email)
    print(user.password)
    print(user.token)
    print("")
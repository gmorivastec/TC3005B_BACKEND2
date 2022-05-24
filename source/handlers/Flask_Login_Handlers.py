import sys
import time
import flask_login

from argon2 import PasswordHasher
from source.api.Flask_Endpoints import verificarQueUsuarioExiste
from source.managers.ConfigManager import ConfigManager
from source.db.DBManager import DBManager
from source.db.Usuario import Usuario
from sqlalchemy import update

# definir una clase para contener la descripción de nuestros usuarios
class UsuarioLogin(flask_login.UserMixin):
    pass

def request_loader(request):

    print("****** REQUEST LOADER ESTA FUNCIONANDO", file=sys.stdout)

    # obtener información que nos mandan en encabezado
    key = request.headers.get('Authorization')
    print(key, file=sys.stdout)

    if key == None:
        return None

    if key == ":":
        return None

    processed = key.split(":")

    # recibimos token de encabezado
    usuario = processed[0]
    token = processed[1]

    # verificamos que usuario exista
    usuarioDB = verificarQueUsuarioExiste(usuario)

    if(usuario == None):
        return None

    # verificamos que tenga token válido
    ph = PasswordHasher()

    try:
        ph.verify(usuarioDB.token, token)
    except:
        return None    

    # verificamos que el token siga vigente
    timestamp_actual = time.time()

    cManager = ConfigManager.getInstance()

    if(usuarioDB.last_date + cManager.config['SESSION']['TOKEN_LIFESPAN'] < timestamp_actual):
        return None

    # actualizar vigencia del token 
    db = DBManager.getInstance()

    query = update(Usuario).where(Usuario.id == usuarioDB.id).values(last_date=timestamp_actual)
    db.session.execute(query)
    db.session.commit()

    # regresamos objeto si hubo Y token valido
    # TODO - DEFINIR OBJETO USUARIO PARA SESION 
    result = UsuarioLogin()
    result.id = usuario
    result.nombre = "Pruebita"
    result.apellido = "Rodriguez"
    result.rol = "ADMIN"
    return result

def unauthorized_handler():
    return 'No autorizado', 401


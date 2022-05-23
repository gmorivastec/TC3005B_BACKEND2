import sys
import time
import flask

from flask import jsonify
from argon2 import PasswordHasher

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
    cur = db.connection.cursor()

    query = "SELECT * FROM users WHERE email=?"
    params = (usuario, )

    cur.execute(query, params)
    data = cur.fetchone()
    cur.close()

    if(not data):
        return None

    # verificamos que tenga token válido
    ph = PasswordHasher()

    try:
        ph.verify(data[3], token)
    except:
        return None    

    # verificamos que el token siga vigente
    timestamp_actual = time.time()

    if(data[4] + VIDA_TOKEN < timestamp_actual):
        return None

    # actualizar vigencia del token 
    cur = db.connection.cursor()
    query = "UPDATE users SET last_date=? WHERE email=?"
    params = (timestamp_actual, usuario)
    cur.execute(query, params)
    cur.close()

    # regresamos objeto si hubo Y token valido 
    result = Usuario()
    result.id = usuario
    result.nombre = "Pruebita"
    result.apellido = "Rodriguez"
    result.rol = "ADMIN"
    return result

def unauthorized_handler():
    return 'No autorizado', 401


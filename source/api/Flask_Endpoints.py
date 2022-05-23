import sys
import flask
import flask_login
import secrets
import time
 
from flask import jsonify
from argon2 import PasswordHasher
from sqlalchemy import select
from source.db.DBManager import DBManager
from source.db.Usuario import Usuario
from configparser import ConfigParser

def raiz():
    return "<p>HOLA</p>"

@flask_login.login_required
def protegido():
    return "<p>PROTEGIDO!</p>"


def login():
    
    # intro al password hasher
    ph = PasswordHasher()

    email = flask.request.form['email']
    pw = flask.request.form['pass']

    print(email + " " + pw, file=sys.stdout)

    # 1. verificar existencia de usuario
    db = DBManager.getInstance()

    query = select(Usuario).where(Usuario.email.in_([email]))
    usuarioDB = None

    for user in db.session.scalar(query):
        usuarioDB = user

    if(usuarioDB == None):
        return "USUARIO NO VALIDO", 401

    
    # 2. verificar validez de password
    try:
        ph.verify(usuarioDB.PASSWORD, pw)
    except:
        # 3. password invalido - no login
        return "PASSWORD NO VALIDO", 401

    # 4. password valido - actualizar token y regresarlo
    token = secrets.token_urlsafe(32)
    # así se obtiene el timestamp del momento actual
    last_date = time.time()

    # 5. actualizar BD con entrada de usuario
    cur = db.connection.cursor()
    query = "UPDATE users SET token=?, last_date=? WHERE email=?"
    params = (ph.hash(token), last_date, email)
    cur.execute(query, params)
    cur.close()
    
    config = ConfigParser()
    config.read('config.ini')

    # si no jaló mostrar error
    return jsonify(token=token, caducidad=config['SESSION']['TOKEN_LIFESPAN']), 200
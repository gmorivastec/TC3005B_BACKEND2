import sys
import flask
import flask_login
import secrets
import time
 
from flask import jsonify
from argon2 import PasswordHasher
from sqlalchemy import select, update
from source.db.DBManager import DBManager
from source.db.Usuario import Usuario
from configparser import ConfigParser

from source.managers.ConfigManager import ConfigManager

def raiz():
    return "<p>HOLA</p>"

@flask_login.login_required
def protegido():
    return "<p>PROTEGIDO!</p>"

def verificarQueUsuarioExiste(email):
    db = DBManager.getInstance()

    query = select(Usuario).where(Usuario.email.in_([email]))
    usuarioDB = db.session.scalar(query)

    return usuarioDB

def login():
    
    # intro al password hasher
    ph = PasswordHasher()

    email = flask.request.form['email']
    pw = flask.request.form['pass']

    print(email + " " + pw, file=sys.stdout)

    # 1. verificar existencia de usuario
    usuarioDB = verificarQueUsuarioExiste(email)

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
    # modificado para usar SQLAlchemy 
    db = DBManager.getInstance()

    query = update(Usuario).where(Usuario.id == usuarioDB.id).values(token=ph.hash(token), last_date=last_date)
    db.session.execute(query)
    db.session.commit()
    
    cManager = ConfigManager.getInstance()

    # si no jaló mostrar error
    return jsonify(token=token, caducidad=cManager.config['SESSION']['TOKEN_LIFESPAN']), 200
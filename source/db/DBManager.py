from configparser import ConfigParser
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

# singleton para acceso a recursos de DB

class DBManager:

    instance = None

    def __init__(self):
        
        # verifica que no se cree una segunda instancia del DBManager
        if DBManager.instance != None:
            raise Exception("Usa getInstance")
        
        # si llegamos aquí todo bien
        print("SE INSTANCIO CORRECTAMENTE")

        # cargar valores desde configuracion
        config = ConfigParser()
        config.read('config.ini')

        driver = config['DATABASE']['DRIVER']
        user = config['DATABASE']['USER']
        password = config['DATABASE']['PASSWORD']
        server = config['DATABASE']['SERVER']
        port = config['DATABASE']['PORT']
        db = config['DATABASE']['DATABASE']

        # crear objeto engine y objeto session
        self.engine = create_engine(driver + '://' + user + ':' + password + '@' + server + ':' + str(port) + '/' + db)
        self.session = Session(self.engine)

    # usa siempre este método para asegurarte de acceder a la instancia única
    def getInstance():

        if DBManager.instance == None:
            DBManager.instance = DBManager()
        
        return DBManager.instance
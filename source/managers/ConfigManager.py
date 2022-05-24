from configparser import ConfigParser 

class ConfigManager:

    instance = None

    def __init__(self):

        if ConfigManager.instance != None:
            raise Exception("Usa getInstance en ConfigManager")

        self.config = ConfigParser()
        self.config.read('config.ini')

    def getInstance():
        if ConfigManager.instance == None:
            ConfigManager.instance = ConfigManager()

        return ConfigManager.instance 
        
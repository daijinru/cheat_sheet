env = 'dev'

class GlobalConfig:
    def __init__(self):
        if env == 'dev':
            self.database = '127.0.0.1'
            self.databasePort = 27017

Config = GlobalConfig()

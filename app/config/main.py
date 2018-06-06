env = 'dev'

class GlobalConfig:
    def __init__(self):
        if env == 'dev':
            self.dev = {}
            self.dev['database'] = '127.0.0.1'
            self.dev['databasePort'] = 27017

Config = GlobalConfig()

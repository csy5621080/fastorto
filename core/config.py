import configparser
import os


class Config(configparser.ConfigParser):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db_section = 'Database'
        self.MODEL_FILE_NAME = 'models.py'
        self.VIEWS_FILE_NAME = 'views.py'
        self.modules = ['.'.join(root.replace('./', '').split('/')) for root, dirs, files in os.walk('.')
                        if self.MODEL_FILE_NAME in files]
        self.views = ['.'.join(root.replace('./', '').split('/')) for root, dirs, files in os.walk('.')
                      if self.VIEWS_FILE_NAME in files]
        self.load_file()

    def load_file(self):
        self.read('core/config.ini')

    def db_url(self):
        engine = self[self.db_section].get('engine')
        host = self[self.db_section].get('host')
        port = self[self.db_section].get('port')
        username = self[self.db_section].get('username')
        password = self[self.db_section].get('password')
        db_name = self[self.db_section].get('database_name')
        return f'{engine}://{username}:{password}@{host}:{port}/{db_name}'


conf = Config()

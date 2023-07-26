import configparser, os

configreader = configparser.ConfigParser()
config_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')
configreader.read(config_file_path, encoding='utf-8')
config = dict(configreader.items('Pmagic'))
del config_file_path, configreader
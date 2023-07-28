from commentedconfigparser import CommentedConfigParser
import configparser, os

class config_reader():
    def __init__(self, entity_title):
        self.config_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.ini')
        self.entity_title = entity_title
        self.config = CommentedConfigParser()
        self.reload()
    
    def reload(self):
        self.config.read(self.config_file_path, encoding='utf-8')
        # self.config.read(self.config_file_path, encoding='utf-8')
    
    def set(self, entity, new_setting):
        self.config[self.entity_title][entity] = new_setting
        with open(self.config_file_path, mode="w", encoding='utf-8') as savefile:
            self.config.write(savefile)
    
    def get(self, entity):
        return self.config[self.entity_title][entity]

if __name__ == '__main__':
    c = config_reader('Pmagic')
    print(c.get('window_tiele'))
    c.set('window_tiele', 'MapleStory')
    c.reload()
    print(c.get('window_tiele'))
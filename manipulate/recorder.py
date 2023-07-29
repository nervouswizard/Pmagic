from pynput import keyboard
from PyQt6.QtCore import QThread
from collections import defaultdict
from setting.config import Config_reader
import time, os, shutil

class Recorder(QThread):
    def __init__(self, filename):
        super().__init__()
        self.config = Config_reader('Pmagic')

        self.filename = filename
        self.script_buffer = []
        self.script_file = open(os.path.join(self.config.get('logpath'), self.filename+'.log'), 'w')
        self.buffer_size = 100000
        self.flush_interval = 200
        self.last_flush_time = time.time()

        self.timer = time.time()

    def on_release(self, key):
        try:
            char = key.char
        except AttributeError:
            char = str(key)
        self.script_buffer.append(f'{time.time()-self.timer} {char} released\n')

        # flush script buffer
        # 錄三分鐘才40幾KB 應該不用開吧
        # if len(self.buffer) > self.buffer_size or time.time() - self.last_flush_time >= self.flush_interval:
        #     self.flush()
        
        # Stop listener
        if key == keyboard.Key.esc:
            return False
        
    def on_press(self, key):
        try:
            char = key.char
        except AttributeError:
            char = str(key)
        self.script_buffer.append(f'{time.time()-self.timer} {char} pressed\n')

    def flush(self):
        self.script_file.writelines(self.script_buffer)
        self.script_file.flush()
        self.buffer=[]
        self.last_flush_time = time.time()

    def process(self):
        # read the script
        with open(os.path.join(self.config.get('logpath'), self.filename+'.log'), mode='r') as f:
            lines = [line.strip().split(' ') for line in f]

        # preprocess the lines
        beginIdx = 0
        endIdx = 0
        for i, line in enumerate(lines):
            if line[1].startswith('Key.'):
                line[1] = line[1].replace('Key.', '')
            line[0] = float(line[0])
            if line[1] == 'esc' and line[2] == 'pressed':
                endIdx = i
                break
        lines = lines[beginIdx:endIdx]
        if lines == []:
            return


        script_start_time = lines[0][0]
        keylist = []
        keyCounter = defaultdict(int)
        for line in lines:
            line[0] = line[0] - script_start_time
            if line[2] == 'pressed' and keyCounter[line[1]+line[2]] == 0:
                    keylist.append(line)
                    keyCounter[line[1]+line[2]] += 1
            elif line[2] == 'released':
                keylist.append(line)
                keyCounter[line[1]+'pressed'] -= 1

        with open(os.path.join(self.config.get('script_path'), self.filename+'.script'), mode='w') as f:
            for line in keylist:
                f.write(' '.join(str(elem) for elem in line)+'\n')

    def run(self):
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()
        self.flush()
        self.script_file.close()
        self.process()

class Deleter():
    config = Config_reader('Pmagic')

    @classmethod
    def delect(cls, filename):
        shutil.copy(os.path.join(cls.config.get('script_path'), filename), os.path.join(cls.config.get('delete_path'), filename))
        os.remove(os.path.join(cls.config.get('script_path'), filename))

    @classmethod
    def delete_old_files(cls):
        current_time = time.time()

        for filename in os.listdir(cls.config.get('delete_path')):
            file_path = os.path.join(cls.config.get('delete_path'), filename)

            # 判断文件是否存在超过指定天数
            if os.path.isfile(file_path):
                file_modified_time = os.path.getmtime(file_path)
                days_difference = (current_time - file_modified_time) / 86400

                if days_difference > 30:
                    os.remove(file_path)
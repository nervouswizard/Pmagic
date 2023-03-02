import os
import sys
import time

from pynput import keyboard

class Logger:
    def __init__(self, filename='Log/default.log', stream=sys.stdout, buffer_size=100000, flush_interval=200):
        self.terminal = stream
        self.log = open(filename, 'w')
        self.buffer = []
        self.buffer_size = buffer_size
        self.flush_interval = flush_interval
        self.last_flush_time = time.time()

    @classmethod
    def timestamped_print(cls, *args, **kwargs):
        _print(time.strftime("[%Y/%m/%d %X]"), *args, **kwargs)

    @classmethod
    def script_time_print(cls, *args, **kwargs):
        _print(time.time()-startTime, *args, **kwargs)

    def write(self, message):
        self.terminal.write(message)
        self.buffer.append(message)
        if len(self.buffer) > self.buffer_size or time.time() - self.last_flush_time >= self.flush_interval:
            self.flush()

    def flush(self):
        if self.buffer:
            self.log.writelines(self.buffer)
            self.log.flush()
            self.buffer=[]
            self.last_flush_time = time.time()

def log_history(name_s_log):
    # log
    os.makedirs('C:/ProgramData/Pmagic/Log', exist_ok=True)
    log_file = f'C:/ProgramData/Pmagic/Log/{name_s_log}.log'
    err_file = f'C:/ProgramData/Pmagic/Log/{name_s_log}.err'
    with open(log_file, 'a'), open(err_file, 'a'):
        sys.stdout = Logger(log_file, sys.stdout)
        sys.stderr = Logger(err_file, sys.stderr)

def on_press(key):
    try:
        char = key.char
    except AttributeError:
        char = str(key)
    print(f'{char} pressed')

def on_release(key):
    try:
        char = key.char
    except AttributeError:
        char = str(key)
    print(f'{char} released')
    if key == keyboard.Key.esc:
        print('Stop listener', flush=True)
        # Stop listener
        return False

_print = print
startTime = time.time()
print = Logger.script_time_print
script_name = "my_script"
log_history(script_name)

try:
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
except Exception as e:
    print(f"Error: {e}")
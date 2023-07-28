from pynput import keyboard
from PyQt6.QtCore import QThread, pyqtSignal

class Recorder(QThread):
    def __init__(self):
        super().__init__()

    def on_release(self, key):
        try:
            char = key.char
        except AttributeError:
            char = str(key)
        print(f'{char} released')
        if key == keyboard.Key.esc:
            print('Stop listener')
            # Stop listener
            return False
        
    def on_press(self, key):
        try:
            char = key.char
        except AttributeError:
            char = str(key)
        print(f'{char} pressed')

    def run(self):
        with keyboard.Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()


if __name__=='__main__':
    import time
    r = Recorder()
    r.start()
    for i in range(10):
        print(i)
        time.sleep(1)
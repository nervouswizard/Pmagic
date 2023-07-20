import os, sys, time, random

class Logger(object):
    def __init__(self, filename='Log/default.log', stream=sys.stdout, buffer_size=100000, flush_interval=200):
        self.terminal = stream
        self.log = open(filename, 'w')
        self.buffer = []
        self.buffer_size = buffer_size
        self.flush_interval = flush_interval
        self.last_flush_time = time.time()

    @classmethod
    def timestamped_print(cla, *args, **kwargs):
        _print(time.strftime("[%Y/%m/%d %X]"), *args, **kwargs)

    @classmethod
    def scriptTime_print(cls, *args, **kwargs):
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
    os.makedirs(logpath, exist_ok=True)
    log_file = f'{logpath}{name_s_log}.log'
    err_file = f'{logpath}{name_s_log}.err'
    with open(log_file, 'a'), open(err_file, 'a'):
        sys.stdout = Logger(log_file, sys.stdout)
        sys.stderr = Logger(err_file, sys.stderr)

startTime = time.time()
_print = print
_stdout = sys.stdout
_stderr = sys.stderr

from pynput import keyboard
import pydirectinput as pg
import threading
import win32gui
import concurrent.futures
from collections import deque
from pyHM import mouse
from processScript import processScript

pg.KEYBOARD_MAPPING['page_up'] = 0xC9 + 1024
pg.KEYBOARD_MAPPING['page_down'] = 0xD1 + 1024
pg.KEYBOARD_MAPPING['caps_lock'] = 0x3A
pg.KEYBOARD_MAPPING['shift_l'] = 0x2A
pg.KEYBOARD_MAPPING['shift_r'] = 0x36
pg.KEYBOARD_MAPPING['ctrl_l'] = 0x1D
pg.KEYBOARD_MAPPING['ctrl_r'] = 0x9D + 1024
pg.KEYBOARD_MAPPING['alt_l'] = 0x38
pg.KEYBOARD_MAPPING['alt_r'] = 0xB8 + 1024

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
        print('Stop listener', flush = True)
        # Stop listener
        return False

def on_escpress(key):
    if key == keyboard.Key.esc:
        escEvent.set()
        return False

def pressKey(key):
    pg.keyDown(key, _pause = False)

def release_key(key):
    pg.keyUp(key, _pause = False)

def press_key(key):
    pg.press(key)

def process_line(line):
    if line[2] == 'pressed':
        pg.keyDown(line[1])
    elif line[2] == 'released':
        pg.keyUp(line[1])

def read_script(filename):
    f = open(filename, mode='r')
    lines = f.readlines()
    f.close()
    for i in range(len(lines)):
        lines[i] = lines[i].replace('\n', '')
        lines[i] = lines[i].split(' ')
        lines[i][0] = float(lines[i][0])
    return lines[-1][0], lines

def get_window_size_and_position(window_title):
    hwnd = win32gui.FindWindow(None, window_title)
    if hwnd == 0:
        print(f"找不到windowTiele為{windowTiele}的視窗")
        return None
    # 将焦点设置为目标窗口
    win32gui.SetForegroundWindow(hwnd)
    return win32gui.GetWindowRect(hwnd)

def random_mouse_click(window_size_and_position):
    while True:
        if escEvent.is_set():
            return
        while True:
            if not pauseEvent.is_set():
                break
    
        x1, y1, x2, y2 = window_size_and_position
        x=random.randint(x1+100, x2-100)
        y=random.randint(y1+100, y2-150)
        mouse.move(x, y, multiplier=random.uniform(0.1, 0.5))
        time.sleep(random.uniform(1, 2))
        pg.click()

def doByRows(filename, times):
    window_size_and_position = get_window_size_and_position(windowTiele)
    mouse_thread = threading.Thread(target=random_mouse_click, args=(window_size_and_position,))
    mouse_thread.start()
    scriptTime, lines = read_script(filename)

    print(f"第{times}次迴圈倒數1秒")
    print('script Time: ', scriptTime)
    time.sleep(1)

    TimeFlag = time.time()

    dqlines = deque(lines)
    start_time = time.monotonic()
    while dqlines:
        if escEvent.is_set():
            mouse_thread.join()
            escEvent.clear()
            return True
        while True:
            if not pauseEvent.is_set():
                break

        line = dqlines[0]
        delay = line[0] - (time.monotonic() - start_time)
        if delay > 0:
            time.sleep(delay)
        
        executor.submit(process_line, line)
        dqlines.popleft()

    ProcessTime = time.time()-TimeFlag
    print('Process Time', ProcessTime)
    print(f'相差{ProcessTime - scriptTime}秒')
    print(f'平均每個指令相差{(ProcessTime - scriptTime)/len(lines)}秒')
    escEvent.set()
    mouse_thread.join()
    escEvent.clear()

def pause_and_continue(key):
    if key == keyboard.Key.esc:
        escEvent.set()
        pauseEvent.clear()

def ForegroundWindowDetector():
    while True:
        if escEvent.is_set():
            return True
        hwnd = win32gui.GetForegroundWindow()
        title = win32gui.GetWindowText(hwnd)
        # print(pauseEvent.is_set())
        if not pauseEvent.is_set() and title != windowTiele:
            print('pause')
            pauseEvent.set()
        if pauseEvent.is_set() and title == windowTiele:
            print('continue')
            pauseEvent.clear()
        time.sleep(0.1)

randomKeyList = ['f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12', 'f13']
logpath = 'C:/ProgramData/Pmagic_log/Log/'
script_path = logpath+'Script_v2/'
escEvent = threading.Event()
pauseEvent = threading.Event()
windowTiele = 'MapleStory'
detector = threading.Thread(target = ForegroundWindowDetector)
detector.daemon = True
detector.start()
executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)

while True:
    # 刪除 logpath 資料夾內的其他 .log 跟 .err
    filelist = os.listdir(logpath)
    for idx, file in enumerate(filelist):
        if file.startswith('Pmagic'): continue
        if file.endswith(('.log', '.err')):
            try:
                os.remove(logpath+file)
            except:
                pass

    print = _print
    sys.stdout = _stdout
    sys.stderr = _stderr
    os.system('cls')
    print("檔案儲存路徑:", logpath)
    d1 = input("\n選擇功能:\n\n(1) 錄製腳本\n(2) 執行腳本\n(3) 刪除腳本\n(4) exit\n")

    if d1 == '1':
        while True:
            scriptName = input("請輸入腳本名稱:")
            if not os.path.exists(script_path+scriptName+'.script'):
                break
            print("腳本名稱重複")
        
        os.system('cls')
        print("開始錄製腳本, 按下 page_down 後才算開始錄製\n按 ESC 結束錄製")
        startTime = time.time()
        print = Logger.scriptTime_print
        log_history(scriptName)
        try:
            with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
                listener.join()
        except:
            pass
        processScript(logpath, script_path, scriptName+'.log')

    elif d1 == '2':
        filelist = os.listdir(script_path)
        while True:
            print('請選擇要執行的腳本')
            for idx, file in enumerate(filelist):
                print(f'({idx}) ', file)
            try:
                d2 = int(input())
            except:
                continue
            if d2 < len(filelist):
                break
            print("wrong number")

        while True:
            print('要執行幾次?')
            try:
                d3 = int(input())
            except:
                continue
            if d3 > 0:
                break
            print("wrong number")

        os.system('cls')
        print('執行腳本', filelist[d2])
        print = Logger.timestamped_print
        log_history(os.path.basename(__file__))
        with keyboard.Listener(on_release=pause_and_continue):
            for i in range(d3):
                if doByRows(script_path+filelist[d2], i):
                    break
        print = _print

    elif d1 == '3':
        while True:
            while True:
                filelist = os.listdir(script_path)
                print('請選擇要刪除的腳本')
                for idx, file in enumerate(filelist):
                    print(f'({idx}) ', file)
                print(f'({len(filelist)}) ', "exit")
                try:
                    d2 = int(input())
                except:
                    continue
                if d2 <= len(filelist): break
                print("wrong number")
            if d2 == len(filelist): break
            print('刪除腳本', filelist[d2])
            os.remove(script_path+filelist[d2])
            os.system('cls')
    
    elif d1 == '4':
        break
    
    else:
        print("wrong input")
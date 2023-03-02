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
    def timestamped_print(self, *args, **kwargs):
        _print(time.strftime("[%Y/%m/%d %X]"), *args, **kwargs)

    @classmethod
    def scriptTime_print(self, *args, **kwargs):
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
            self.buffer.clear()
            self.last_flush_time = time.time()

def log_history(name_s_log):
    # log
    os.makedirs('C:/ProgramData/Pmagic', exist_ok=True)
    os.makedirs('C:/ProgramData/Pmagic/Log', exist_ok=True)
    sys.stdout = Logger('C:/ProgramData/Pmagic/Log/' + name_s_log + '.log', sys.stdout)
    f = open('C:/ProgramData/Pmagic/Log/' + name_s_log + '.log', 'a')
    f.close()
    sys.stderr = Logger('C:/ProgramData/Pmagic/Log/' + name_s_log + '.err', sys.stderr)
    f = open('C:/ProgramData/Pmagic/Log/' + name_s_log + '.err', 'a')
    f.close()

startTime = time.time()
_print = print
_stdout = sys.stdout
_stderr = sys.stderr

from pynput import keyboard
import pydirectinput as pg
import threading
from collections import Counter
import win32gui
import concurrent.futures
from collections import deque

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

def processScript(filename):
    f = open(datapath + filename, mode='r')
    lines = f.readlines()
    f.close()
    beginIdx = 0
    for i in range(len(lines)):
        if i == len(lines): continue
        lines[i] = lines[i].replace('\n', '')
        lines[i] = lines[i].split(' ')
        if lines[i][1].startswith('Key.'): lines[i][1] = lines[i][1].replace('Key.', '')
        lines[i][0] = float(lines[i][0])
        if lines[i][1] == 'page_down' and lines[i][2] == 'released' and beginIdx == 0:
            beginIdx = i+1
        if lines[i][1] == 'esc' and lines[i][2] == 'pressed':
            endIdx = i
            break
    lines = lines[beginIdx:endIdx]

    keylist = []
    keyCounter = Counter()
    for i in range(len(lines)):
        if lines[i][2] == 'released':
            keylist.append(lines[i])
            keyCounter[lines[i][1]+'pressed'] -= 1
        elif lines[i][2] == 'pressed':
            if keyCounter[lines[i][1]+lines[i][2]] == 0:
                keylist.append(lines[i])
                keyCounter[lines[i][1]+lines[i][2]] += 1
        
    LastTime = keylist[0][0]
    for i in range(len(keylist)):
        if i == len(keylist): continue
        if i == 0:
            keylist[i][0] = 0
            continue
        temp = keylist[i][0]-LastTime
        LastTime = keylist[i][0]
        keylist[i][0] = temp
        
    createFolder(datapath + 'Script/')
    filename = filename.replace('.log', '.script')
    f = open(datapath + 'Script/' + filename, mode='w')
    for line in keylist:
        line = [str(line[i]) for i in range(len(line))]
        f.write(' '.join(line)+'\n')
    f.close()

def process_line(line):
    if line[2] == 'pressed':
        pg.keyDown(line[1])
    elif line[2] == 'released':
        pg.keyUp(line[1])

def read_script(filename):
    f = open(filename, mode='r')
    lines = f.readlines()
    f.close()
    scriptTime = 0.0
    for i in range(len(lines)):
        lines[i] = lines[i].replace('\n', '')
        lines[i] = lines[i].split(' ')
        lines[i][0] = float(lines[i][0])
        scriptTime += lines[i][0]
    return scriptTime, lines

def doByRows(filename, times):
    hwnd = win32gui.FindWindow(None, windowTiele)
    if hwnd == 0:
        print(f"找不到windowTiele為{windowTiele}的視窗")
    else:
        # 将焦点设置为目标窗口
        win32gui.SetForegroundWindow(hwnd)
    
    scriptTime, lines = read_script(filename)

    print(f"第{times}次迴圈倒數1秒")
    print('script Time: ', scriptTime)
    time.sleep(1)

    for key in randomKeyList:
        if random.random()>0.5:
            press_key(key)
            time.sleep(0.1)

    TimeFlag = time.time()

    start_time = time.monotonic()
    dqlines = deque(lines)
    while dqlines:
        if escEvent.is_set():
            escEvent.clear()
            return True
        while True:
            if not pauseEvent.is_set():
                break
        line = dqlines[0]
        delay = line[0] - (time.monotonic() - start_time)
        delay = delay - 0.0083
        if delay > 0:
            time.sleep(delay)
            
        start_time = time.monotonic()
        executor.submit(process_line, line)
        dqlines.popleft()

    ProcessTime = time.time()-TimeFlag
    print('Process Time', ProcessTime)
    print(f'相差{ProcessTime - scriptTime}秒')
    print(f'平均每個指令相差{(ProcessTime - scriptTime)/len(lines)}秒')

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
            pauseEvent.set()
        if pauseEvent.is_set() and title == windowTiele:
            pauseEvent.clear()
        time.sleep(0.1)

randomKeyList = ['f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12', 'f13']
datapath = 'C:/ProgramData/Pmagic_log/Log/'
escEvent = threading.Event()
pauseEvent = threading.Event()
windowTiele = 'MapleStory'
hwnd = win32gui.FindWindow(None, windowTiele)
detector = threading.Thread(target = ForegroundWindowDetector)
detector.daemon = True
detector.start()
executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)

while True:
    print = _print
    sys.stdout = _stdout
    sys.stderr = _stderr
    os.system('cls')
    print("檔案儲存路徑:", datapath)
    d1 = input("選擇功能：\n(1) 錄製腳本\n(2) 執行腳本\n(3) 刪除腳本\n(4) exit\n")

    if d1 == '1':
        while True:
            scriptName = input("請輸入腳本名稱:")
            if not os.path.exists(datapath+'Script/'+scriptName+'.script'):
                break
            print("腳本名稱重複")
        
        os.system('cls')
        print("開始錄製腳本, 按下page_down後才算開始錄製")
        startTime = time.time()
        print = Logger.scriptTime_print
        log_history(scriptName)
        try:
            with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
                listener.join()
        except:
            pass
        # processScript(scriptName+'.log')

    elif d1 == '2':
        filelist = os.listdir(datapath+'Script/')
        while True:
            print('請選擇要執行的腳本')
            for idx, file in enumerate(filelist):
                print(f'({idx}) ', file)
            d2 = int(input())
            if d2 < len(filelist):
                break
            print("wrong number")

        while True:
            print('要執行幾次?')
            d3 = int(input())
            if d3 > 0:
                break
            print("wrong number")

        os.system('cls')
        print('執行腳本', filelist[d2])
        print = Logger.timestamped_print
        log_history(os.path.basename(__file__))
        with keyboard.Listener(on_release=pause_and_continue):
            for i in range(d3):
                if doByRows(datapath+'Script/'+filelist[d2], i):
                    break
            print = _print

    elif d1 == '3':
        while True:
            while True:
                filelist = os.listdir(datapath+'Script/')
                print('請選擇要刪除的腳本')
                for idx, file in enumerate(filelist):
                    print(f'({idx}) ', file)
                print(f'({len(filelist)}) ', "exit")
                d2 = int(input())
                if d2 <= len(filelist): break
                print("wrong number")
            if d2 == len(filelist): break
            print('刪除腳本', filelist[d2])
            os.remove(datapath+'Script/'+filelist[d2])
            os.system('cls')
    
    elif d1 == '4':
        break
    
    else:
        print("wrong input")
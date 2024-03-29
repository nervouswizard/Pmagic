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
import configparser
import string
from ctypes import windll

PostMessageW = windll.user32.PostMessageW
MapVirtualKeyW = windll.user32.MapVirtualKeyW
VkKeyScanA = windll.user32.VkKeyScanA

WM_KEYDOWN = 0x100
WM_KEYUP = 0x101

VkCode = {
    "back":  0x08,
    "tab":  0x09,
    "return":  0x0D,
    "shift":  0x10,
    "control":  0x11,
    "menu":  0x12,
    "pause":  0x13,
    "capital":  0x14,
    "escape":  0x1B,
    "esc":  0x1B,
    "space":  0x20,
    "end":  0x23,
    "home":  0x24,
    "left":  0x25,
    "up":  0x26,
    "right":  0x27,
    "down":  0x28,
    "print":  0x2A,
    "snapshot":  0x2C,
    "insert":  0x2D,
    "delete":  0x2E,
    "lwin":  0x5B,
    "rwin":  0x5C,
    "numpad0":  0x60,
    "numpad1":  0x61,
    "numpad2":  0x62,
    "numpad3":  0x63,
    "numpad4":  0x64,
    "numpad5":  0x65,
    "numpad6":  0x66,
    "numpad7":  0x67,
    "numpad8":  0x68,
    "numpad9":  0x69,
    "multiply":  0x6A,
    "add":  0x6B,
    "separator":  0x6C,
    "subtract":  0x6D,
    "decimal":  0x6E,
    "divide":  0x6F,
    "f1":  0x70,
    "f2":  0x71,
    "f3":  0x72,
    "f4":  0x73,
    "f5":  0x74,
    "f6":  0x75,
    "f7":  0x76,
    "f8":  0x77,
    "f9":  0x78,
    "f10":  0x79,
    "f11":  0x7A,
    "f12":  0x7B,
    "numlock":  0x90,
    "scroll":  0x91,
    "lshift":  0xA0,
    "rshift":  0xA1,
    "lcontrol":  0xA2,
    "rcontrol":  0xA3,
    "lmenu":  0xA4,
    "rmenu":  0XA5,
    "page_up": 0x21,
    "page_down": 0x22,
    "caps_lock": 0x14,
    "shift_l": 0xA0,
    "shift_r": 0xA1,
    "ctrl_l": 0XA2,
    "ctrl_r": 0xA3,
    "alt_l": 0xA4,
    "alt_r": 0xA5,
}

def get_virtual_keycode(key: str):
    """根据按键名获取虚拟按键码

    Args:
        key (str): 按键名

    Returns:
        int: 虚拟按键码
    """
    if len(key) == 1 and key in string.printable:
        # https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-vkkeyscana
        return VkKeyScanA(ord(key)) & 0xff
    else:
        return VkCode[key]
    
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

def bg_process_line(line):
    if line[2] == 'pressed':
        """按下指定按键

        Args:
            handle (HWND): 窗口句柄
            key (str): 按键名
        """
        vk_code = get_virtual_keycode(line[1])
        scan_code = MapVirtualKeyW(vk_code, 0)
        # https://docs.microsoft.com/en-us/windows/win32/inputdev/wm-keydown
        wparam = vk_code
        lparam = (scan_code << 16) | 1
        PostMessageW(handle, WM_KEYDOWN, wparam, lparam)
        
    elif line[2] == 'released':
        """放开指定按键

        Args:
            handle (HWND): 窗口句柄
            key (str): 按键名
        """
        vk_code = get_virtual_keycode(line[1])
        scan_code = MapVirtualKeyW(vk_code, 0)
        # https://docs.microsoft.com/en-us/windows/win32/inputdev/wm-keyup
        wparam = vk_code
        lparam = (scan_code << 16) | 0XC0000001
        PostMessageW(handle, WM_KEYUP, wparam, lparam)

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
        if stopmouseEvent.is_set():
            stopmouseEvent.clear()
            return
    
        x1, y1, x2, y2 = window_size_and_position
        x=random.randint(x1+100, x2-100)
        y=random.randint(y1+100, y2-150)
        mouse.move(x, y, multiplier=random.uniform(0.1, 0.5))
        time.sleep(random.uniform(3, 5))
        pg.click()

def doByRows(filename, times):
    if UsewindowTiele:
        window_size_and_position = get_window_size_and_position(windowTiele)
    if UsewindowTiele and Use_mouse_random_move:
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
            stopmouseEvent.set()
            escEvent.clear()
            return True

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
    stopmouseEvent.set()

def pause_and_continue(key):
    if key == keyboard.Key.esc:
        escEvent.set()

configreader = configparser.ConfigParser()
configreader.read('config.ini', encoding='utf-8')
config = dict(configreader.items('Pmagic'))
del configreader
windowTiele = config['window_tiele']
Use_background_running = config['use_background_running']=='true'
UsewindowTiele = config['focus_on_window']=='true'
Use_mouse_random_move = config['use_mouse_random_move']=='true'

logpath = 'C:/ProgramData/Pmagic_log/Log/'
script_path = logpath+'Script_v2/'
escEvent = threading.Event()
stopmouseEvent = threading.Event()

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

        if Use_background_running:
            handle = windll.user32.FindWindowW(None, windowTiele)
            process_line = bg_process_line

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
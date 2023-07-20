import win32gui, time, random, ctypes, win32api, tkinter
import pydirectinput as pg
SendInput = ctypes.windll.user32.SendInput
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]
    
class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]
    
class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

def random_mouse_click(x1, x2, y1, y2):
    user32 = ctypes.windll.user32
    screen_width = user32.GetSystemMetrics(0)
    screen_height = user32.GetSystemMetrics(1)

    # x=random.randint(x1+100, x2-100)*(65536//screen_width)
    # y=random.randint(y1+100, y2-150)*(65536//screen_height)
    x = 225
    y = 82
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.mi = MouseInput( x, y, 0, 0x0001|0x8000, 1000, ctypes.pointer(extra))
    x = Input( ctypes.c_ulong(0), ii_ )
    user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
    time.sleep(1)
    ii_.mi = MouseInput( 0, 0, 0, 0x0002, 0, ctypes.pointer(extra))
    x = Input( ctypes.c_ulong(0), ii_ )
    user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
    time.sleep(1)
    x = 225*(65536//screen_width)
    y = 82*(65536//screen_height)
    ii_.mi = MouseInput( x, y, 0, 0x0001|0x8000, 0, ctypes.pointer(extra))
    x = Input( ctypes.c_ulong(0), ii_ )
    user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
    time.sleep(1)
    ii_.mi = MouseInput( 0, 0, 0, 0x0004, 0, ctypes.pointer(extra))
    x = Input( ctypes.c_ulong(0), ii_ )
    user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


    # pg.moveTo(x=random.randint(x1+100, x2-100), y=random.randint(y1+100, y2-150), duration=random.uniform(0.1, 0.5))
    # time.sleep(random.uniform(0.5, 1.5))
    # pg.click()

def get_window_size_and_position(windowTiele):
    hwnd = win32gui.FindWindow(None, windowTiele)
    if hwnd == 0:
        print(f"找不到windowTiele為{windowTiele}的視窗")
        return None
    
    # 将焦点设置为目标窗口
    # win32gui.SetForegroundWindow(hwnd)
    return win32gui.GetWindowRect(hwnd)


windowTiele = 'MapleStory'
window_size_and_position = get_window_size_and_position(windowTiele)
if window_size_and_position:
    x, y, width, height = window_size_and_position
    print(f"視窗大小：{width}x{height}")
    print(f"視窗座標：({x}, {y})")
random_mouse_click(x, width, y, height)
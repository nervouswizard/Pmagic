from pyHM import mouse
import win32gui, random, time
import pydirectinput as pg

def random_mouse_click(x1, x2, y1, y2):
    x=random.randint(x1+100, x2-100)
    y=random.randint(y1+100, y2-150)
    # mouse.move(x, y, multiplier=random.uniform(0.1, 0.5))
    # pydirectinput.moveTo(x, y)
    time.sleep(0.5)
    pg.click()
    # time.sleep(random.uniform(0.5, 1.5))
    # pg.moveTo(x=random.randint(x1+100, x2-100), y=random.randint(y1+100, y2-150), duration=random.uniform(0.1, 0.5))
    # time.sleep(random.uniform(0.5, 1.5))
    # pg.click()

def get_window_size_and_position(windowTiele):
    hwnd = win32gui.FindWindow(None, windowTiele)
    if hwnd == 0:
        print(f"找不到windowTiele為{windowTiele}的視窗")
        return None
    
    # 将焦点设置为目标窗口
    win32gui.SetForegroundWindow(hwnd)
    return win32gui.GetWindowRect(hwnd)


windowTiele = 'MapleStory'
window_size_and_position = get_window_size_and_position(windowTiele)
if window_size_and_position:
    x, y, width, height = window_size_and_position
    print(f"視窗大小：{width}x{height}")
    print(f"視窗座標：({x}, {y})")
# while True:
random_mouse_click(x, width, y, height)

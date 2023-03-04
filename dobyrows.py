import os, time
import pydirectinput as pg
from collections import deque
from concurrent.futures import ThreadPoolExecutor

pg.KEYBOARD_MAPPING['page_up'] = 0xC9 + 1024
pg.KEYBOARD_MAPPING['page_down'] = 0xD1 + 1024
pg.KEYBOARD_MAPPING['caps_lock'] = 0x3A
pg.KEYBOARD_MAPPING['shift_l'] = 0x2A
pg.KEYBOARD_MAPPING['shift_r'] = 0x36
pg.KEYBOARD_MAPPING['ctrl_l'] = 0x1D
pg.KEYBOARD_MAPPING['ctrl_r'] = 0x9D + 1024
pg.KEYBOARD_MAPPING['alt_l'] = 0x38
pg.KEYBOARD_MAPPING['alt_r'] = 0xB8 + 1024

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

def doByRows(filename, times):
    scriptTime, lines = read_script(filename)

    print(f"第{times}次迴圈倒數1秒")
    print('script Time: ', scriptTime)
    time.sleep(1)

    TimeFlag = time.time()

    dqlines = deque(lines)
    start_time = time.monotonic()
    while dqlines:
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


datapath = 'C:/ProgramData/Pmagic/Log/'
script_name = 'my_script.script'
executor = ThreadPoolExecutor(max_workers=10)

print('執行腳本', script_name)
doByRows(os.path.join(datapath,'Script',script_name), 1)
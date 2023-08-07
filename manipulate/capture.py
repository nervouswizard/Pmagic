from setting.config import Config_reader
import ctypes, os, sys, cv2, time
from threading import Thread
import numpy as np
from ctypes import wintypes
from manipulate.manipulator import process_line
import mss
import mss.windows
user32 = ctypes.windll.user32

MM_TL_TEMPLATE = cv2.imread('assets/minimap_tl_template.png', 0)
MM_BR_TEMPLATE = cv2.imread('assets/minimap_br_template.png', 0)

HPMP_TL_TEMPLATE = cv2.imread('assets/HPMP_tl.png', 0)
HPMP_BR_TEMPLATE = cv2.imread('assets/HPMP_br.png', 0)
HPMP_TEMPLATE = cv2.imread('assets/HPMP.png', 0)

MINIMAP_TOP_BORDER = 5
MINIMAP_BOTTOM_BORDER = 9

PLAYER_TEMPLATE = cv2.imread('assets/player_template.png', 0)
PT_HEIGHT, PT_WIDTH = PLAYER_TEMPLATE.shape

OTHER_TEMPLATE = cv2.imread('assets/other_template.png', 0)

class Capture():
    def __init__(self):
        self.config = Config_reader('Pmagic')

        self.window = {
            'left': 0,
            'top': 0,
            'width': 1366,
            'height': 768
        }

        self.minimap = None
        self.minimap_stop = False

        self.hpmp = None
        self.hpmp_stop = False

        self.build_thread()        

    def build_thread(self):
        self.minimap_thread = Thread(target=self.minimap_capture)
        self.minimap_thread.daemon=True
        self.hpmp_thread = Thread(target=self.hpmp_capture)
        self.hpmp_thread.daemon=True

    def find_window(self):
        handle = user32.FindWindowW(None, self.config.get('window_tiele'))
        if handle == 0: return
        rect = wintypes.RECT()
        user32.GetWindowRect(handle, ctypes.pointer(rect))
        rect = (rect.left, rect.top, rect.right, rect.bottom)
        rect = tuple(max(0, x) for x in rect)
        self.window['left'] = rect[0]
        self.window['top'] = rect[1]
        self.window['width'] = rect[2] - rect[0]
        self.window['height'] = rect[3] - rect[1]

    def single_match(self, frame, template):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        result = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF)
        _, _, _, top_left = cv2.minMaxLoc(result)
        w, h = template.shape[::-1]
        bottom_right = (top_left[0] + w, top_left[1] + h)
        return top_left, bottom_right

    def multi_match(self, frame, template, threshold=0.95):
        """
        Finds all matches in FRAME that are similar to TEMPLATE by at least THRESHOLD.
        :param frame:       The image in which to search.
        :param template:    The template to match with.
        :param threshold:   The minimum percentage of TEMPLATE that each result must match.
        :return:            An array of matches that exceed THRESHOLD.
        """

        if template.shape[0] > frame.shape[0] or template.shape[1] > frame.shape[1]:
            return []
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        result = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
        locations = np.where(result >= threshold)
        locations = list(zip(*locations[::-1]))
        results = []
        for p in locations:
            x = int(round(p[0] + template.shape[1] / 2))
            y = int(round(p[1] + template.shape[0] / 2))
            results.append((x, y))
        return results

    def screenshot(self, delay=1):
        try:
            return np.array(mss.mss().grab(self.window))
        except :
            print(f'\n[!] Error while taking screenshot, retrying in {delay} second' + ('s' if delay != 1 else ''))
            time.sleep(delay)

    def hpmp_capture(self):
        while True:
            if self.hpmp_stop: break
            self.find_window()
            frame = self.screenshot()
            if frame is None:
                continue
            
            tl, br = self.single_match(frame, HPMP_TEMPLATE)
            mm_tl = (
                tl[0],
                tl[1]
            )
            mm_br = (
                max(mm_tl[0] + 10, br[0]),
                max(mm_tl[1] + 10, br[1])
            )

            frame = frame[mm_tl[1]:mm_br[1], mm_tl[0]+21:mm_br[0]-3]
            bgr = cv2.split(frame)
            r = bgr[2]
            r = r[:r.shape[0]//2, :]
            _, r = cv2.threshold(r, 127, 255, cv2.THRESH_BINARY)
            hp = np.argmin(np.diff(np.sum(r, axis=0).tolist()))

            b = bgr[0]
            b = b[b.shape[0]//2:, :]
            _, b = cv2.threshold(b, 127, 255, cv2.THRESH_BINARY)
            mp = np.argmin(np.diff(np.sum(b, axis=0).tolist()))

            hp_percent = hp*100//frame.shape[1]
            mp_percent = mp*100//frame.shape[1]

            frame = cv2.line(frame, (hp, 0), (hp, 16), (0, 0, 0), 1)
            frame = cv2.line(frame, (mp, 17), (mp, frame.shape[1]), (0, 0, 0), 1)
            self.hpmp = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # 決定要不要用藥水
            if self.config.get('auto_hpmp_check') == 'true':
                if hp_percent < int(self.config.get('hp_threshold')):
                    process_line([0, self.config.get('hp_key'), 'pressed'])
                    time.sleep(0.01)
                    process_line([0, self.config.get('hp_key'), 'released'])
                if mp_percent < int(self.config.get('mp_threshold')):
                    process_line([0, self.config.get('mp_key'), 'pressed'])
                    time.sleep(0.01)
                    process_line([0, self.config.get('mp_key'), 'released'])
            
    def minimap_capture(self):
        while True:
            if self.minimap_stop: break
            self.find_window()
            frame = self.screenshot()
            if frame is None:
                continue
            
            tl, _ = self.single_match(frame, MM_TL_TEMPLATE)
            _, br = self.single_match(frame, MM_BR_TEMPLATE)
            
            mm_tl = (
                tl[0] + MINIMAP_BOTTOM_BORDER,
                tl[1] + MINIMAP_TOP_BORDER
            )
            mm_br = (
                max(mm_tl[0] + PT_WIDTH, br[0] - MINIMAP_BOTTOM_BORDER),
                max(mm_tl[1] + PT_HEIGHT, br[1] - MINIMAP_BOTTOM_BORDER)
            )
            frame = frame[mm_tl[1]:mm_br[1], mm_tl[0]:mm_br[0]]

            if frame is []: continue

            player = self.multi_match(frame, PLAYER_TEMPLATE, threshold=0.8)
            other = self.multi_match(frame, OTHER_TEMPLATE, threshold=0.8)

            if player:
                frame = cv2.circle(frame, player[0], 3, (0,0,255), -1)
                

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.minimap = frame

            # 有其他玩家就結束遊戲
            # print(other)
            # if other:
            #     process_line([0, 'esc', 'pressed'])
            #     time.sleep(0.01)
            #     process_line([0, 'esc', 'released'])
            #     time.sleep(0.01)
            #     process_line([0, 'up', 'pressed'])
            #     time.sleep(0.01)
            #     process_line([0, 'up', 'released'])
            #     time.sleep(0.01)
            #     process_line([0, 'enter', 'pressed'])
            #     time.sleep(0.01)
            #     process_line([0, 'enter', 'released'])

if __name__=='__main__':
    sys.path.append(os.getcwd())
    from setting.config import Config_reader
    c = Capture()
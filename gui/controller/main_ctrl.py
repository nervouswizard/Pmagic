from PyQt6 import QtWidgets, QtGui, QtCore
from gui.main import Ui_MainWindow
from setting.config import Config_reader
from gui.controller.createScript_ctrl import createScript_MainWindow_controller
from manipulate.manipulator import Deleter, Runner
from manipulate.capture import Capture
import os, time

class MainWindow_controller(QtWidgets.QMainWindow):
    def __init__(self):
        # qt init
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # config
        self.config = Config_reader('Pmagic')
        os.makedirs(self.config.get('script_path'), exist_ok=True)
        os.makedirs(self.config.get('delete_path'), exist_ok=True)

        # 刪除腳本
        Deleter.delete_old_files()

        # 新增腳本
        self.new_script_dialog = createScript_MainWindow_controller()
        self.new_script_dialog.finished.connect(self.init)

        # 截圖
        self.capture = Capture()
        self.minimap_timer = QtCore.QTimer(self)
        self.minimap_timer.timeout.connect(self.show_minimap)
        self.hpmp_timer = QtCore.QTimer(self)
        self.hpmp_timer.timeout.connect(self.show_hpmp)


        # bind function
        self.ui.scripts_list.customContextMenuRequested.connect(self.show_context_menu)
        self.ui.search_bar_for_script.textChanged.connect(self.filter_scripts_list)
        self.ui.scripts_list.itemClicked.connect(self.show_selected_item)
        self.ui.actionNew_script.triggered.connect(self.trigger_new_script)
        self.ui.actionUse_background_running.changed.connect(self.use_background_running_change)
        self.ui.actionFocus_on_window.changed.connect(self.focus_on_window_change)
        self.ui.actionUse_mouse_random_move.changed.connect(self.use_mouse_random_move_change)
        self.ui.actionShow_minimap.changed.connect(self.show_minimap_change)
        self.ui.actionShow_hpmp.changed.connect(self.show_hpmp_change)
        self.ui.start_script.clicked.connect(self.start_script)
        self.ui.stop_script.clicked.connect(self.stop_script)
        self.ui.script_times.valueChanged.connect(self.script_times_change)
        self.ui.hp_threshold.valueChanged.connect(self.hp_threshold_change)
        self.ui.mp_threshold.valueChanged.connect(self.mp_threshold_change)
        self.ui.auto_hpmp_check.stateChanged.connect(self.auto_hpmp_check_change)

        self.ui.test_button.clicked.connect(self.test)
        self.ui.test_button.setVisible(False)

        self.init()

    def init(self):
        # 顯示所有的腳本
        script_list = os.listdir(self.config.get("script_path"))
        self.ui.selected_script.setText("None")
        self.ui.scripts_list.clear()
        self.ui.scripts_list.addItems(script_list)

        # 檢查 config
        if self.config.get('use_background_running') == 'true':
            self.ui.actionUse_background_running.setChecked(True)
        if self.config.get('focus_on_window') == 'true':
            self.ui.actionFocus_on_window.setChecked(True)
        if self.config.get('use_mouse_random_move') == 'true':
            self.ui.actionUse_mouse_random_move.setChecked(True)
        if self.config.get('show_minimap') == 'true':
            self.ui.actionShow_minimap.setChecked(True)
        if self.config.get('show_hpmp') == 'true':
            self.ui.actionShow_hpmp.setChecked(True)
        if self.config.get('auto_hpmp_check') == 'true':
            self.ui.auto_hpmp_check.setChecked(True)
        self.ui.script_times.setValue(int(self.config.get('script_times')))
        self.ui.hp_threshold.setValue(int(self.config.get('hp_threshold')))
        self.ui.mp_threshold.setValue(int(self.config.get('mp_threshold')))
        
    
    # 顯示小地圖
    def show_minimap(self):
        if self.capture.minimap is None:
            return
        img = self.capture.minimap
        height, width, channel = img.shape
        bytesPerline = channel * width
        qimg = QtGui.QImage(img, width, height, bytesPerline, QtGui.QImage.Format.Format_RGB888)
        qimg = qimg.scaled(self.ui.minimap_label.width(), self.ui.minimap_label.height(), QtCore.Qt.AspectRatioMode.KeepAspectRatio)
        canvas = QtGui.QPixmap().fromImage(qimg)
        self.ui.minimap_label.setPixmap(canvas)
        
    # 顯示血魔
    def show_hpmp(self):
        if self.capture.hpmp is None:
            return
        img = self.capture.hpmp
        height, width, channel = img.shape
        bytesPerline = channel * width
        qimg = QtGui.QImage(img, width, height, bytesPerline, QtGui.QImage.Format.Format_RGB888)
        qimg = qimg.scaled(self.ui.hpmp_label.width(), self.ui.hpmp_label.height(), QtCore.Qt.AspectRatioMode.KeepAspectRatio)
        canvas = QtGui.QPixmap().fromImage(qimg)
        self.ui.hpmp_label.setPixmap(canvas)
        del img, height, width, channel, bytesPerline, qimg, canvas

    # scripts_list 按滑鼠右鍵顯示
    def show_context_menu(self, pos):
        menu = QtWidgets.QMenu(self)
        delete_action = QtGui.QAction('Delete', self)
        delete_action.triggered.connect(self.delete_script)
        menu.addAction(delete_action)
        menu.exec(self.ui.scripts_list.mapToGlobal(pos))

    # 搜尋腳本
    def filter_scripts_list(self, text):
        for index in range(self.ui.scripts_list.count()):
            item = self.ui.scripts_list.item(index)
            if text in item.text():
                item.setHidden(False)
            else:
                item.setHidden(True)

    # 顯示被選擇的腳本
    def show_selected_item(self, item):
        self.ui.selected_script.setText(item.text())

    # 按下New script
    def trigger_new_script(self):
        self.new_script_dialog.show()

    # 背景視窗執行改變勾選狀態 
    def use_background_running_change(self):
        if self.ui.actionUse_background_running.isChecked():
            self.config.set('use_background_running', 'true')
        else:
            self.config.set('use_background_running', 'false')
        self.config.reload()

    # 開始時自動前景改變勾選狀態 
    def focus_on_window_change(self):
        if self.ui.actionFocus_on_window.isChecked():
            self.config.set('focus_on_window', 'true')
        else:
            self.config.set('focus_on_window', 'false')
        self.config.reload()

    # 隨機移動滑鼠改變勾選狀態 
    def use_mouse_random_move_change(self):
        if self.ui.actionUse_mouse_random_move.isChecked():
            self.config.set('use_mouse_random_move', 'true')
        else:
            self.config.set('use_mouse_random_move', 'false')
        self.config.reload()

    # 顯示小地圖改變勾選狀態
    def show_minimap_change(self):
        if self.ui.actionShow_minimap.isChecked():
            self.config.set('show_minimap', 'true')
            self.capture.minimap_stop = False
            self.capture.build_thread()
            self.capture.minimap_thread.start()
            self.minimap_timer.start(10)
        else:
            self.config.set('show_minimap', 'false')
            self.capture.minimap_stop = True
            self.minimap_timer.stop()
            self.ui.minimap_label.clear()
        self.config.reload()
        self.init()

    # 顯示血量魔力改變勾選狀態
    def show_hpmp_change(self):
        if self.ui.actionShow_hpmp.isChecked():
            self.config.set('show_hpmp', 'true')
            self.capture.hpmp_stop = False
            self.capture.build_thread()
            self.capture.hpmp_thread.start()
            self.hpmp_timer.start(10)
        else:
            self.config.set('show_hpmp', 'false')
            self.capture.hpmp_stop = True
            self.hpmp_timer.stop()
            self.ui.hpmp_label.clear()
        self.config.reload()
        self.init()

    # 開始腳本
    def start_script(self):
        self.script_runner = Runner(self.ui.selected_script.text())
        self.script_runner.start()
        self.ui.start_script.setEnabled(False)
        self.ui.show_running_script_list.addItem(f'執行腳本{self.ui.selected_script.text()}')
    
    # 結束腳本
    def stop_script(self):
        self.ui.show_running_script_list.addItem('stop_script')
        self.script_runner.terminate()
        self.ui.start_script.setEnabled(True)

    # 腳本運行次數改變
    def script_times_change(self):
        self.config.set('script_times', str(self.ui.script_times.value()))
        self.config.reload()

    # 血量界線改變
    def hp_threshold_change(self):
        self.config.set('hp_threshold', str(self.ui.hp_threshold.value()))
        self.config.reload()

    # 魔力界線改變
    def mp_threshold_change(self):
        self.config.set('mp_threshold', str(self.ui.mp_threshold.value()))
        self.config.reload()

    # 自動回血魔改變勾選狀態
    def auto_hpmp_check_change(self):
        if self.ui.auto_hpmp_check.isChecked():
            self.config.set('auto_hpmp_check', 'true')
        else:
            self.config.set('auto_hpmp_check', 'false')
        self.config.reload()

    # 刪除腳本
    def delete_script(self):
        Deleter.delect(self.ui.scripts_list.currentItem().text())
        self.init()
    
    def test(self):
        pass
from PyQt6 import QtWidgets, QtGui
from gui.main import Ui_MainWindow
from setting.config import Config_reader
from gui.controller.createScript_ctrl import createScript_MainWindow_controller
from manipulate.manipulator import Deleter, Runner
import os

class MainWindow_controller(QtWidgets.QMainWindow):
    def __init__(self):
        # qt init
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.config = Config_reader('Pmagic')
        os.makedirs(self.config.get('script_path'), exist_ok=True)
        os.makedirs(self.config.get('delete_path'), exist_ok=True)
        Deleter.delete_old_files()
        self.new_script_dialog = createScript_MainWindow_controller()
        self.init()

        # bind function
        self.ui.scripts_list.customContextMenuRequested.connect(self.show_context_menu)
        self.ui.search_bar_for_script.textChanged.connect(self.filter_scripts_list)
        self.ui.scripts_list.itemClicked.connect(self.show_selected_item)
        self.ui.actionNew_script.triggered.connect(self.trigger_new_script)
        self.ui.actionUse_background_running.changed.connect(self.use_background_running_change)
        self.ui.actionFocus_on_window.changed.connect(self.focus_on_window_change)
        self.ui.actionUse_mouse_random_move.changed.connect(self.use_mouse_random_move_change)
        self.ui.start_script.clicked.connect(self.start_script)
        self.ui.stop_script.clicked.connect(self.stop_script)
        self.ui.script_times.valueChanged.connect(self.script_times_change)

    def init(self):
        # 顯示所有的腳本
        script_list = os.listdir(self.config.get("script_path"))
        self.ui.selected_script.setText("None")
        self.ui.scripts_list.clear()
        self.ui.scripts_list.addItems(script_list)

        # 檢查 Setting 相關 config
        if self.config.get('use_background_running') == 'true':
            self.ui.actionUse_background_running.setChecked(True)
        if self.config.get('focus_on_window') == 'true':
            self.ui.actionFocus_on_window.setChecked(True)
        if self.config.get('use_mouse_random_move') == 'true':
            self.ui.actionUse_mouse_random_move.setChecked(True)
        self.ui.script_times.setValue(int(self.config.get('script_times')))
    
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

    # use background running 改變勾選狀態 
    def use_background_running_change(self):
        if self.ui.actionUse_background_running.isChecked():
            self.config.set('use_background_running', 'true')
        else:
            self.config.set('use_background_running', 'false')
        self.config.reload()

    # focus on window 改變勾選狀態 
    def focus_on_window_change(self):
        if self.ui.actionFocus_on_window.isChecked():
            self.config.set('focus_on_window', 'true')
        else:
            self.config.set('focus_on_window', 'false')
        self.config.reload()

    # use mouse random move 改變勾選狀態 
    def use_mouse_random_move_change(self):
        if self.ui.actionUse_mouse_random_move.isChecked():
            self.config.set('use_mouse_random_move', 'true')
        else:
            self.config.set('use_mouse_random_move', 'false')
        self.config.reload()

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

    # 刪除腳本
    def delete_script(self):
        Deleter.delect(self.ui.scripts_list.currentItem().text())
        self.init()
    
    def test(self):
        print('test function')
from PyQt6 import QtWidgets
from gui.main import Ui_MainWindow
from setting.config import config_reader
from gui.controller.createScript_ctrl import createScript_MainWindow_controller
import os

class MainWindow_controller(QtWidgets.QMainWindow):
    def __init__(self):
        # qt init
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.config = config_reader('Pmagic')
        self.new_script_dialog = createScript_MainWindow_controller()
        self.init()

        # bind function
        self.ui.scripts_list.customContextMenuRequested.connect(self.show_context_menu)
        self.ui.search_bar_for_script.textChanged.connect(self.filter_scripts_list)
        self.ui.scripts_list.itemClicked.connect(self.show_selected_item)
        self.ui.actionNew_script.triggered.connect(self.trigger_new_script)

    def init(self):
        # 顯示所有的腳本
        script_list = os.listdir(self.config.get("script_path"))
        self.ui.scripts_list.clear()
        self.ui.scripts_list.addItems(script_list)
        # 檢查Setting 相關 config
        if self.config.get('use_background_running') == 'true':
            self.ui.actionUse_background_running.setChecked(True)
        if self.config.get('focus_on_window') == 'true':
            self.ui.actionFocus_on_window.setChecked(True)
        if self.config.get('use_mouse_random_move') == 'true':
            self.ui.actionUse_mouse_random_move.setChecked(True)
    
    # 按滑鼠右鍵顯示
    def show_context_menu(self, point):
        print('right click')
        # menu = QtWidgets.QMenu(self)
        # delete_action = QtGui.QAction('Delete', self)
        # delete_action.triggered.connect(self.delete_script)
        # menu.addAction(delete_action)
        # menu.exec(self.ui.scripts_list.mapToGlobal(pos))

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

    def delete_script(self):
        print('delete')
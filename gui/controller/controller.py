from PyQt6 import QtWidgets
from gui.GUI import Ui_MainWindow
from setting.config import config
import os

class MainWindow_controller(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.search_bar_for_script.textChanged.connect(self.filter_scripts_list)
        self.show_scripts_list()

    # 顯示所有的腳本
    def show_scripts_list(self):
        script_list = os.listdir(config["script_path"])
        self.ui.scripts_list.addItems(script_list)
    
    # 搜尋腳本
    def filter_scripts_list(self, text):
        for index in range(self.ui.scripts_list.count()):
            item = self.ui.scripts_list.item(index)
            if text in item.text():
                item.setHidden(False)
            else:
                item.setHidden(True)
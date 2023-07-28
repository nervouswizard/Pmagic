from PyQt6 import QtWidgets, QtGui
from gui.GUI import Ui_MainWindow
from setting.config import config_reader
import os

class MainWindow_controller(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.config = config_reader('Pmagic')

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init()
        self.context_menu = QtWidgets.QMenu(self)
        action1 = self.context_menu.addAction("Action 1")
        action2 = self.context_menu.addAction("Action 2")
        action3 = self.context_menu.addAction("Action 3")
        self.ui.scripts_list.customContextMenuRequested.connect(self.show_context_menu)
        self.ui.search_bar_for_script.textChanged.connect(self.filter_scripts_list)
        self.ui.scripts_list.itemClicked.connect(self.show_selected_item)
    # 滑鼠右鍵選單
    def contextMenuEvent(self, event):
        print(self.ui.scripts_list.size())
        # Show the context menu
        self.context_menu.exec(event.globalPos())

    def init(self):
        # 顯示所有的腳本
        script_list = os.listdir(self.config.get("script_path"))
        self.ui.scripts_list.clear()
        self.ui.scripts_list.addItems(script_list)
    
    # 按滑鼠右鍵顯示
    def show_context_menu(self, pos):

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


    def delete_script(self):
        print('delete')
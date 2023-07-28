from PyQt6 import QtWidgets
from setting.config import config_reader
from gui.createScript import Ui_Dialog
from gui.messagebox import Messagebox
import os

class createScript_MainWindow_controller(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.config = config_reader('Pmagic')
        self.init()

        # bind function
        self.ui.name_line.textChanged.connect(self.name_list_changed)
        self.ui.start_button.clicked.connect(self.start_button_click)
        self.ui.stop_button.clicked.connect(self.stop_button_click)


    def init(self):
        self.ui.list.clear()
        self.ui.list.addItem("請先輸入腳本名稱")

    def name_list_changed(self):
        self.ui.list.clear()
        self.ui.list.addItem(f"腳本儲存位置 : {self.config.get('script_path')}")
        self.ui.list.addItem(f"腳本名稱 : {self.ui.name_line.text()}")
        self.ui.list.addItem("按start以開始錄製腳本")

    def start_button_click(self):
        if os.path.exists(os.path.join(self.config.get('script_path'), self.ui.name_line.text()+'.script')):
            Messagebox.waring_message_box("錯誤", "腳本名稱重複!")
            return
        self.ui.name_line.setReadOnly(True)
        self.ui.list.addItem("START")

    def stop_button_click(self):
        self.ui.list.addItem("END")
        self.ui.list.addItem("儲存中")
        self.ui.list.addItem("儲存完成")
        self.ui.name_line.setReadOnly(False)
        self.init()
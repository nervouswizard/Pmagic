from PyQt6 import QtWidgets, QtGui
from setting.config import Config_reader
from gui.createScript import Ui_Dialog
from gui.messagebox import Messagebox
from manipulate.manipulator import Recorder
import os

class createScript_MainWindow_controller(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.config = Config_reader('Pmagic')
        self.init()

        # bind function
        self.ui.name_line.textChanged.connect(self.name_list_changed)
        self.ui.start_button.clicked.connect(self.start_button_click)


    def init(self):
        self.ui.list.clear()
        self.ui.list.addItem("請先輸入腳本名稱")

    def name_list_changed(self):
        self.ui.list.clear()
        self.ui.list.addItem(f"腳本儲存位置 : {self.config.get('script_path')}")
        self.ui.list.addItem(f"腳本名稱 : {self.ui.name_line.text()}")
        self.ui.list.addItem("按start以立刻開始錄製腳本")
        self.ui.list.addItem("按ESC以結束錄製, 直接關閉視窗會導致錄製失敗")
        self.ui.list.item(3).setForeground(QtGui.QColor(255,0,0))

    def start_button_click(self):
        if os.path.exists(os.path.join(self.config.get('script_path'), self.ui.name_line.text()+'.script')):
            Messagebox.waring_message_box("錯誤", "腳本名稱重複!")
            return
        self.ui.name_line.setReadOnly(True)
        self.ui.start_button.setEnabled(False)
        self.recorder = Recorder(self.ui.name_line.text())
        self.recorder.finished.connect(self.stop_recording)
        self.ui.list.addItem("START")
        self.recorder.start()

    def stop_recording(self):
        self.ui.list.addItem("END")
        self.ui.name_line.setReadOnly(False)
        self.ui.start_button.setEnabled(True)
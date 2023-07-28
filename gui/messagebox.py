from PyQt6.QtWidgets import QMessageBox

class Messagebox():

    @classmethod
    def waring_message_box(self, title, text):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Warning)
        msg_box.setWindowTitle(title)
        msg_box.setText(text)
        msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
        msg_box.exec()
# Form implementation generated from reading ui file 'GUI.ui'
#
# Created by: PyQt6 UI code generator 6.5.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(657, 587)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(parent=self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(72, 112, 181, 226))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.search_bar_for_script = QtWidgets.QLineEdit(parent=self.widget)
        self.search_bar_for_script.setObjectName("search_bar_for_script")
        self.horizontalLayout_2.addWidget(self.search_bar_for_script)
        self.search_button = QtWidgets.QPushButton(parent=self.widget)
        self.search_button.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../icon/search.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.search_button.setIcon(icon)
        self.search_button.setObjectName("search_button")
        self.horizontalLayout_2.addWidget(self.search_button)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.scripts_list = QtWidgets.QListWidget(parent=self.widget)
        self.scripts_list.setObjectName("scripts_list")
        self.verticalLayout.addWidget(self.scripts_list)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 657, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

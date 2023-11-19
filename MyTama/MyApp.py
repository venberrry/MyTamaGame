import sys
import time
from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import QApplication, QLineEdit, QMainWindow, QStackedWidget, QPushButton, QToolButton
from ClientElevation import ClientCommunication
from threading import Thread

class MyWindow(QMainWindow):
    signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setFixedSize(400, 500)
        self.setStyleSheet("background-color: #2b2b2b;")
        # Создаем стек с окнами
        self.statusBar().setSizeGripEnabled(False)
        self.stacked_widget = QStackedWidget(self)
        self.setCentralWidget(self.stacked_widget)

        self.ui_widget_menu = uic.loadUi('tama_guis/menu.ui')
        self.stacked_widget.addWidget(self.ui_widget_menu)
        self.ui_widget_reg = uic.loadUi('tama_guis/reg.ui')
        self.stacked_widget.addWidget(self.ui_widget_reg)
        self.ui_widget_error = uic.loadUi('tama_guis/error.ui')
        self.stacked_widget.addWidget(self.ui_widget_error)
        self.ui_widget_load = uic.loadUi('tama_guis/loading.ui')
        self.stacked_widget.addWidget(self.ui_widget_load)

        self.statusBar().setSizeGripEnabled(False)

        # create room
        createRoomBtn = self.findChild(QPushButton, 'createRoomBTN')
        createRoomBtn.clicked.connect(self.show_widget_reg)
        self.ui_widget_reg.sendNickBTN.clicked.connect(self.acceptNick)

        # error widget
        self.ui_widget_error.backToMenuBTN.clicked.connect(self.show_menu)

        # Настройка ввода количества символов для ника юзера
        self.ui_widget_reg.nickLineEdit.setMaxLength(10)
        self.ui_widget_reg.nickLineEdit.textChanged.connect(self.on_text_changed)

    def connect_to_server(self):
        try:
            client = ClientCommunication(4096, ('127.0.0.1', 8007))
            client.connect(self.clientNickname)
            print('передал', self.clientNickname)
            self.stacked_widget.setCurrentWidget(self.ui_widget_load)
        except Exception as e:
            print(f"An error occurred: {e}")
            self.stacked_widget.setCurrentWidget(self.ui_widget_error)

    @pyqtSlot()
    def show_menu(self):
        self.stacked_widget.setCurrentWidget(self.ui_widget_menu)

    @pyqtSlot()
    def show_widget_reg(self):
        self.stacked_widget.setCurrentWidget(self.ui_widget_reg)

    @pyqtSlot()
    def acceptNick(self):
        self.clientNickname: str = self.ui_widget_reg.nickLineEdit.text()
        print(self.clientNickname)
        print('tyt1')
        self.ui_widget_reg.nickLineEdit.clear()
        print('tyt2')
        print('tyt3')
        self.connect_to_server()
        print('tyt4')

    def on_text_changed(self, text):
        print('символ')
        max_length = 10
        if len(text) > max_length:
            self.sender().setText(text[:max_length])

    # def conn_to_server(self):
    #     clientNickname = self.ui_widget_reg.nickLineEdit.text()
    #     print(clientNickname)
    #     print('tyt2')
    #     # Очищаем поле
    #     self.ui_widget_reg.nickLineEdit.clear()
    #     time.sleep(0.25)
    #     self.actual_connect_to_server()
    #     print('tyt3')




if __name__ == '__main__':
    app = QApplication([])
    window = MyWindow()
    window.show()
    app.exec()


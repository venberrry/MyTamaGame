import time
from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal, pyqtSlot
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QPushButton, QLabel
from PyQt6.uic.properties import QtGui
from PyQt6.QtGui import QPixmap

from ClientElevation import ClientCommunication

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
        self.ui_widget_reg_conn = uic.loadUi('tama_guis/reg_conn.ui')
        self.stacked_widget.addWidget(self.ui_widget_reg_conn)
        self.ui_widget_error = uic.loadUi('tama_guis/error.ui')
        self.stacked_widget.addWidget(self.ui_widget_error)
        self.ui_widget_load = uic.loadUi('tama_guis/loading.ui')
        self.stacked_widget.addWidget(self.ui_widget_load)
        self.ui_widget_room = uic.loadUi('tama_guis/room.ui')
        self.stacked_widget.addWidget(self.ui_widget_room)
        self.ui_widget_character = uic.loadUi('tama_guis/character.ui')
        self.stacked_widget.addWidget(self.ui_widget_character)

        self.ui_widget_menu.joinRoomBTN.clicked.connect(self.join_server)

        # Установка изображений для QLabel в 'character.ui'
        self.ui_widget_character.black_label.setPixmap(QPixmap("tama_guis/src/black_cat.jpg"))
        self.ui_widget_character.white_label_2.setPixmap(QPixmap("tama_guis/src/white_cat.jpg"))
        self.ui_widget_character.din_label.setPixmap(QPixmap("tama_guis/src/dinozavr.jpg"))

        # НАЧАЛО
        self.stacked_widget.setCurrentWidget(self.ui_widget_menu)

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

        # Room Setting
        # self.ui_widget_room.chatWidget.inputArea
        self.ui_widget_room.submitBTN.clicked.connect(self.send_message_to_chat)

    def connect_to_server_create_room(self):
        try:
            self.client = ClientCommunication(4096, ('127.0.0.1', 8007))
            self.client.connect_create_room(self.clientNickname, self.character)
            print('передал', self.clientNickname, self.character)

            self.stacked_widget.setCurrentWidget(self.ui_widget_room)
        except Exception as e:
            self.stacked_widget.setCurrentWidget(self.ui_widget_error)
            print(f"An error occurred: {e}")

    @pyqtSlot()
    def show_menu(self):
        self.stacked_widget.setCurrentWidget(self.ui_widget_menu)

    @pyqtSlot()
    def show_choose_your_pikachu(self):
        self.stacked_widget.setCurrentWidget(self.ui_widget_character)
        print('err5')
        self.ui_widget_character.black_BTN.clicked.connect(self.set_character_black)
        print('err6')
        self.ui_widget_character.white_BTN.clicked.connect(self.set_character_white)
        print('err7')
        self.ui_widget_character.din_BNT.clicked.connect(self.set_character_dino)
        print('я сделал')

    @pyqtSlot()
    def set_character_black(self):
        self.character = "black_one"
        print('черный')
        self.stacked_widget.setCurrentWidget(self.ui_widget_load)
        self.start_connect()

    @pyqtSlot()
    def set_character_white(self):
        self.character = "white_one"
        print('белый')
        self.stacked_widget.setCurrentWidget(self.ui_widget_load)
        self.start_connect()

    @pyqtSlot()
    def set_character_dino(self):
        self.character = "dino_one"
        print('динозавр гугл')
        self.stacked_widget.setCurrentWidget(self.ui_widget_load)
        self.start_connect()

    @pyqtSlot()
    def show_widget_reg(self):
        self.stacked_widget.setCurrentWidget(self.ui_widget_reg)

    @pyqtSlot()
    def acceptNick(self):
        self.clientNickname: str = self.ui_widget_reg.nickLineEdit.text()
        print(self.clientNickname)
        self.ui_widget_reg.nickLineEdit.clear()
        try:
            print('q')
            self.show_choose_your_pikachu()
            print('ваш карактер принят')
        except:
            self.stacked_widget.setCurrentWidget(self.ui_widget_error)
            print('err1')
        print('tyt3')

    def start_connect(self):
        try:
            self.connect_to_server_create_room()
            print('коннект ту сервер')
        except:
            self.stacked_widget.setCurrentWidget(self.ui_widget_error)
            print('err1')

    @pyqtSlot()
    def send_message_to_chat(self):
        print('oi3')
        msg = self.ui_widget_room.inputArea.text()
        if msg != "":
            print('oi2')
            self.client.client_send_text("text", msg)
            self.ui_widget_room.chatArea.append(msg)
            print('oi')
        else:
            print('oioioii')
        # clear
        self.ui_widget_room.inputArea.clear()

    def on_text_changed(self, text):
        max_length = 10
        if len(text) > max_length:
            self.sender().setText(text[:max_length])

    def connect_to_server(self):
        try:
            self.client = ClientCommunication(4096, ('127.0.0.1', 8007))
            self.client.connect_to_serv(self.clientNickname)
            print('передал', self.clientNickname)

            self.stacked_widget.setCurrentWidget(self.ui_widget_room)
        except Exception as e:
            self.stacked_widget.setCurrentWidget(self.ui_widget_error)
            print(f"An error occurred: {e}")

    def acceptNick_withoutCreatingServ(self):
        self.clientNickname: str = self.ui_widget_reg.nickLineEdit.text()
        print(self.clientNickname)
        self.ui_widget_reg.nickLineEdit.clear()
        try:
            print('ваше имя принято', self.clientNickname)
            print('начинаю подключение')
            self.connect_to_server()
        except:
            self.stacked_widget.setCurrentWidget(self.ui_widget_error)
            print('err1')
        print('tyt3')

    def join_server(self):
        self.stacked_widget.setCurrentWidget(self.ui_widget_reg_conn)
        self.ui_widget_reg_conn.sendNickBTN.clicked.connect(self.acceptNick_withoutCreatingServ)



if __name__ == '__main__':
    app = QApplication([])
    window = MyWindow()
    window.show()
    app.exec()


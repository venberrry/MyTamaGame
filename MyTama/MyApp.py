import copy
import time
import socket
from datetime import datetime

from ServerPack.Tamagochi import Tamago

from common.ClientUtils import Utils
import pickle
from PyQt6 import uic
from PyQt6.QtCore import pyqtSignal, pyqtSlot, QThread
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget, QPushButton, QLabel
from PyQt6 import QtGui, QtWidgets, QtCore
from PyQt6.QtGui import QPixmap
from tama_guis.menu import Ui_MenuWindowGUI
from tama_guis.reg import Ui_RegWindowGUI
from tama_guis.error import Ui_ErrorWindowGUI
from tama_guis.loading import Ui_LoadWindowGUI
from tama_guis.room import Ui_RoomWindowGUI
from tama_guis.reg_conn import Ui_RegConnWindowGUI
from tama_guis.character import Ui_CharWindowGUI
from threading import Thread


class DB:
    client_tamagochi = Tamago("ad", "ad")


class RecvFromServer(QThread):
    my_signal = pyqtSignal(str)
    my_signal_message = pyqtSignal(str, str)

    def __init__(self, sock, addr, buff):
        super().__init__()
        self.sock = sock
        self.addr = addr
        self.buff = buff

    def run(self):
        try:
            while True:
                ut = Utils(self.buff)
                pickle_pack = ut.recv_full_pickle(self.sock)
                print("fldfldsfokdo")
                pack = pickle.loads(pickle_pack)
                type = pack.get("type")
                print('from pack', pack.get("type"))
                print('from pack', pack.get("data"))
                print('from pack', pack.get("optional"))
                if type == "text":
                    print("[", datetime.now().hour, ':',
                          datetime.now().minute, ':',
                          datetime.now().second, '] (', pack.get("nick"), ")",
                          ':', pack.get("data"), "\n")
                elif type == "nickname":
                    print("nick был принят", pack.get("data"))
                elif type == "tamagochi_exist":
                    self.my_signal.emit("Im alive")
                    print("Заходим в комнату с существующим тамагочи")
                elif type == "tamagochi_not_exist":
                    print("соре, вам некуда заходить")
                    self.my_signal.emit("Im not alive")
                elif type == "new_message":
                    print('recv new message')
                    message = pack.get("data")
                    self.my_signal_message.emit("new_message", message)
                elif type == "update":
                    print('recv update')
                    tama_image = pack.get("data")
                    print(tama_image.eat)

                    DB.client_tamagochi = copy.deepcopy(tama_image)
                    self.my_signal.emit("update_tama")
                elif type == "tama_not_exist_can_create":
                    print('recv create')
                    tama_image = pack.get("data")
                    print("recv", tama_image)
                    self.my_signal.emit(type)
                elif type == "tama_exist_cannot_create":
                    self.my_signal.emit(type)
                elif type == "tama_not_exist_cannot_join":
                    self.my_signal.emit(type)
                elif type == "tama_can_join":
                    print('recv join')
                    tama_image = pack.get("data")
                    print("recv", tama_image)
                    self.my_signal.emit(type)

                    DB.client_tamagochi = copy.deepcopy(tama_image)
                    self.my_signal.emit("update_tama")

        except Exception as err:
            self.my_signal.emit("ops_error")
            print("----------DISCONECT1")
            print(f"При получении данных возникла ошибка: {err}")
            print("----------DISCONECT1")


class ClientCommunication(QThread):
    message_sent = pyqtSignal(str)
    message_signal = pyqtSignal(str, str)

    def __init__(self, buff, address):
        super().__init__()
        self.buff = buff
        self.address = address
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('localhost', 0))

    def send_nickname(self, clientNick: str, type_connect: str, con_nickname):  # РАБОТАЕТ
        temp_type: str = "nickname"
        data = {
            'type': temp_type,
            'data': clientNick,
            'optional': type_connect,
            'connectedNick': con_nickname
        }
        data_new = pickle.dumps(data)
        self.sock.send(data_new + b'OK')

    def send_character(self, clientChar: str):  # РАБОТАЕТ
        temp_type: str = "character"
        data = {
            'type': temp_type,
            'data': clientChar,
            'optional': None
        }
        data_new = pickle.dumps(data)
        self.sock.send(data_new + b'OK')

    def send_message(self, msg):
        temp_type: str = "message"
        data = {
            'type': temp_type,
            'data': msg,
            'optional': ""
        }
        data_new = pickle.dumps(data)
        self.sock.send(data_new + b'OK')

    def send_eat(self):
        temp_type: str = "eat_up"
        data = {
            'type': temp_type,
            'data': "",
            'optional': ""
        }
        data_new = pickle.dumps(data)
        self.sock.send(data_new + b'OK')

    def send_mood(self):
        temp_type: str = "mood_up"
        data = {
            'type': temp_type,
            'data': "",
            'optional': ""
        }
        data_new = pickle.dumps(data)
        self.sock.send(data_new + b'OK')

    def send_sleep(self):
        temp_type: str = "sleep_up"
        data = {
            'type': temp_type,
            'data': "",
            'optional': ""
        }
        data_new = pickle.dumps(data)
        self.sock.send(data_new + b'OK')

    def just_connect(self):  # РАБОТАЕТ
        self.sock.connect(self.address)
        self.recv_cycle = RecvFromServer(self.sock, self.address, self.buff)
        self.recv_cycle.my_signal.connect(self.trans_signal)
        self.recv_cycle.my_signal_message.connect(self.trans_signal_message)
        self.recv_cycle.start()

    def trans_signal_message(self, line, msg):
        print("trans-message ", line)
        self.message_signal.emit(line, msg)

    def trans_signal(self, line):
        print("trans-signal ", line)
        self.message_sent.emit(line)


class MenuWindow(QMainWindow, Ui_MenuWindowGUI):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


class RegWindow(QMainWindow, Ui_RegWindowGUI):
    def __init__(self, client, clientNick, char_window, error_window):
        super().__init__()
        self.clientNick = clientNick
        self.setupUi(self)
        self.client = client
        self.char_window = char_window
        self.error_window = error_window
        self.sendNickBTN.clicked.connect(self.accept_nick)

    def accept_nick(self):
        self.clientNick: str = self.nickLineEdit.text()
        print(self.clientNick, "создаёт комнату")
        try:
            self.connect_to_server()
            self.client.send_nickname(self.clientNick, "create", "")
            self.hide()
        except:
            self.hide()
            self.error_window.show()

    def connect_to_server(self):
        self.client.just_connect()


class CharacterWindow(QMainWindow, Ui_CharWindowGUI):
    def __init__(self, client, error_window, room_window):
        super().__init__()
        self.setupUi(self)
        self.error_window = error_window
        self.room_window = room_window
        self.client = client
        self.black_BTN.clicked.connect(self.black_choosed)
        self.white_BTN.clicked.connect(self.white_choosed)
        self.din_BNT.clicked.connect(self.dino_choosed)

    def black_choosed(self):
        self.character = "black_cat"
        try:
            DB.client_tamagochi.name = "black_cat"
            self.client.send_character(self.character)
            self.hide()
            self.room_window.show()
            self.room_window.update_tama()
        except:
            self.hide()
            self.error_window.show()

    def white_choosed(self):
        self.character = "white_cat"
        try:
            DB.client_tamagochi.name = "white_cat"
            self.client.send_character(self.character)
            self.hide()
            self.room_window.show()
            self.room_window.update_tama()
        except:
            self.hide()
            self.error_window.show()

    def dino_choosed(self):
        self.character = "google_dino"
        try:
            DB.client_tamagochi.name = "google_dino"
            self.client.send_character(self.character)
            self.hide()
            self.room_window.show()
            self.room_window.update_tama()
        except:
            self.hide()
            self.error_window.show()


class RoomWindow(QMainWindow, Ui_RoomWindowGUI):
    def __init__(self, client):
        super().__init__()
        self.setupUi(self)
        self.client = client

        self.submitBTN.clicked.connect(self.send_message)
        self.eat_btn.clicked.connect(self.eat_send)
        self.mood_btn.clicked.connect(self.mood_send)
        self.sleep_btn.clicked.connect(self.sleep_send)
        self.tama_pic = QtWidgets.QLabel(parent=self.centralwidget)
        self.tama_pic.setGeometry(QtCore.QRect(150, 80, 101, 101))
        self.tama_pic.setStyleSheet("")
        self.tama_pic.setText("")
        self.tama_pic.setScaledContents(True)
        self.tama_pic.setObjectName("tama_pic")
        self.tama_pic1 = QtWidgets.QLabel(parent=self.centralwidget)
        self.tama_pic1.setGeometry(QtCore.QRect(150, 80, 101, 101))
        self.tama_pic1.setStyleSheet("")
        self.tama_pic1.setText("")
        self.tama_pic1.setScaledContents(True)
        self.tama_pic.raise_()
        self.update_tama()

    def send_message(self):
        text = self.inputArea.text()
        self.inputArea.clear()

        self.client.send_message(text)

    def new_message(self, msg):
        self.chatArea.append(msg)

    def update_tama(self):
        # self.mood_stat = self.localTama.mood
        # self.eat_stat = self.localTama.eat
        # self.sleep_stat = self.localTama.sleep
        if DB.client_tamagochi.eat == "0" and DB.client_tamagochi.sleep == "0" and DB.client_tamagochi.mood == "0":
            print("покойся с миром")

            self.tama_pic1.setPixmap(QtGui.QPixmap("tama_guis/src/grave.jpg"))
            self.tama_pic1.setObjectName("tama_picq")
            self.tama_pic1.raise_()
        if str(DB.client_tamagochi.name) == "black_cat":
            print("черный котек поставлен")
            self.tama_pic.setPixmap(QtGui.QPixmap("tama_guis/src/black_cat.jpg"))
        elif str(DB.client_tamagochi.name) == "white_cat":
            print("белый котек поставлен")
            self.tama_pic.setPixmap(QtGui.QPixmap("tama_guis/src/white_cat.jpg"))
        elif str(DB.client_tamagochi.name) == "google_dino":
            print("гугл поставлен")
            self.tama_pic.setPixmap(QtGui.QPixmap("tama_guis/src/dinozavr.jpg"))
        self.mood_stat.setText(str(DB.client_tamagochi.mood))
        self.eat_stat.setText(str(DB.client_tamagochi.eat))
        self.sleep_stat.setText(str(DB.client_tamagochi.sleep))
        print(self.mood_stat, self.mood_stat, self.sleep_stat)

    def eat_send(self):
        self.client.send_eat()

    def mood_send(self):
        self.client.send_mood()

    def sleep_send(self):
        self.client.send_sleep()


class LoadingWindow(QMainWindow, Ui_LoadWindowGUI):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


class ErrorWindow(QMainWindow, Ui_ErrorWindowGUI):
    def __init__(self, menu_window):
        super().__init__()
        self.setupUi(self)
        self.menu_window = menu_window
        self.backToMenuBTN.clicked.connect(self.back_to_menu)

    def back_to_menu(self):
        self.hide()
        QApplication.quit()


class RegConnWindow(QMainWindow, Ui_RegConnWindowGUI):
    def __init__(self, client, clientNick, char_window, error_window, room_window):
        super().__init__()
        self.clientNick = clientNick
        self.setupUi(self)
        self.client = client
        self.char_window = char_window
        self.error_window = error_window
        self.room_window = room_window
        self.sendNickBTN.clicked.connect(self.accept_nick_conn)

    def accept_nick_conn(self):
        self.clientNick: str = self.nickLineEdit.text()
        self.whereToConnect: str = self.nickToConnLineEdit.text()
        print(self.clientNick, "подключается к", self.whereToConnect)
        try:
            self.connect_to_server()
            self.client.send_nickname(self.clientNick, "join", self.whereToConnect)
            self.hide()
        except:
            self.hide()
            self.error_window.show()

    def connect_to_server(self):
        self.client.just_connect()


class MyWindow(QMainWindow):
    signal = pyqtSignal(str)
    signalMessage = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()
        self.setFixedSize(400, 500)
        self.setStyleSheet("background-color: #2b2b2b;")
        self.client = ClientCommunication(4096, ('127.0.0.1', 8007))
        self.client.message_sent.connect(self.signal_from_server)
        self.client.message_signal.connect(self.msg_signal)
        self.clientNick = "username"

        self.gui = Ui_MenuWindowGUI()
        self.gui.setupUi(self)
        self.load_window = LoadingWindow()
        self.error_window = ErrorWindow(self.gui)
        self.room_window = RoomWindow(self.client)
        self.char_window = CharacterWindow(self.client, self.error_window, self.room_window)
        self.registation_window = RegWindow(self.client, self.clientNick, self.char_window, self.error_window)
        self.registation_connect_window = RegConnWindow(self.client, self.clientNick, self.char_window,
                                                        self.error_window, self.room_window)

        self.gui.createRoomBTN.clicked.connect(self.reg_win_show)
        self.gui.joinRoomBTN.clicked.connect(self.join_room)
        self.gui.leftGameBTN.clicked.connect(self.left_game)

    def reg_win_show(self):
        self.hide()
        self.registation_window.show()

    def join_room(self):
        self.hide()
        self.registation_connect_window.show()

    def left_game(self):
        QApplication.quit()

    def msg_signal(self, line, msg):
        if line == "new_message":
            self.room_window.new_message(msg)

    def signal_from_server(self, line):
        print("GUI", line)
        if line == "tama_not_exist_can_create":
            self.char_window.show()
        elif line == "tama_exist_cannot_create":
            self.error_window.show()
        elif line == "tama_not_exist_cannot_join":
            self.error_window.show()
        elif line == "tama_can_join":
            self.room_window.show()
            # Обработку тамогчи и передать окну которая тамагочи
        elif line == "update_tama":
            self.room_window.update_tama()
        elif line == "ops_error":
            self.error_window.show()


if __name__ == '__main__':
    app = QApplication([])
    window = MyWindow()
    window.show()
    app.exec()

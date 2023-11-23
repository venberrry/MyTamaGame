import socket
from common.ClientUtils import Utils
from threading import Thread
import pickle
from datetime import datetime
import time
from PyQt6.QtCore import pyqtSignal, QObject

class RecvFromServer(Thread):
    def __init__(self, sock, addr, buff):
        super().__init__(daemon=True)
        self.sock = sock
        self.addr = addr
        self.buff = buff

    def run(self):
        try:
            while True:
                    ut = Utils(self.buff)
                    pickle_pack = ut.recv_full_pickle(self.sock)
                    pack = pickle.loads(pickle_pack)
                    type = pack.get("type")
                    if type == "text":
                        print("[", datetime.now().hour, ':',
                               datetime.now().minute, ':',
                               datetime.now().second,'] (', pack.get("nick"), ")",
                               ':', pack.get("data"), "\n")
                        # self.ui_widget_room.chatArea.append("[", datetime.now().hour, ':',
                        #        datetime.now().minute, ':',
                        #        datetime.now().second,'] (', pack.get("nick"), ")",
                        #        ':', pack.get("data"), "\n")
                        # self.ui_widget_room.chatArea.append('FFFFF\n')
                    elif type == "welcome":
                        pass
                    elif type == "updates":
                        stats = pack.get("data")
                    print(stats)
        except Exception as err:
            print("----------DISCONECT1")
            print(f"При получении данных возникла ошибка: {err}")
            print("----------DISCONECT1")


class ClientCommunication(Thread):
    message_sent = pyqtSignal(str)

    def __init__(self, buff, address):
        super().__init__(daemon=True)
        self.buff = buff
        self.address = address
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('localhost', 0))

    def get_client_nickname(self):
        print("Введите свой ник:")
        self.nickname = str(input())

    def client_send_text(self, temp_type, msg):
        print('отправляю')
        try:
            data_new = dict()
            if temp_type == "text":
                data = {
                    'type': temp_type,
                    'data': msg,
                    'optional': ""
                }
                print(data)
                data_new = pickle.dumps(data)

            self.sock.send(data_new + b'OK')
            print('отправлено')
        except Exception as err:
            print("DISCONNECT2")
            self.stacked_widget.setCurrentWidget(self.ui_widget_error)

    def first_send_nickname(self, clientNickname):
        temp_type: str = "nickname_create_room"
        data = {
            'type': temp_type,
            'data': clientNickname,
            'optional': None
        }
        data_new = pickle.dumps(data)
        try:
            print('передаю пикл с именем')
            self.sock.send(data_new + b'OK')
        except:
            print("DISCONNECT4")
            self.stacked_widget.setCurrentWidget(self.ui_widget_error)

    def first_send_character(self, clientChar: str):
        print('tyyyyyt2')
        temp_type: str = "client_character"
        data = {
            'type': temp_type,
            'data': clientChar,
            'optional': None
        }
        data_new = pickle.dumps(data)
        try:
            print('передаю пикл с ТАМАГОЧЕЙ')
            self.sock.send(data_new + b'OK')
        except:
            print("DISCONNECT4")
            self.stacked_widget.setCurrentWidget(self.ui_widget_error)

    def connect_create_room(self, clientNickname, clientChar):
        try:
            print('начинаю подключение и передачу ника', clientNickname, clientChar)
            self.sock.connect(self.address)
            recv_cycle = RecvFromServer(self.sock, self.address, self.buff)
            recv_cycle.start()
            self.first_send_nickname(clientNickname)
            print('tyyyyyt')
            time.sleep(2)
            self.first_send_character(clientChar)
            print('tyyyyyt')
        except Exception as err:
            print("DISCONNECT3")
            self.stacked_widget.setCurrentWidget(self.ui_widget_error)

    def first_get_info(self):
        temp_type: str = "connection"
        data = {
            'type': temp_type,
            'data': None,
            'optional': None
        }
        data_new = pickle.dumps(data)
        try:
            print('передаю пикл с именем')
            self.sock.send(data_new + b'OK')
        except:
            print("DISCONNECT4")
            self.stacked_widget.setCurrentWidget(self.ui_widget_error)

    def connect_to_serv(self, clientNickname):
        try:
            print('начинаю подключение и передачу ника', clientNickname)
            self.sock.connect(self.address)
            recv_cycle = RecvFromServer(self.sock, self.address, self.buff)
            recv_cycle.start()
            self.first_send_nickname(clientNickname)
            self.first_get_info()
        except Exception as err:
            print("DISCONNECT3")
            self.stacked_widget.setCurrentWidget(self.ui_widget_error)


if __name__ == '__main__':
    cl1 = ClientCommunication(10, ('127.0.0.1', 8007))
    print("created")
    print("open cli conn")
    cl1.connect_create_room()
    print("conn is over")
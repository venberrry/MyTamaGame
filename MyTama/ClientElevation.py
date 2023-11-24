import socket
from common.ClientUtils import Utils
from threading import Thread
import pickle
from datetime import datetime
import time
from PyQt6.QtCore import pyqtSignal, QObject, Qt, QThread, pyqtSignal

class RecvFromServer(QThread):
    my_signal = pyqtSignal(str)
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
                    elif type == "nickname":
                        print("nick был принят", pack.get("data"))
                    elif type == "tamagochi_exist":
                        print("трунь")
                        self.my_signal.emit("Im alive")
                        print("Заходим в комнату с существующим тамагочи")
                    elif type == "tamagochi_not_exist":
                        print("соре, вам некуда заходить")
                    elif type == "updates":
                        stats = pack.get("data")
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

    def send_nickname(self, clientNick: str):     # РАБОТАЕТ
        temp_type: str = "nickname"
        data = {
            'type': temp_type,
            'data': clientNick,
            'optional': None
        }
        data_new = pickle.dumps(data)
        self.sock.send(data_new + b'OK')

    def send_character(self, clientChar: str):    # РАБОТАЕТ
        temp_type: str = "character"
        data = {
            'type': temp_type,
            'data': clientChar,
            'optional': None
        }
        data_new = pickle.dumps(data)
        self.sock.send(data_new + b'OK')

    def just_connect(self):      # РАБОТАЕТ
        self.sock.connect(self.address)
        recv_cycle = RecvFromServer(self.sock, self.address, self.buff)
        recv_cycle.start()



if __name__ == '__main__':
    cl1 = ClientCommunication(10, ('127.0.0.1', 8007))
    print("created")
    print("open cli conn")
    cl1.just_connect()
    print("conn is over")
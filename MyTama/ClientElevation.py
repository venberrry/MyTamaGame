import socket
from common.ClientUtils import Utils
from threading import Thread
import pickle
from datetime import datetime

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
                    elif type == "file":
                        info = pack.get("data")
                        print(info)
                        with open(pack.get("optional"), 'wb') as file:
                            file.write(info + "Proverka".encode("UTF-8"))
                        print("You got file named:", pack.get("optional"))
                    elif type == "welcome":
                        pass
        except Exception as err:
            print("DISCONECT1")
            print(f"При получении данных возникла ошибка: {err}")
            print("DISCONECT1")


class ClientCommunication(Thread):
    def __init__(self, buff, address):
        super().__init__(daemon=True)
        self.buff = buff
        self.address = address
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('localhost', 0))

    def get_client_nickname(self):
        print("Введите свой ник:")
        self.nickname = str(input())

    def client_send_text(self, temp_type):
        try:
            data_new = dict()
            if temp_type == "text":
                message = ''
                try:
                    message = input("Ввод текста: ")
                    if message == "exit":
                        self.sock.close()
                except Exception as something_bad:
                    print("Кажется клиент отвалился:", something_bad)
                    self.sock.close()

                data = {
                    'type': temp_type,
                    'data': message,
                    'optional': ""
                }
                data_new = pickle.dumps(data)

            if temp_type == "file":
                message = ''
                info = bytearray()
                try:
                    message = str(input("Ввод имя файла:"))
                    print(message)
                    if message == "exit":
                        self.sock.close()
                        info = bytearray()
                    with open(message, 'rb') as file:
                        while lines := file.read():
                            info.extend(lines)
                except Exception as something_bad:
                    print("Кажется клиент отвалился:", something_bad)
                    self.sock.close()

                data = {
                    'type': temp_type,
                    'data': info,
                    'optional': message
                }
                data_new = pickle.dumps(data)

            if temp_type == "welcome":
                nick = ''
                try:
                    nick = input("Ввод ника: ")
                    if nick == "exit":
                        self.sock.close()
                except Exception as something_bad:
                    print("Кажется клиент отвалился:", something_bad)
                    self.sock.close()

                data = {
                    'type': temp_type,
                    'data': nick,
                    'optional': nick
                }
                data_new = pickle.dumps(data)

            return data_new
        except Exception as err:
            print("DISCONNECT2")

    def first_send_nickname(self, clientNickname):
        temp_type: str = "nickname"
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



    def connect(self, clientNickname):
        try:
            print('начинаю подключение и передачу ника', clientNickname)
            self.sock.connect(self.address)
            recv_cycle = RecvFromServer(self.sock, self.address, self.buff)
            recv_cycle.start()
            self.first_send_nickname(clientNickname)
            # while True:
            #     try:
            #         temp_type = input("Что вы хотите передать? (text/file/welcome)\n")
            #         data = self.client_send_text(temp_type)
            #         self.sock.send(data + b'OK')
            #     except KeyboardInterrupt:
            #         print("Вы отвалились: ")
            #         self.sock.close()
        except Exception as err:
            print("DISCONNECT3")
            self.stacked_widget.setCurrentWidget(self.ui_widget_error)


if __name__ == '__main__':
    cl1 = ClientCommunication(10, ('127.0.0.1', 8007))
    print("created")
    print("open cli conn")
    cl1.connect()
    print("conn is over")
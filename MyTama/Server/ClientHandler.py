import random
from servcommon.ServUtils import Utils
from threading import Thread
import pickle
import multiprocessing

class Tamago():
    def __init__(self, name):
        self.name = name
        self.hunger = 10
        self.sleep = 10
        self.eat = 10

class ClientHandler(Thread):
    def __init__(self, sock, addr, buff, nickname, clies:list, tama):
        super().__init__()
        self.sock = sock
        self.addr = addr
        self.buff = buff
        self.nick_clie = nickname
        self.clies = clies
        self.tamagochi = tama

    def send_mes_all(self, pack):
        for cli in self.clies:
            try:
                cli.sock.send(pack + b'OK')
            except Exception as err:
                print(err)
                self.clies.remove(cli)

    def send_mes_not_all(self, pack):
        for cli in self.clies:
            if cli.sock != self.sock:
                try:
                    cli.sock.send(pack + b'OK')
                except Exception as err:
                    print(err)
                    self.clies.remove(cli)

    def pack_new_char_characteristics(self, tama):
        temp_type: str = "updates"
        data = {
            'type': temp_type,
            'data': tama,
            'optional': None
        }
        data_new = pickle.dumps(data)
        return data_new

    def send_new_tama_stats(self, pack):
        for cli in self.clies:
            try:
                cli.sock.send(pack + b'OK')
            except Exception as err:
                print(err)
                self.clies.remove(cli)

    def run(self):
        while True:
            try:
                ut = Utils(self.buff, self.clies, self.sock)
                pickle_pack = ut.recv_full_pickle(self.sock)
                print(pickle_pack)
                pack = pickle.loads(pickle_pack)
                print("~Server got:", pack)
                pack.update({"nick": self.nick_clie})
                new_pack = pickle.dumps(pack)
                type = pack.get("type")
                if type == "text":
                    self.send_mes_all(new_pack)
                elif type == "file":
                    self.send_mes_not_all(new_pack)
                elif type == "nickname_create_room":
                    self.nick_clie = pack.get("data")
                elif type == "client_character":
                    self.character = pack.get("data")
                    self.tamagochi = Tamago(self.character)
                    new_info_tama = self.pack_new_char_characteristics(self.tamagochi)
                    self.send_new_tama_stats(new_info_tama)
                elif type == "connection":
                    pack.update({"type": "updates"})
                    pack.update({"data": self.tamagochi})
                    new_pack = pickle.dumps(pack)
                    self.send_mes_not_all(new_pack)

            except Exception as err:
                print(err)
                break
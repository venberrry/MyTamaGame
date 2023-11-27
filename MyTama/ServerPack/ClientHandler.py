import random

from threading import Thread
import pickle
import multiprocessing
import time
import Tamagochi
from ServerPack.servcommon.ServUtils import Utils


class ClientHandler(Thread):
    def __init__(self, sock, addr, buff, nickname, clies:list, serv_tamago):
        super().__init__()
        self.sock = sock
        self.addr = addr
        self.buff = buff
        self.nick_clie = nickname
        self.clies = clies
        self.tamagochi = serv_tamago

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

    def send_mes_directly(self, new_pack):
        for cli in self.clies:
            if cli.sock == self.sock:
                try:
                    cli.sock.send(new_pack + b'OK')
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
                print("~ServerPack got:", pack)
                pack.update({"nick": self.nick_clie})
                new_pack = pickle.dumps(pack)
                type = pack.get("type")
                if type == "text":
                    self.send_mes_all(new_pack)
                elif type == "file":
                    self.send_mes_not_all(new_pack)
                elif type == "nickname":
                    self.nick_clie = pack.get("data")
                    conn_type = pack.get("optional")
                    print("Ник изменен", self.nick_clie)
                    print("CH NICK", self.tamagochi)
                    print("CH NICK", self.tamagochi.name)
                    print("CH NICK", self.tamagochi.creator)
                    if conn_type == "create" and self.tamagochi.name == "ff":
                        pack.update({"type": "tama_not_exist_can_create"})
                        pack.update({"data": self.tamagochi})
                        pack.update({"optional": ""})
                        new_pack = pickle.dumps(pack)
                        self.send_mes_directly(new_pack)
                    elif conn_type == "create" and self.tamagochi.name != "ff":
                        pack.update({"type": "tama_exist_cannot_create"})
                        pack.update({"data": ""})
                        pack.update({"optional": ""})
                        new_pack = pickle.dumps(pack)
                        self.send_mes_directly(new_pack)
                    elif conn_type == "join" and self.tamagochi.name == "ff":
                        pack.update({"type": "tama_not_exist_cannot_join"})
                        pack.update({"data": ""})
                        pack.update({"optional": ""})
                        new_pack = pickle.dumps(pack)
                        self.send_mes_directly(new_pack)
                    elif conn_type == "join" and self.tamagochi.name != "ff":
                        pack.update({"type": "tama_can_join"})
                        pack.update({"data":  self.tamagochi})
                        pack.update({"optional": ""})
                        new_pack = pickle.dumps(pack)
                        self.send_mes_directly(new_pack)
                elif type == "character":
                    self.character = pack.get("data")
                    self.tamagochi.name = self.character
                    self.tamagochi.creator = self.nick_clie

                    print("ТАМАГОЧИ СОЗДАН")
                    print("CH", self.tamagochi)
                elif type == "eat_up":
                    if int(self.tamagochi.eat) + 10 <= 100 and int(self.tamagochi.sleep) - 5 >= 0:
                        self.tamagochi.eat = str(int(self.tamagochi.eat) + 10)
                        self.tamagochi.sleep = str(int(self.tamagochi.sleep) - 5)
                    pack.update({"type": "update"})
                    pack.update({"data": self.tamagochi})
                    pack.update({"optional": ""})
                    new_pack = pickle.dumps(pack)
                    self.send_mes_all(new_pack)
                elif type == "mood_up":
                    if int(self.tamagochi.mood) + 10 <= 100 and int(self.tamagochi.eat) - 5 >= 0 :
                        self.tamagochi.mood = str(int(self.tamagochi.mood) + 10)
                        self.tamagochi.eat = str(int(self.tamagochi.eat) - 5)
                    pack.update({"type": "update"})
                    pack.update({"data": self.tamagochi})
                    pack.update({"optional": ""})
                    new_pack = pickle.dumps(pack)
                    self.send_mes_all(new_pack)
                elif type == "sleep_up":
                    if int(self.tamagochi.sleep) + 10 <= 100 and int(self.tamagochi.mood) - 5 >= 0:
                        self.tamagochi.sleep = str(int(self.tamagochi.sleep) + 10)
                        self.tamagochi.mood = str(int(self.tamagochi.mood) - 5)
                    pack.update({"type": "update"})
                    pack.update({"data": self.tamagochi})
                    pack.update({"optional": ""})
                    new_pack = pickle.dumps(pack)
                    self.send_mes_all(new_pack)
                elif type == "message":
                    pack["type"] = "new_message"
                    pack["data"] = str(self.nick_clie + " : " + pack.get("data"))
                    new_pack = pickle.dumps(pack)
                    self.send_mes_all(new_pack)

            except Exception as err:
                print(err)
                break
import random
from servcommon.ServUtils import Utils
from threading import Thread
import pickle
import multiprocessing
import time
import Tamagochi

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

    def send_mes_directly(self, new_pack, sender):
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
                print("~Server got:", pack)
                pack.update({"nick": self.nick_clie})
                new_pack = pickle.dumps(pack)
                type = pack.get("type")
                if type == "text":
                    self.send_mes_all(new_pack)
                elif type == "file":
                    self.send_mes_not_all(new_pack)
                elif type == "nickname":
                    self.nick_clie = pack.get("data")
                    print("Ник изменен", self.nick_clie)
                    pack.update({"type": "nickname"})
                    pack.update({"data": self.nick_clie})
                    pack.update({"optional": ""})
                    self.send_mes_directly(new_pack, self.sock)
                    print("CH NICK", self.tamagochi)
                    print("CH NICK", self.tamagochi.name)
                    print("CH NICK", self.tamagochi.creator)
                    if self.tamagochi.name != "ff":
                        print("Тамагочи уже создан и упакован")
                        pack.update({"type": "tamagochi_exist"})
                        pack.update({"data": ""})
                        pack.update({"optional": ""})
                        new_pack = pickle.dumps(pack)
                        self.send_mes_directly(new_pack, self.sock)
                    else:
                        print("Тамагочи ещё не создан")
                        pack.update({"type": "tamagochi_not_exist"})
                        pack.update({"data": ""})
                        pack.update({"optional": ""})
                        new_pack = pickle.dumps(pack)
                        self.send_mes_directly(new_pack, self.sock)
                elif type == "character":
                    self.character = pack.get("data")
                    self.tamagochi.name = self.character
                    self.tamagochi.creator = self.nick_clie
                    #self.tamagochi = Tamagochi.create_tama(self.character, self.nick_clie)

                    print("ТАМАГОЧИ СОЗДАН")
                    print("CH", self.tamagochi)
                elif type == "connection":
                    pack.update({"type": "updates"})
                    pack.update({"data": self.tamagochi})
                    new_pack = pickle.dumps(pack)
                    self.send_mes_not_all(new_pack)

            except Exception as err:
                print(err)
                break
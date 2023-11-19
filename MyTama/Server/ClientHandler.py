from servcommon.ServUtils import Utils
from threading import Thread
import pickle

class ClientHandler(Thread):
    def __init__(self, sock, addr, buff, nickname, clies:list):
        super().__init__()
        self.sock = sock
        self.addr = addr
        self.buff = buff
        self.nick_clie = nickname
        self.clies = clies

    def send_mes_all(self, pack):
        for cli in self.clies:
            if cli.is_alive():
                try:
                    print(cli.is_alive())
                    cli.sock.send(pack + b'OK')
                    print(self.clies)
                except Exception as err:
                    print(err)
                    print(self.addr)
        for cli in self.clies:
            if not(cli.is_alive()):
                self.clies.remove(cli)

    def send_mes_not_all(self, pack):
        for cli in self.clies:
            if cli.sock != self.sock:
                try:
                    cli.sock.send(pack + b'OK')
                except Exception as err:
                    print(err)

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
                if type == "nickname":
                    self.send_mes_all(new_pack)
                elif type == "file":
                    self.send_mes_not_all(new_pack)
                elif type == "welcome":
                    self.nick_clie = pack.get("data")
            except Exception as err:
                print(err)
                break
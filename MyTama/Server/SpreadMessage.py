import socket
from servcommon.ServUtils import Utils
from threading import Thread
import pickle

class SpreadMeassage:
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
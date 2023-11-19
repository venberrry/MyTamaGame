import socket
from servcommon.ServUtils import Utils
from threading import Thread
import pickle
import multiprocessing
from ClientHandler import ClientHandler

class Serv:
    def __init__(self, buff, address):
        self.buff = buff
        self.address = address
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clies = []
        self.rooms = {}

    def prep(self):
        self.sock.bind(self.address)
        self.sock.listen(2)

    def connect(self):
        while True:
            print(self.clies)
            conn, address = self.sock.accept()
            print(f"NEW CONNECT: {address}")
            clie_nickname = address[0]
            clie = ClientHandler(conn, address, self.buff, clie_nickname, self.clies)
            clie.start()
            self.clies.append(clie)


if __name__ == '__main__':
    s1 = Serv(10, ('127.0.0.1', 8007))
    print("created")
    s1.prep()
    print("prep done")
    s1.connect()
    print("conn is over")
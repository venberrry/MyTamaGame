import multiprocessing
import socket

from ServerPack.Tamagochi import Tamago, Life
from servcommon.ServUtils import Utils
from threading import Thread
import pickle
from multiprocessing import Process, Pipe
import time
from ClientHandler import ClientHandler

class Serv:
    def __init__(self, buff, address):
        self.buff = buff
        self.address = address
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clies = []
        # self.life = Life(self.serv_tamago)

    def prep(self):
        self.sock.bind(self.address)
        self.sock.listen(2)

    def connect(self):
        while True:
            conn, address = self.sock.accept()
            print(f"NEW CONNECT: {address}")
            clie_nickname = address[0]
            clie = ClientHandler(conn, address, self.buff, clie_nickname, self.clies)
            # if not self.gameStarted:
            #     self.life.start()
            #     self.gameStarted = True
            # self.life.clients.append(clie)
            clie.start()
            self.clies.append(clie)

s1 = Serv(10, ('127.0.0.1', 8007))
print("created")
s1.prep()
print("prep done")
s1.connect()
print("conn is over")

import pickle
from threading import Thread
import time




class Life(Thread):
    def __init__(self, tama):
        super().__init__()
        self.clients = []
        self.tama:Tamago = tama

    def run(self):
        while True:
            self.tama.get_low()
            for client in self.clients:
                pack = {}
                pack.update({"type": "update"})
                pack.update({"data": self.tama})
                pack.update({"optional": ""})
                new_pack = pickle.dumps(pack)
                client.send_mes_directly(new_pack)
            print("Yes")
            time.sleep(20)


class Tamago:
    def __init__(self, name, creator):
        self.creator = creator
        self.name = name
        self.mood = "50"
        self.sleep = "50"
        self.eat = "50"
        self.get_low()

    def get_low(self):
        if int(self.mood) - 5 >= 0:
            self.mood = str(int(self.mood) - 5)
        if int(self.eat) - 5 >= 0:
            self.eat = str(int(self.eat) - 5)
        if int(self.sleep) - 5 >= 0:
            self.sleep = str(int(self.sleep) - 5)

def create_tama(name, creator):
    my_tama = Tamago(name, creator)
    return my_tama
    print('я живой')
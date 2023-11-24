from threading import Thread
import time

class Tamago:
    def __init__(self, name, creator):
        self.creator = creator
        self.name = name
        self.hunger = 10
        self.sleep = 10
        self.eat = 10

    def getting_low(self):
        pass

def create_tama(name, creator):
    my_tama = Tamago(name, creator)
    return my_tama
    print('я живой')
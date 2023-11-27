import socket
import pickle
from ServerPack.Tamagochi import Tamago

class Utils:
    def __init__(self, buffer_size):
        self.buffer_size = buffer_size

    def recv_full_pickle(self, connection: socket):
        result = bytearray()
        while True:
            try:
                pickle_bytecode = connection.recv(self.buffer_size)
                data = pickle_bytecode
            except Exception as error:
                print(f"При получении данных возникла ошибка: {error}")
                return
            else:
                if not data:
                    return
                # проверка на окончание передачи, что были все пакеты переданы
                result.extend(data)
                if result[-2:] == b'OK':
                    break

        return result


    def recv_full_data(self, connection: socket):
        result = bytearray()
        while True:
            try:
                pickle_pack = connection.recv(self.buffer_size)
                data = pickle.loads(pickle_pack)
                print(f"Gooooot {data}")
            except Exception as error:
                print(f"При получении данных возникла ошибка: {error}")
                return
            else:
                if not data:
                    return
                # проверка на окончание передачи, что были все пакеты переданы
                result.extend(data)
                if result[-2:] == b'OK':
                    break
        return result

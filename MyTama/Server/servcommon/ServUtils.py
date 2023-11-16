import socket
import pickle

class Utils:
    def __init__(self, buffer_size, clies, sock):
        self.buffer_size = buffer_size
        self.clies = clies
        self.sock = sock

    def recv_full_pickle(self, connection: socket):
        result = bytearray()
        while True:
            try:
                pickle_bytecode = connection.recv(self.buffer_size)
                data = pickle_bytecode
                # data = pickle.loads(pickle_bytecode)
                # res = self.define_pack(data)
                # print(f"Got {data}")
            except Exception as error:
                print("ZASHELLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL")
                for cli in self.clies:
                    if cli.sock != self.sock:
                        self.clies.remove(cli)
                print(f"При получении данных возникла ошибка: {error}")
                return
            else:
                if not data:
                    return
                # проверка на окончание передачи, что были все пакеты переданы
                result.extend(data)
                if result[-2:] == b'OK':
                    break

        # print('done')
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
        print('done')
        return result

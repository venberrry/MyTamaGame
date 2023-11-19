import multiprocessing
import time

class Room:
    def __init__(self, room_id):
        self.room_id = room_id
        self.members = []

    def add_member(self, member):
        self.members.append(member)

    def broadcast_message(self, message):
        for member in self.members:
            member.receive_message(f"Room {self.room_id}: {message}")

class Member:
    def __init__(self, member_id, room):
        self.member_id = member_id
        self.room = room

    def join_room(self):
        self.room.add_member(self)

    def send_message(self, message):
        self.room.broadcast_message(f"Member {self.member_id}: {message}")

    def receive_message(self, message):
        print(f"Member {self.member_id} received: {message}")

def room_process(room_id, room_pipe):
    room = Room(room_id)
    while True:
        if room_pipe.poll():
            message = room_pipe.recv()
            room.broadcast_message(f"External Message: {message}")
        time.sleep(1)

if __name__ == "__main__":
    # Создаем канал для обмена данными между процессами
    parent_conn, child_conn = multiprocessing.Pipe()

    # Создаем процесс для комнаты
    room_process = multiprocessing.Process(target=room_process, args=(1, child_conn))
    room_process.start()

    # Создаем несколько участников и добавляем их в комнату
    member1 = Member(1, room_process)
    member2 = Member(2, room_process)

    member1.join_room()
    member2.join_room()

    # Отправляем сообщение извне в комнату
    parent_conn.send("Hello from the outside!")

    # Отправляем сообщения от участников
    member1.send_message("Hi, everyone!")
    member2.send_message("How are you doing?")

    # Ожидаем завершения процесса комнаты
    room_process.join()

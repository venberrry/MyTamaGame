from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget


class WorkerThread(QThread):
    # Определение сигнала
    my_signal = pyqtSignal(str)

    def run(self):
        # Выполняем работу в фоновом потоке
        result = "Результат работы потока"

        # Отправляем сигнал с результатом
        self.my_signal.emit(result)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        layout = QVBoxLayout()

        # Кнопка для запуска потока
        button = QPushButton("Запустить поток")
        button.clicked.connect(self.start_thread)

        layout.addWidget(button)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def start_thread(self):
        # Создаем и запускаем поток
        self.thread = WorkerThread()
        self.thread.my_signal.connect(self.handle_signal)
        self.thread.start()

    def handle_signal(self, result):
        # Обрабатываем сигнал из потока
        print(result)


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()

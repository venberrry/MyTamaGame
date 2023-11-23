from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys

class Paint(QMainWindow):
    save_finished = pyqtSignal()
    def __init__(self):
        super().__init__()

        self.setFixedSize(400, 500)
        self.setStyleSheet("background-color: #2b2b2b;")

        self.image = QImage(300, 300, QImage.Format_RGB32)
        self.image.fill(Qt.white)

        self.drawing = False
        self.brushSize = 7

        self.lastPoint = QPoint()

        self.canvas = Canvas(self)
        self.setCentralWidget(self.canvas)

        save_button = QPushButton("Save", self)
        save_button.clicked.connect(self.save)

        black_button = QPushButton("Black", self)
        black_button.clicked.connect(lambda: self.setColor(Qt.black))
        white_button = QPushButton("White", self)
        white_button.clicked.connect(lambda: self.setColor(Qt.white))
        green_button = QPushButton("Green", self)
        green_button.clicked.connect(lambda: self.setColor(Qt.green))
        yellow_button = QPushButton("Yellow", self)
        yellow_button.clicked.connect(lambda: self.setColor(Qt.yellow))
        red_button = QPushButton("Red", self)
        red_button.clicked.connect(lambda: self.setColor(Qt.red))

        save_button.setStyleSheet("font-family: Franklin Gothic Demi; font-size: 8pt; color: white;")
        black_button.setStyleSheet("font-family: Franklin Gothic Demi; font-size: 8pt;color: white;")
        white_button.setStyleSheet("font-family: Franklin Gothic Demi; font-size: 8pt;color: white;")
        green_button.setStyleSheet("font-family: Franklin Gothic Demi; font-size: 8pt;color: white;")
        yellow_button.setStyleSheet("font-family: Franklin Gothic Demi; font-size: 8pt;color: white;")
        red_button.setStyleSheet("font-family: Franklin Gothic Demi; font-size: 8pt;color: white;")

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.canvas)

        color_layout = QHBoxLayout()
        color_layout.addWidget(black_button)
        color_layout.addWidget(white_button)
        color_layout.addWidget(green_button)
        color_layout.addWidget(yellow_button)
        color_layout.addWidget(red_button)

        self.layout.addLayout(color_layout)
        self.layout.addWidget(save_button)

        central_widget = QWidget(self)
        central_widget.setLayout(self.layout)

        self.setCentralWidget(central_widget)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.lastPoint = self.canvas.mapFromGlobal(event.globalPos())

    def mouseMoveEvent(self, event):
        if (event.buttons() & Qt.LeftButton) & self.drawing:
            painter = QPainter(self.canvas.image)
            painter.setPen(QPen(self.canvas.brushColor, self.brushSize,
                                Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))

            currentPoint = self.canvas.mapFromGlobal(event.globalPos())
            painter.drawLine(self.lastPoint, currentPoint)

            self.lastPoint = currentPoint
            self.canvas.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False

    def save(self):
        self.saved_canvas = self.canvas.image.copy()
        self.saved_canvas.save("output.png")
        self.save_finished.emit()

    def setColor(self, color):
        self.canvas.brushColor = color

class Canvas(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.image = QImage(self.size(), QImage.Format_RGB32)
        self.image.fill(Qt.white)
        self.brushColor = Qt.black

    def paintEvent(self, event):
        canvasPainter = QPainter(self)
        canvasPainter.drawImage(self.rect(), self.image, self.image.rect())

    def resizeEvent(self, event):
        self.image = QImage(self.size(), QImage.Format_RGB32)
        self.image.fill(Qt.white)

if __name__ == "__main__":
    App = QApplication(sys.argv)
    window = Paint()
    window.show()
    sys.exit(App.exec())

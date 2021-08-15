import sys

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QVBoxLayout, QWidget
import rx
import rx.operators as rxop
from rx.subject import Subject


class CPUBoardWindow(QMainWindow):
    def __init__(self, clock_control):
        super().__init__()

        self.setWindowTitle("CPU")

        self.button = QPushButton("Stop the clock!")
        self.button.clicked.connect(self.button_clicked)

        self.label = QLabel()

        layout = QVBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(self.label)

        container = QWidget()
        container.setLayout(layout)

        self.setFixedSize(QSize(800, 600))

        self.setCentralWidget(container)

        self.clock_control = clock_control

    def button_clicked(self):
        self.clock_control.on_completed()
        self.label.setText("Clock stopped")

    def count(self, item):
        self.label.setText(str(item))


def main():
    app = QApplication(sys.argv)

    clock_source = rx.interval(1)
    clock_control = Subject()

    window = CPUBoardWindow(clock_control)
    window.show()

    clock_source.subscribe(clock_control)
    clock_control.subscribe(window.count)

    app.exec()


if __name__ == '__main__':
    main()

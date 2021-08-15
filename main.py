import sys

from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QVBoxLayout, QWidget
import rx
import rx.operators as rxop


class CPUBoardWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("CPU")

        self.button = QPushButton("Press Me!")
        self.button.clicked.connect(self.button_clicked)

        self.label = QLabel()

        layout = QVBoxLayout()
        layout.addWidget(self.button)
        layout.addWidget(self.label)

        container = QWidget()
        container.setLayout(layout)

        self.setFixedSize(QSize(800, 600))

        self.setCentralWidget(container)

    def button_clicked(self):
        self.label.setText("The button was clicked")

    def count(self, item):
        self.label.setText(str(item))


def main():
    app = QApplication(sys.argv)
    window = CPUBoardWindow()
    window.show()

    rx.interval(2).subscribe(window.count)

    app.exec()


if __name__ == '__main__':
    main()

from physical.elements import Pin
import sys

from PySide6.QtWidgets import QApplication, QMainWindow

from gui.cpu import QClockModule
from circuits.cpumodules import ClockModule

clock = ClockModule()


class Main(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        clock_module = QClockModule(clock)

        self.setCentralWidget(clock_module)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    app.aboutToQuit.connect(Pin.disconnect_all)
    app.exec()

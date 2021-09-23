from enum import auto, Enum

from PySide6.QtCore import QSize, Signal
from PySide6.QtWidgets import QLabel


class State(Enum):
    ON = auto()
    OFF = auto()

    def switch(self):
        if self == State.ON:
            return State.OFF
        elif self == State.OFF:
            return State.ON


class COLOR(Enum):
    BLUE = {
        State.OFF: '#0c2c45',
        State.ON: '#2f8dda'
    }

    def to_style(self, state):
        return f'background: {self.value[state]}'


class _Diode(QLabel):

    set_signal = Signal(State)

    def __init__(self, *args, color=COLOR.BLUE, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFixedSize(QSize(30, 30))
        self.setText('')
        self._color = color
        self._state = State.OFF
        self._set_style()
        self.set_signal.connect(self._set_state)

    def _set_style(self):
        self.setStyleSheet(self._color.to_style(self._state))

    def set(self, state):
        self.set_signal.emit(state)

    def _set_state(self, state):
        if state:
            self._state = State.ON
        else:
            self._state = State.OFF
        self._set_style()


class BlueDiode(_Diode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, color=COLOR.BLUE, **kwargs)

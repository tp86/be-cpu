from math import log10

from PySide6.QtWidgets import (QDial, QGridLayout, QGroupBox, QLCDNumber,
                               QPushButton)

from gui.diodes import BlueDiode


class QClockModule(QGroupBox):
    _dial_resolution = 100

    def __init__(self, clock):
        super().__init__('Clock')

        self._clock = clock

        # Widgets
        self._freq_display = QLCDNumber()
        self._freq_display.setSegmentStyle(QLCDNumber.Flat)
        self._freq_display.setDigitCount(4)
        self._freq_display.display(self._clock.frequency)

        self._freq_dial = QDial()
        self._freq_dial.setValue(log10(self._clock.frequency))
        self._freq_dial.setRange(-1 * self._dial_resolution,
                                 1 * self._dial_resolution)
        self._freq_dial.setSingleStep(1)
        self._freq_dial.setNotchesVisible(True)
        self._freq_dial.valueChanged.connect(self._set_clock_frequency)

        self._mode_button = QPushButton()
        self._mode_button.setCheckable(True)
        self._mode_button.toggled.connect(self._set_mode)
        self._mode_button_set_text()

        self._manual_clock_button = QPushButton('Manual Trigger')
        self._manual_clock_button.pressed.connect(self._clock.high)
        self._manual_clock_button.released.connect(self._clock.low)

        self._clock_diode = BlueDiode()
        self._clock.CLK.subscribe(self._clock_diode.set)

        # Layout
        self._layout = QGridLayout()
        self._layout.addWidget(self._freq_display, 0, 0)
        self._layout.addWidget(self._freq_dial, 1, 0)
        self._layout.addWidget(self._mode_button, 0, 1)
        self._layout.addWidget(self._manual_clock_button, 1, 1)
        self._layout.setColumnMinimumWidth(1, 100)
        self._layout.addWidget(self._clock_diode, 0, 2, 2, 1)

        self.setLayout(self._layout)

    def _set_clock_frequency(self, dial_value):
        frequency = 10 ** (dial_value / self._dial_resolution)
        self._clock.frequency = frequency
        self._freq_display.display(self._clock.frequency)

    def _set_mode(self, checked):
        if checked:
            self._clock.manual()
        else:
            self._clock.auto()
        self._mode_button_set_text()

    def _mode_button_set_text(self):
        if self._mode_button.isChecked():
            mode = 'Manual'
        else:
            mode = 'Auto'
        self._mode_button.setText(f'Mode: {mode}')

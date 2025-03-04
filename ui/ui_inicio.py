from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *


class Ui_inicio(QFrame):
    def __init__(self, expanded):
        super().__init__()
        if expanded:
            self.setFixedSize(1050, 760)
        else:
            self.setFixedSize(1125, 760)

        self.setStyleSheet("background-color: #181818; border-radius: 10px;")

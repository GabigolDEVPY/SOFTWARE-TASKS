from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *


class Ui_inicio(QFrame):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #181818; border-radius: 10px;")
        self.setFixedSize(1125, 750)
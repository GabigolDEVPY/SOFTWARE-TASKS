from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *


class Ui_Concluidos(QFrame):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #800080")
        self.setFixedSize(800, 900)
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *

class ui_diarias(QFrame):
    def __init__(self):
        super().__init__()
        self.setFixedSize(820, 580)
        self.setStyleSheet("background-color: #8b00cc;")

from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *


class Ui_Concluidos(QFrame):
    def __init__(self, expanded):
        super().__init__()
        self.setStyleSheet("background-color: #525252; border-radius: 10px;")
        if expanded:
            self.setFixedSize(1050, 760)
        else:
            self.setFixedSize(1125, 760)
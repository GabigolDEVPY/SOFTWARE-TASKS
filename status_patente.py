from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from custom_sidebar import Sidebar
from tema import aplicar_tema_dark
import sys

class statusPatente(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(150, 50)
        self.setStyleSheet("background-color: #000000;")
        
        # criando widgets
        self.XPmenu = QLabel(" XP ")
        self.XPmenu.setStyleSheet("border-radius: None;")
        self.patente = QLabel("patente")
        self.patente.setStyleSheet("border-radius: None;")
        
        #criando layout
        self.layoutStatus = QHBoxLayout()
        self.layoutStatus.setSpacing(0)
        
        self.setLayout(self.layoutStatus)
        self.layoutStatus.addWidget(self.XPmenu)
        self.layoutStatus.addWidget(self.patente)
        
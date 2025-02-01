from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from custom_sidebar import Sidebar
from status_patente import statusPatente
import sys

class janela_principal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(900, 600)
        self.widget_central = QWidget()
        self.setCentralWidget(self.widget_central)
        self.CentralLayout = QHBoxLayout()
        self.widget_central.setStyleSheet("background-color: #161616;")
        
        # criando a sidebar
        self.sideBar = Sidebar(self)
        self.sideBar.setParent(self)
        
        # criando status pantente
        self.statusPatente = statusPatente()
        self.statusPatente.setContentsMargins(0, 0, 0, 20)
        
        
        self.widget_central.setLayout(self.CentralLayout)
        self.CentralLayout.addWidget(self.sideBar, alignment=Qt.AlignTop | Qt.AlignLeft)
        self.CentralLayout.addWidget(self.statusPatente, alignment=Qt.AlignTop)

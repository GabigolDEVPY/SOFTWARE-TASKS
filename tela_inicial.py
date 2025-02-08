from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from custom_sidebar import Sidebar
from status_patente import statusPatente
from ui.ui_diarias import ui_diarias
import sys

class janela_principal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(900, 600)
        self.widget_central = QWidget()
        self.setCentralWidget(self.widget_central)
        self.CentralLayout = QHBoxLayout()
        self.CentralLayout.setSpacing(0)
        self.CentralLayout.setContentsMargins(0, 0, 0, 0)
        self.widget_central.setStyleSheet("background-color: #161616;")
        
        # frame centro
        self.widgetcentro = QFrame()
        self.widgetcentro.setFixedSize(820, 600)
        self.widgetcentro.setStyleSheet("background-color: #2c2c2c;")
        
        # criando status patente
        self.status_patente = statusPatente()
        
        # criando a sidebar
        self.sideBar = Sidebar(self.status_patente)
        self.sideBar.btn_menu.clicked.connect(lambda: self.sideBar.toggle_sidebar())
        self.sideBar.setParent(self)
        
        # layout para o frma e o status patente
        self.Vlayout = QVBoxLayout()
        self.Vlayout.setContentsMargins(5, 0, 5, 5)
        self.Vlayout.addWidget(self.status_patente, alignment=Qt.AlignTop | Qt.AlignRight)
        self.Vlayout.addWidget(self.widgetcentro)
        
        # layout engloba tudo
        self.widget_central.setLayout(self.CentralLayout)
        self.CentralLayout.addWidget(self.sideBar, alignment=Qt.AlignTop | Qt.AlignLeft)
        self.CentralLayout.addLayout(self.Vlayout)


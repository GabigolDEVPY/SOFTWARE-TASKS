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
        self.XPmenu = QLabel(" XP")
        self.XPmenu.setStyleSheet("border-radius: None; color: #ffffff;")
        self.XPmenu.setFixedSize(25, 20)
        
        self.XP = QLabel("0")
        self.XP.setStyleSheet("border-radius: None; background-color: #30005f; color: #ffffff;")
        self.XP.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.XP.setFixedSize(60, 20)
        self.atualizar_patente()
        
    def atualizar_patente(self):
        if int(self.XP.text()) >= 1000:
            Pixmap = QPixmap("D:\WINDOWS\PROGRAMACAO_TUDO\SOFTWARE-TASKS\icons\patente.png")
        elif int(self.XP.text()) < 1000:
            Pixmap = QPixmap("D:\WINDOWS\PROGRAMACAO_TUDO\SOFTWARE-TASKS\icons\patente2.png")
            
            
        self.patente = QLabel()
        self.patente.setPixmap(Pixmap)
        self.patente.setFixedSize(50, 50)
        self.patente.setStyleSheet("border-radius: None; background-color: #30005f")
        self.patente.setScaledContents(True)
        self.patente.setContentsMargins(0, 0, 0, 10)
        
        #criando layout
        self.layoutStatus = QHBoxLayout()
        self.layoutStatus.setSpacing(0)
        
        self.setLayout(self.layoutStatus)
        self.layoutStatus.addWidget(self.XPmenu, alignment=Qt.AlignTop)
        self.layoutStatus.addWidget(self.XP, alignment=Qt.AlignTop)
        self.layoutStatus.addWidget(self.patente)
        
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
import os

local = os.path.dirname(os.path.abspath(__file__))
local_patentes = os.path.join(local, "icons")
patentes = [(i * 1000, os.path.join(local_patentes, f"Prancheta {i + 1}.png")) for i in range(111)]


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
        
        #criando layout
        self.layoutStatus = QHBoxLayout()
        self.layoutStatus.setSpacing(0)
        
        # criando patente
        self.patente = QLabel()
        self.patente.setFixedSize(50, 50)
        self.patente.setStyleSheet("border-radius: None; background-color: #30005f")
        self.patente.setScaledContents(True)
        self.patente.setContentsMargins(0, 0, 0, 10)
        
        self.setLayout(self.layoutStatus)
        self.layoutStatus.addWidget(self.XPmenu, alignment=Qt.AlignTop)
        self.layoutStatus.addWidget(self.XP, alignment=Qt.AlignTop)
        self.layoutStatus.addWidget(self.patente)
        
        self.atualizar_patente()
        
    def atualizar_patente(self):
        xp = int(self.XP.text())
        for i in range(111, -1, -1):
            if xp == (i) * 1000:
                Pixmap = QPixmap(patentes[i][1])
                self.patente.setPixmap(Pixmap)


            

        
        

from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
import os

local = os.path.dirname(os.path.abspath(__file__))
local_patentes = os.path.join(local, "icons")
patentes = [(i * 1000, os.path.join(local_patentes, f"Prancheta {i + 1}.png")) for i in range(111)]

class popUp(QDialog):
    def __init__(self, id, numero):
        super().__init__()
        self.setFixedSize(300, 300)
        self.setStyleSheet("Background-color: #161616;")
        
        #criando componentes
        self.VerticalLayout = QVBoxLayout()
        self.setLayout(self.VerticalLayout)
        self.label_patente = QLabel()
        self.label_parabens = QLabel("LEVEL AUMENTADO\n"
                                    f"           LEVEL {str(int(numero / 1000))}")
        
        self.label_parabens.setStyleSheet("font-size: 20px; color: #ffffff; font-weight: bold;")
        self.label_patente.setFixedSize(150, 150)
        self.label_patente.setScaledContents(True)
        
        self.botao = QPushButton("OK")
        self.botao.setStyleSheet("QPushButton {background-color: #30005f; font-size: 20px; font-weight: bold; color: #ffffff; border-radius: 1px;} QPushButton:Hover {background-color: #000000;}")
        self.botao.setFixedSize(150, 50)
        self.patente = QPixmap(id)
        self.label_patente.setPixmap(self.patente)
        
        self.VerticalLayout.addWidget(self.label_parabens, alignment=Qt.AlignCenter | Qt.AlignTop)
        self.VerticalLayout.addWidget(self.label_patente, alignment=Qt.AlignCenter)
        self.VerticalLayout.addWidget(self.botao, alignment=Qt.AlignCenter)
        self.botao.clicked.connect(lambda: self.close())
        
        self.show()
        self.exec()


class statusPatente(QFrame):
    def __init__(self):
        super().__init__()
        self.setFixedSize(820, 40)
        self.setStyleSheet("background-color: #30005f;")
        
        # criando widgets
        self.XPmenu = QLabel("XP")
        self.XPmenu.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.XPmenu.setStyleSheet("border-radius: None; color: #ffffff; background-color: #000000; font-size: 15px;")
        self.XPmenu.setFixedSize(35, 40)
        
        self.XP = QLabel("0")
        self.XP.setStyleSheet("border-radius: None; background-color: #161616; color: #ffffff; font-weight: semi-bold; font-size: 15px;")
        self.XP.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.XP.setFixedSize(70, 40)
        
        #criando layout
        self.layoutStatus = QHBoxLayout()
        self.layoutStatus.setContentsMargins(670, 0, 0, 0)
        self.layoutStatus.setSpacing(0)
        
        # criando patente
        self.patente = QLabel()
        self.patente.setFixedSize(50, 50)
        self.patente.setStyleSheet("border-radius: None; background-color: #30005f")
        self.patente.setScaledContents(True)
        self.patente.setContentsMargins(0, 0, 0, 10)
        
        self.setLayout(self.layoutStatus)
        self.layoutStatus.addWidget(self.XPmenu, alignment=Qt.AlignCenter)
        self.layoutStatus.addWidget(self.XP, alignment=Qt.AlignCenter)
        self.layoutStatus.addWidget(self.patente)
        
        self.patente_inicial()
        
    def patente_inicial(self):
        xp = int(self.XP.text())
        for i in range(111, -1, -1):
            if xp == (i) * 1000:
                Pixmap = QPixmap(patentes[i][1])
                self.patente.setPixmap(Pixmap)    
        
    def atualizar_patente(self):
        xp = int(self.XP.text())
        for i in range(111, -1, -1):
            if xp == (i) * 1000:
                Pixmap = QPixmap(patentes[i][1])
                popUp(patentes[i][1], patentes[i][0])
                self.patente.setPixmap(Pixmap)


            

        
        

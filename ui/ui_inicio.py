from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from backend import load_json
import os

local = os.path.dirname(os.path.abspath(__file__))
raiz = os.path.dirname(local)  # Volta uma pasta
local_patentes = os.path.join(raiz, "icons")
patentes = [(i * 1000, os.path.join(local_patentes, f"Prancheta {i + 1}.png")) for i in range(111)]


class framedireita(QFrame):
    def __init__(self, indice):
        super().__init__()
        self.setFixedSize(350, 600)
        self.setStyleSheet("background-color: #2C2F33; border-radius: 10px;")
        self.users = load_json.load_file()
        self.user = self.users[indice]

        self.central_layout = QVBoxLayout()
        self.setLayout(self.central_layout)

        self.texto_nivel = QLabel("NIVEL")
        self.Patente = QLabel()
        pixmap = QPixmap(patentes[1][1]) 
        self.Patente.setPixmap(pixmap)
        self.Patente.setFixedSize(300, 300)
        self.Patente.setScaledContents(True)
        self.central_layout.addWidget(self.texto_nivel, alignment=Qt.AlignTop | Qt.AlignCenter)
        self.central_layout.addWidget(self.Patente, alignment=Qt.AlignTop | Qt.AlignCenter)

        self.patente_inicial()  

    def patente_inicial(self):
        xp = int(self.user["xp"])
        print(xp)
        for i in range(111, -1, -1):
            if xp >= i * 1000:
                pixmap = QPixmap(patentes[i][1])
                self.Patente.setPixmap(pixmap)
                break
        
class frameesquerda(QFrame):
    def __init__(self):
        super().__init__()
        self.setFixedSize(650, 740)
        self.setStyleSheet("background-color: #2C2F33; border-radius: 10px;")
        



class Ui_inicio(QFrame):
    def __init__(self, expanded, indice):
        super().__init__()
        if expanded:
            self.setFixedSize(1050, 760)
        else:
            self.setFixedSize(1125, 760)
        self.setStyleSheet("background-color: #23272A; border-radius: 10px;")
        self.Central_layout = QHBoxLayout()
        self.Central_layout.setSpacing(10)
        self.setLayout(self.Central_layout)
        self.frame_esquerda = frameesquerda()
        self.frame_direita = framedireita(indice)
        self.spacer = QSpacerItem(30, 30)
        
        
        self.Central_layout.addWidget(self.frame_esquerda, alignment=Qt.AlignLeft)
        self.Central_layout.addWidget(self.frame_direita, alignment=Qt.AlignRight | Qt.AlignTop)
        self.Central_layout.addItem(self.spacer)
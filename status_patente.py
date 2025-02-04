from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
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
        
        self.XP = QLabel("1001")
        self.XP.setStyleSheet("border-radius: None; background-color: #30005f; color: #ffffff;")
        self.XP.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.XP.setFixedSize(60, 20)
        self.atualizar_patente()
        
    def atualizar_patente(self):
        print("123")
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
        
    def atualizar_xp(self):
        print("XP atualizado!")  # Para ver se está sendo chamado
        try:
            print(self.XP.text())
            novo_xp = int(self.XP.text()) + 100
            self.XP.setText("10099")
        except AttributeError:
            print("Erro: status_patente.XP não encontrado!")
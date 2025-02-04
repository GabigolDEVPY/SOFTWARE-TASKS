from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *

class StatusPatente(QWidget):
    def __init__(self):
        super().__init__()
        
        # Layout principal do widget
        self.setFixedSize(200, 100)
        self.layout = QVBoxLayout()

        # Widget para mostrar XP
        self.XP_label = QLabel("XP: 500")
        self.XP_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.XP_label)

        # Widget para mostrar ícone de patente
        self.patente_label = QLabel()
        self.layout.addWidget(self.patente_label)

        # Atualizando a patente conforme o XP
        self.atualizar_patente()

        # Setando o layout
        self.setLayout(self.layout)

    def atualizar_patente(self):
        # Verificando o valor do XP e atualizando o ícone
        xp = int(self.XP_label.text().split(":")[1].strip())
        if xp >= 1000:
            self.patente_label.setPixmap(QPixmap("patente_ouro.png"))
        else:
            self.patente_label.setPixmap(QPixmap("patente_prata.png"))

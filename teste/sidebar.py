from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *

class Sidebar(QWidget):
    def __init__(self, status_patente):
        super().__init__()
        
        # Recebendo o objeto de StatusPatente para manipular
        self.status_patente = status_patente
        
        # Layout do Sidebar
        self.layout = QVBoxLayout()

        # Botões do Sidebar
        self.botao_dashboard = QPushButton("Dashboard")
        self.botao_dashboard.clicked.connect(self.mudar_xp)
        self.layout.addWidget(self.botao_dashboard)

        # Setando o layout do Sidebar
        self.setLayout(self.layout)

    def mudar_xp(self):
        # Alterando o XP ao clicar no botão
        novo_xp = int(self.status_patente.XP_label.text().split(":")[1].strip()) + 100
        self.status_patente.XP_label.setText(f"XP: {novo_xp}")
        self.status_patente.atualizar_patente()

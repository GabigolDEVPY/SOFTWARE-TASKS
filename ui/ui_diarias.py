from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *

class ui_diarias(QFrame):
    def __init__(self, status_patente):
        super().__init__()
        self.setFixedSize(825, 555)
        self.setStyleSheet("background-color: #303030;")
        self.centralLayout = QVBoxLayout()
        self.setLayout(self.centralLayout)
        
        self.statusPatente = status_patente
        
        # criando widgets
        self.texto = QLabel("INICIO")
        self.listview = QStackedWidget()
        self.botao = QPushButton("CLIQUE AQUI")
        self.botao.clicked.connect(lambda: self.statusPatente.atualizar_xp())
        
        # add no layout
        
        self.centralLayout.addWidget(self.texto)
        self.centralLayout.addWidget(self.listview)
        self.centralLayout.addWidget(self.botao)

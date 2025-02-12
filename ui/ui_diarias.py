from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *




class botoes(QPushButton):
    def __init__(self, nome, altura, largura):
        super().__init__()
        self.setStyleSheet("QPushButton {background-color: #30005f; border-radius: None; color: #ffffff; font-weight: bold;} QPushButton:Hover {background-color: #000000;}")
        self.setText(nome)
        self.setMinimumSize(largura, altura)
        

class TaskLista(QWidget):
    def __init__(self):
        super().__init__()
        self.CentralLayout = QHBoxLayout(self)
        self.task_list = QListWidget()
        
        # layout botões
        self.layout_botoes = QVBoxLayout()
        self.layout_botoes.setAlignment(Qt.AlignTop)
        self.botao_adicionar = botoes("ADICIONAR", 40, 100)
        self.botao_excluir = botoes("EXCLUIR", 40, 100)
        self.layout_botoes.addWidget(self.botao_adicionar)
        self.layout_botoes.addWidget(self.botao_excluir)
        
        self.CentralLayout.addWidget(self.task_list)
        self.CentralLayout.addLayout(self.layout_botoes)
        



class ui_diarias(QFrame):
    def __init__(self, status_patente):
        super().__init__()
        self.setFixedSize(825, 555)
        self.setStyleSheet("background-color: #303030;")
        self.centralLayout = QVBoxLayout()
        self.centralLayout.setSpacing(0)
        self.setLayout(self.centralLayout)
        self.statusPatente = status_patente
        
        # criando widgets
        self.texto = QLabel("INICIO")
        self.texto.setMinimumSize(100, 24)
        self.texto.setStyleSheet("font-size: 24px; font-weight: bold; color: #ffffff;")
        self.tela_list = TaskLista()

        
        # add no layout
        
        self.centralLayout.addWidget(self.texto)
        self.centralLayout.addWidget(self.tela_list)

from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *

class dialog_tarefa(QDialog):
    def __init__(self, lista):
        super().__init__()
        self.lista = lista
        self.setStyleSheet("background-color: #303030;")
        self.setFixedSize(500, 500)
        self.central_layout = QVBoxLayout()
        self.setLayout(self.central_layout)
        self.titulo = QLabel("ADICIONAR TAREFA")
        self.titulo.setStyleSheet("font-size: 30px; color: #ffffff; font-weight: bold;")
        self.espaco = QSpacerItem(90, 90, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.linha_tarefa = QLabel("NOME DA TAREFA")
        self.linha_tarefa.setStyleSheet("font-size: 15px; color: #ffffff; font-weight: bold;")
        self.tarefa = QLineEdit()
        self.tarefa.setStyleSheet("color: #ffffff;")
        self.tarefa.setMinimumHeight(35)
        self.linha_descricao = QLabel("DESCRIÇÃO")
        self.linha_descricao.setStyleSheet("font-size: 15px; color: #ffffff; font-weight: bold;")
        self.descricao = QTextEdit()
        self.descricao.setStyleSheet("color: #ffffff;")
        self.botao_ok = botoes("OK", 45, 300)
        self.botao_cancelar = botoes("CANCELAR", 45, 300)
        
        # adicionando no layout
        self.central_layout.addWidget(self.titulo, alignment=Qt.AlignCenter)
        self.central_layout.addItem(self.espaco)
        self.central_layout.addWidget(self.linha_tarefa)
        self.central_layout.addWidget(self.tarefa)
        self.central_layout.addWidget(self.linha_descricao)
        self.central_layout.addWidget(self.descricao)
        self.central_layout.addWidget(self.botao_ok, alignment=Qt.AlignmentFlag.AlignCenter)
        self.central_layout.addWidget(self.botao_cancelar, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.botao_cancelar.clicked.connect(lambda: self.close())
        self.botao_ok.clicked.connect(lambda: add_task(self))
        
        def add_task(self):
            item = QListWidgetItem(self.lista)
            widget = Custom_widget(self.tarefa.text())
            item.setSizeHint(widget.sizeHint())
            self.lista.addItem(item)
            self.lista.setItemWidget(item, widget)
            widget.muda_cor()
            self.close()
            

        
        self.show()
        self.exec()


class botoes(QPushButton):
    def __init__(self, nome, altura, largura):
        super().__init__()
        self.setStyleSheet("QPushButton {background-color: #30005f; border-radius: None; color: #ffffff; font-weight: bold;} QPushButton:Hover {background-color: #000000;}")
        self.setText(nome)
        self.setFixedSize(largura, altura)
        
class Custom_widget(QWidget):
    def __init__(self, nome):
        super().__init__()
        self.central_layout = QHBoxLayout()
        self.setLayout(self.central_layout)
        self.checkbox = QCheckBox()
        self.checkbox.setStyleSheet("background: transparent;")
        self.checkbox.setFixedWidth(40)
        self.titulo = QLabel(nome)
        self.titulo.setStyleSheet("background: transparent; font-weight: bold; font-size: 15px; color: #ffffff;")
        self.prioridade = QComboBox()
        self.prioridade.setStyleSheet("border-radius: 2px; font-weight: bold; color: #ffffff;")
        self.prioridade.setFixedSize(95, 35)
        self.prioridade.addItems(["URGENTE", "RELEVANTE", "TRANQUILO"])
        self.prioridade.currentIndexChanged.connect(lambda: self.muda_cor())
        self.central_layout.addWidget(self.checkbox)     
        self.central_layout.addWidget(self.titulo)     
        self.central_layout.addWidget(self.prioridade)     
    

    def muda_cor(self):
        opcao = self.prioridade.currentText()
        
        if opcao == "URGENTE":
            self.setStyleSheet("background-color: #800000;")
        elif opcao == "RELEVANTE":
            self.setStyleSheet("background-color: #ff6600;")
        elif opcao == "TRANQUILO":
            self.setStyleSheet("background-color: #007a0a;")

        

class TaskLista(QWidget):
    def __init__(self):
        super().__init__()
        self.CentralLayout = QHBoxLayout(self)
        self.task_list = QListWidget()
        
        # layout botões
        self.layout_botoes = QVBoxLayout()
        self.layout_botoes.setAlignment(Qt.AlignTop)
        self.botao_adicionar = botoes("ADICIONAR", 35, 80)
        self.botao_excluir = botoes("EXCLUIR", 35, 80)
        self.layout_botoes.addWidget(self.botao_adicionar)
        self.layout_botoes.addWidget(self.botao_excluir)
        
        self.CentralLayout.addWidget(self.task_list)
        self.CentralLayout.addLayout(self.layout_botoes)
        
        self.botao_adicionar.clicked.connect(lambda: dialog_tarefa(self.task_list))
        
        



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

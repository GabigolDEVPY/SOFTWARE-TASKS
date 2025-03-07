from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from backend import load_json

class Custom_widget(QFrame):
    def __init__(self, nome, id, dificuldade, prioridade, indice, check):
        super().__init__()
        self.setStyleSheet("background-color: #23272A;")
        self.setMinimumHeight(70)

        def verificarXP(dificuldade):
            xp = 0
            if dificuldade == "DIFÍCIL":
                xp = 150

            elif dificuldade == "MEDIO":
                xp = 120

            elif dificuldade == "FÁCIL":
                xp = 100

            return str(xp)
        
        self.indice = indice
        self.central_layout = QHBoxLayout()
        self.setLayout(self.central_layout)
        self.Qprioridade = prioridade
        self.dificuldade = dificuldade
        self.id = id   
        self.titulo = QLabel(nome)
        self.titulo.setStyleSheet("background: transparent; font-weight: bold; font-size: 15px; color: #ffffff;")
        self.xp = QLabel(f"XP {verificarXP(self.dificuldade)}  ")
        self.xp.setStyleSheet("background: transparent; font-weight: bold; font-size: 15px; color: #ffffff;")
        self.central_layout.addWidget(self.titulo)     
        self.central_layout.addWidget(self.xp, alignment=Qt.AlignmentFlag.AlignRight)


        
        def qual_cor():
            
            xp_text = self.xp.text()
            xp_value = int(xp_text.split()[1])
            
            if xp_value == 150:
                self.setStyleSheet("background-color: #800000;")
            elif xp_value == 120:
                self.setStyleSheet("background-color: #ff6600;")
            elif xp_value == 100:
                self.setStyleSheet("background-color: #007a0a;")


                
        qual_cor()
        


        
class widget(QFrame):
    def __init__(self, indice):
        super().__init__()
        self.setFixedSize(400, 70) 
        self.setStyleSheet("background-color: #ffae00; border-radius: 20px;")
        self.marcacao = QFrame()
        self.marcacao.setFixedSize(20, 20)
        self.marcacao.setStyleSheet("background-color: #d70000; border-radius: 10px;")
        self.texto = QTextEdit()
        self.texto.setReadOnly(True)
        self.texto.setStyleSheet("font-weight: bold; font-size: 15px;")
        self.centralLayout = QHBoxLayout()
        self.setLayout(self.centralLayout)
        self.centralLayout.addWidget(self.texto, alignment=Qt.AlignCenter)
        self.centralLayout.addWidget(self.marcacao, alignment=Qt.AlignRight)
        
        def trocar_texto():
            users = load_json.load_file()
            tarefas = users[indice]["diarias"]
            print("as tarefas", tarefas)
            principal = users[indice]["principal"]
            print("a principal", principal)
            for tarefa in tarefas:
                if tarefa["titulo"] == principal:
                    self.texto.setText(principal)
                    return
            self.texto.setText("Nenhuma tarefa principal.")      
            self.marcacao.setStyleSheet("background-color: #5ca300; border-radius: 10px;")  
            self.setStyleSheet("background-color: #5ca300; border-radius: 20px;")      
        trocar_texto()   

class linha(QLabel):
    def __init__(self, texto):
        super().__init__()
        self.setStyleSheet("color: white; font-size: 19px; font-weight: bold ;")
        self.setText(texto)

class TelaDireita(QFrame):
    def __init__(self, indice):
        super().__init__()
        self.setMinimumSize(320, 720)
        self.setStyleSheet("background-color: #2f2f2f; border-radius: 20px;")
        self.centralLayout = QVBoxLayout()
        self.setLayout(self.centralLayout)
        
        # frame para Tarefas concluidas
        self.layoutframezinhos = QHBoxLayout()
        self.frame_concluidas = framezinho("Concluidas")
        self.frame_restantes = framezinho("Restantes")

        
        # criando os widgets
        
        self.TarefaPrincipal = linha("  Tarefa principal")
        self.widget = widget(indice)
        spacer1 = QSpacerItem(50, 50)
        spacer2 = QSpacerItem(280, 280)
        spacer3 = QSpacerItem(200, 200)
        
        self.centralLayout.addWidget(self.TarefaPrincipal, alignment=Qt.AlignCenter | Qt.AlignTop | Qt.AlignLeft)
        self.centralLayout.addWidget(self.widget, alignment=Qt.AlignCenter | Qt.AlignTop)
        self.centralLayout.addItem(spacer1)
        self.centralLayout.addLayout(self.layoutframezinhos)
        self.layoutframezinhos.addWidget(self.frame_concluidas, alignment=Qt.AlignCenter)
        self.layoutframezinhos.addWidget(self.frame_restantes, alignment=Qt.AlignCenter )

        self.centralLayout.addItem(spacer2)

        self.centralLayout.addItem(spacer3)

class framezinho(QFrame):
    def __init__(self, texto):
        super().__init__()
        self.setStyleSheet("background-color: #23272A;")
        self.Central_layout = QVBoxLayout()
        self.setLayout(self.Central_layout)
        self.setFixedSize(150, 150)
        self.linha = linha(texto)
        self.Central_layout.addWidget(self.linha, alignment=Qt.AlignTop | Qt.AlignCenter)
        
        
class Ui_Concluidos(QFrame):
    def __init__(self, expanded, indice):
        super().__init__()
        self.setStyleSheet("background-color: #23272A; border-radius: 10px;")
        self.indice = indice
        if expanded:
            self.setFixedSize(1050, 760)
        else:
            self.setFixedSize(1125, 760)
        self.central_layout = QHBoxLayout()
        self.setLayout(self.central_layout)
        
        self.lista = QListWidget()
        self.lista.setFixedSize(610, 740)
        self.lista.setStyleSheet("background-color: #2f2f2f;")
        self.lista.setSpacing(10)
        self.tela_direita = TelaDireita(indice)
        
        self.central_layout.addWidget(self.lista, alignment=Qt.AlignLeft)
        self.central_layout.addWidget(self.tela_direita, alignment=Qt.AlignLeft)
        
        def add_tarefas_inicial(self):
            users = load_json.load_file()
            tarefas = users[indice]["concluidas"]

            for tarefa in tarefas:
                id = tarefa['id']
                check = tarefa["checkbox"]
                prioridade = tarefa["prioridade"]
                difuculdade = tarefa["dificuldade"]
                item = QListWidgetItem(self.lista)
                widget = Custom_widget(tarefa['titulo'], id, difuculdade, prioridade, self.indice, check)
                item.setSizeHint(widget.sizeHint())
                self.lista.addItem(item)
                self.lista.setItemWidget(item, widget)
        
        add_tarefas_inicial(self)        
        

        
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from backend import load_json

class Custom_widget(QFrame):
    def __init__(self, nome, id, dificuldade, prioridade, indice, check):
        super().__init__()
        self.setStyleSheet("background-color: #23272A;")

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
        self.prioridade = QComboBox()
        self.prioridade.setDisabled(True)
        self.prioridade.setStyleSheet("border-radius: 5px; font-weight: bold; color: #ffffff;")
        self.prioridade.setFixedSize(120, 35)
        self.prioridade.addItems(["URGENTE", "RELEVANTE", "TRANQUILO"])
        self.muda_cor(self.Qprioridade)
        self.prioridade.currentIndexChanged.connect(lambda: self.muda_cor(self.prioridade.currentText()))
    
        self.central_layout.addWidget(self.titulo)     
        self.central_layout.addWidget(self.xp, alignment=Qt.AlignmentFlag.AlignRight)
        self.central_layout.addWidget(self.prioridade)
        
                
            
        
        def qual_cor():
            
            xp_text = self.xp.text()
            xp_value = int(xp_text.split()[1])
            
            if xp_value == 150:
                self.xp.setStyleSheet("color: #800000; background-color: transparent; font-weight: bold;")
                
            elif xp_value == 120:
                self.xp.setStyleSheet("color: #ff6600; background-color: transparent; font-weight: bold;")
                
            elif xp_value == 100:
                self.xp.setStyleSheet("color: #007a0a; background-color: transparent; font-weight: bold;")
            else:
                self.xp.setStyleSheet("color: #ffffff; background-color: transparent; font-weight: bold;")  
                
        qual_cor()
        
    def muda_cor(self, opcao):
        users = load_json.load_file()
        tarefas = users[self.indice]['diarias']
        opcao = opcao      
        for tarefa in tarefas:
            if tarefa["id"] == self.id:
                tarefa["prioridade"] = opcao
                print(tarefa)
                load_json.save_file(users)
                break
        print(opcao)
        if opcao == "URGENTE":
            # Mudar a cor de fundo do widget inteiro para vermelho
            self.prioridade.setStyleSheet("background-color: #800000; color: #ffffff; font-weight: bold;")
            self.setStyleSheet("background-color: #ff4f4f;")
            self.prioridade.setCurrentText("URGENTE")
        elif opcao == "RELEVANTE":
            # Mudar a cor de fundo do widget inteiro para laranja
            self.prioridade.setCurrentText("RELEVANTE")
            self.prioridade.setStyleSheet("background-color: #ff6600; color: #ffffff; font-weight: bold;")
            self.setStyleSheet("background-color: #ff934a;")
        elif opcao == "TRANQUILO":
            # Mudar a cor de fundo do widget inteiro para verde
            self.prioridade.setCurrentText("TRANQUILO")
            self.prioridade.setStyleSheet("background-color: #007a0a; color: #ffffff; font-weight: bold;")
            self.setStyleSheet("background-color: #3fff4f;")                

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
        
        # criando os widgets
        
        self.TarefaPrincipal = linha("  Tarefa principal")
        self.mensagem = linha("  Tarefas concluidas")
        self.widget = widget(indice)
        spacer1 = QSpacerItem(50, 50)
        spacer2 = QSpacerItem(280, 280)
        spacer3 = QSpacerItem(200, 200)
        self.numero_tarefas = linha("  0")
        
        self.centralLayout.addWidget(self.TarefaPrincipal, alignment=Qt.AlignCenter | Qt.AlignTop | Qt.AlignLeft)
        self.centralLayout.addWidget(self.widget, alignment=Qt.AlignCenter | Qt.AlignTop)
        self.centralLayout.addItem(spacer1)
        self.centralLayout.addWidget(self.mensagem, alignment=Qt.AlignCenter | Qt.AlignLeft | Qt.AlignTop)
        self.centralLayout.addWidget(self.numero_tarefas, alignment=Qt.AlignCenter | Qt.AlignLeft | Qt.AlignTop)
        self.centralLayout.addItem(spacer2)

        self.centralLayout.addItem(spacer3)

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
        self.lista.setStyleSheet("background-color: #616161;")
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
                widget.muda_cor(prioridade)
        
        add_tarefas_inicial(self)        
        

        
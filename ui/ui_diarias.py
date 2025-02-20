from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from backend import load_json
import random

class ver(QDialog):
    def __init__(self, descricao):
        super().__init__()
        self.setStyleSheet("background-color: #303030;")
        self.centrallayout = QVBoxLayout()
        self.setLayout(self.centrallayout)
        self.titulo = QLabel("DESCRIÇÃO")  
        self.titulo.setStyleSheet("color: #ffffff; font-weight: bold; font-size: 20px;")      
        self.descricao = QTextEdit(descricao)
        self.descricao.setStyleSheet("color: #ffffff;")
        self.descricao.setMinimumSize(400, 300)
        self.descricao.setReadOnly(True)    
        self.botao_ok = botoes("OK", 40, 150)
        self.centrallayout.addWidget(self.titulo, alignment=Qt.AlignCenter)       
        self.centrallayout.addWidget(self.descricao)       
        self.centrallayout.addWidget(self.botao_ok, alignment=Qt.AlignCenter)
        self.botao_ok.clicked.connect(lambda: self.close())
        self.show()
        self.exec()       


class dialog_tarefa(QDialog):
    def __init__(self, lista, user, indice):
        super().__init__()
        self.user = user
        self.tarefas = user['tarefas']
        self.indice = indice
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
        
        # parte só para esses combobox chato aqui
        self.layoutCombos = QHBoxLayout()
        self.layoutCombos.setContentsMargins(70, 5, 70, 5)
        self.qual_prioridade = QComboBox()
        self.qual_prioridade.setFixedSize(140, 40)
        self.qual_prioridade.addItems(["URGENTE", "RELEVANTE", "TRANQUILO"])
        self.qual_dificuldade = QComboBox()
        self.qual_dificuldade.setFixedSize(140, 40)
        self.qual_dificuldade.addItems(["FÁCIL", "MEDIO", "DIFÍCIL"])
        self.layoutCombos.addWidget(self.qual_prioridade)
        self.layoutCombos.addWidget(self.qual_dificuldade)
        
        
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
        self.central_layout.addLayout(self.layoutCombos)
        self.central_layout.addWidget(self.botao_ok, alignment=Qt.AlignmentFlag.AlignCenter)
        self.central_layout.addWidget(self.botao_cancelar, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.botao_cancelar.clicked.connect(lambda: self.close())
        self.botao_ok.clicked.connect(lambda: add_task(self.tarefas))
        
        def add_task(tarefas):
            id = len(tarefas)
            item = QListWidgetItem(self.lista)
            widget = Custom_widget(self.tarefa.text(), id, self.qual_dificuldade.currentText(), self.qual_prioridade.currentText())
            item.setSizeHint(widget.sizeHint())
            self.lista.addItem(item)
            self.lista.setItemWidget(item, widget)
            widget.muda_cor(self.qual_prioridade.currentText())

            self.user['tarefas'].append({
                "id": id, 
                "titulo": self.tarefa.text(),
                "descrição": self.descricao.toPlainText(),
                "dificuldade": self.qual_dificuldade.currentText(),
                "prioridade": self.qual_prioridade.currentText()
                })
            users = load_json.load_file()
            users[self.indice] = self.user
            load_json.save_file(users)
            print(users)
            
            

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
    def __init__(self, nome, id, dificuldade, prioridade):
        super().__init__()
        self.central_layout = QHBoxLayout()
        self.setLayout(self.central_layout)
        self.Qprioridade = prioridade
        self.dificuldade = dificuldade
        self.id = id
        self.checkbox = QCheckBox()
        self.checkbox.setStyleSheet("background-color: #c0c0c0;")
        self.checkbox.setStyleSheet("background: transparent;")
        self.checkbox.setFixedWidth(40)
        self.titulo = QLabel(nome)
        self.titulo.setStyleSheet("background: transparent; font-weight: bold; font-size: 15px; color: #ffffff;")
        self.xp = QLabel(f"XP {self.verificarXP(self.dificuldade)}  ")
        self.xp.setStyleSheet("background: transparent; font-weight: bold; font-size: 15px; color: #ffffff;")
        self.prioridade = QComboBox()
        self.prioridade.setStyleSheet("border-radius: 2px; font-weight: bold; color: #ffffff;")
        self.prioridade.setFixedSize(105, 35)
        self.prioridade.addItems(["URGENTE", "RELEVANTE", "TRANQUILO"])
        self.muda_cor(self.Qprioridade)
        self.prioridade.currentIndexChanged.connect(lambda: self.muda_cor(self.prioridade.currentText()))
        self.central_layout.addWidget(self.checkbox)     
        self.central_layout.addWidget(self.titulo)     
        self.central_layout.addWidget(self.xp, alignment=Qt.AlignmentFlag.AlignRight)
        self.central_layout.addWidget(self.prioridade)     
        
    def verificarXP(self, dificuldade):
        xp = 0
        if dificuldade == "DIFÍCIL":
            xp = 150
            self.xp.setStyleSheet("color: #800000")
        elif dificuldade == "MEDIO":
            xp = 120
            self.xp.setStyleSheet("color: #ff6600")
        elif dificuldade == "FÁCIL":
            xp = 100
            self.xp.setStyleSheet("color: #007a0a")   
        return str(xp)    
    

    def muda_cor(self, opcao):
        print(opcao)
        opcao = opcao      
        if opcao == "URGENTE":
            # Mudar a cor de fundo do widget inteiro para vermelho
            self.prioridade.setStyleSheet("background-color: #800000; color: #ffffff;")
            self.prioridade.setCurrentText("URGENTE")
        elif opcao == "RELEVANTE":
            # Mudar a cor de fundo do widget inteiro para laranja
            self.prioridade.setCurrentText("RELEVANTE")
            self.prioridade.setStyleSheet("background-color: #ff6600; color: #ffffff;")
        elif opcao == "TRANQUILO":
            # Mudar a cor de fundo do widget inteiro para verde
            self.prioridade.setCurrentText("TRANQUILO")
            self.prioridade.setStyleSheet("background-color: #007a0a; color: #ffffff;")

        

class TaskLista(QWidget):
    def __init__(self, status_patente, user, indice):
        super().__init__()
        self.user = user
        self.tarefas = user['tarefas']
        self.indice = indice
        self.CentralLayout = QHBoxLayout(self)
        self.task_list = QListWidget()
        self.status_patente = status_patente
        
        # layout botões
        self.layout_botoes = QVBoxLayout()
        self.layout_botoes.setAlignment(Qt.AlignTop)
        self.botao_concluir = botoes("CONCLUIR", 35, 80)
        self.botao_adicionar = botoes("ADICIONAR", 35, 80)
        self.botao_ver = botoes("VER TAREFA", 35, 80)
        self.botao_excluir = botoes("EXCLUIR", 35, 80)
        self.layout_botoes.addWidget(self.botao_concluir)
        self.layout_botoes.addWidget(self.botao_adicionar)
        self.layout_botoes.addWidget(self.botao_ver)
        self.layout_botoes.addWidget(self.botao_excluir)
        self.CentralLayout.addWidget(self.task_list)
        self.CentralLayout.addLayout(self.layout_botoes)
        
        self.botao_adicionar.clicked.connect(lambda: dialog_tarefa(self.task_list, self.user, self.indice))
        self.botao_concluir.clicked.connect(lambda: concluir_tarefa(self, self.tarefas))
        self.botao_ver.clicked.connect(lambda: ver_tarefa(self.tarefas))
        self.botao_excluir.clicked.connect(lambda: excluir_tarefa(self.tarefas))
        
        def add_tarefas_inicial(tarefas):
            for tarefa in tarefas:
                id = tarefa['id']
                prioridade = tarefa["prioridade"]
                difuculdade = tarefa["dificuldade"]
                item = QListWidgetItem(self.task_list)
                widget = Custom_widget(tarefa['titulo'], id, difuculdade, prioridade)
                item.setSizeHint(widget.sizeHint())
                self.task_list.addItem(item)
                self.task_list.setItemWidget(item, widget)
                widget.muda_cor(prioridade)
        
        add_tarefas_inicial(self.tarefas)
        
        def concluir_tarefa(self, tarefas):
            tarefas = tarefas
            selected_item = self.task_list.currentRow()
            selected_line = self.task_list.currentItem()
            if selected_item >= 0:
                widget = self.task_list.itemWidget(selected_line)
                id = widget.id
                xp = int(widget.xp.text().split()[1])
                
                for tarefa in tarefas:
                    if tarefa["id"] == id:
                        tarefas.remove(tarefa)
                        print(tarefas)
                self.task_list.takeItem(selected_item)
                self.user['tarefas'] = tarefas
                users = load_json.load_file()
                users[self.indice]['tarefas'] = tarefas
                load_json.save_file(users)
                self.status_patente.atualizar_xp(xp)
        
        def ver_tarefa(tarefas):
            tarefas = tarefas
            selected_item = self.task_list.currentItem()
            if selected_item:
                widget = self.task_list.itemWidget(selected_item)
                id = widget.id
                for tarefa in tarefas:
                    if tarefa["id"] == id:
                        ver(tarefa["descrição"])
                        
        def excluir_tarefa(tarefas):
            tarefas = tarefas
            selected_item = self.task_list.currentRow()
            selected_line = self.task_list.currentItem()
            if selected_item >= 0:
                widget = self.task_list.itemWidget(selected_line)
                id = widget.id
                
                for tarefa in tarefas:
                    if tarefa["id"] == id:
                        tarefas.remove(tarefa)
                        users = load_json.load_file()
                        users[self.indice]['tarefas'] = tarefas
                        load_json.save_file(users)
                        print(users)
                self.task_list.takeItem(selected_item)                
                        
        



class ui_diarias(QFrame):
    def __init__(self, status_patente, user, indice):
        super().__init__()
        self.user = user
        self.indice = indice
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
        self.tela_list = TaskLista(self.statusPatente, self.user, self.indice)

        
        # add no layout
        
        self.centralLayout.addWidget(self.texto)
        self.centralLayout.addWidget(self.tela_list)

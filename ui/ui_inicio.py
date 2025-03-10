from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from backend import load_json
import os

local = os.path.dirname(os.path.abspath(__file__))
raiz = os.path.dirname(local)  # Volta uma pasta
local_patentes = os.path.join(raiz, "icons")
patentes = [(i * 1000, os.path.join(local_patentes, f"Prancheta {i + 1}.png")) for i in range(111)]

class botoes(QPushButton):
    def __init__(self, nome, altura, largura):
        super().__init__()
        self.setStyleSheet("QPushButton {background-color: #f87000; border-radius: 10px; color: #ffffff; font-weight: bold;} QPushButton:Hover {background-color: #000000;}")
        self.setText(nome)
        self.setFixedSize(largura, altura)
        
class frame_botoes(QHBoxLayout):
    def __init__(self):
        super().__init__()
        self.botao = botoes("CONCLUIR", 60, 180)
        self.botao2 = botoes("CONCLUIR", 60, 180)
        self.botao3 = botoes("CONCLUIR", 60, 180)
        self.addWidget(self.botao)
        self.addWidget(self.botao2)
        self.addWidget(self.botao3)

class widget(QFrame):
    def __init__(self, indice):
        super().__init__()
        self.setFixedSize(600, 90) 
        self.setStyleSheet("background-color: #ffae00; border-radius: 20px;")
        self.marcacao = QFrame()
        self.marcacao.setFixedSize(20, 20)
        self.marcacao.setStyleSheet("background-color: #d70000; border-radius: 10px;")
        self.texto = QTextEdit()
        self.texto.setFixedSize(550, 50)
        self.texto.setReadOnly(True)
        self.texto.setStyleSheet("font-weight: bold; font-size: 20px;")
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
        
class BarraDeXP(QWidget):
    def __init__(self, xp_atual=0, xp_maximo=1000):
        super().__init__()
        self.xp_atual = xp_atual
        self.xp_maximo = xp_maximo

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        self.setLayout(layout)

        self.label = QLabel(f"XP: {self.xp_atual} / {self.xp_maximo}")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("color: white; font-weight: bold;")

        self.progress = QProgressBar()
        self.progress.setMaximum(self.xp_maximo)
        self.progress.setValue(self.xp_atual)
        self.progress.setTextVisible(True)
        self.progress.setAlignment(Qt.AlignCenter)
        self.progress.setFormat(f"{self.get_porcentagem()}%")
        self.progress.setStyleSheet("""
            QProgressBar {
                border: 2px solid #555555;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #ff8514;
                width: 10px;
            }
        """)

        layout.addWidget(self.label)
        layout.addWidget(self.progress)

    def get_porcentagem(self):
        return int((self.xp_atual / self.xp_maximo) * 100)

    def atualizar_xp(self, novo_xp):
        self.xp_atual = novo_xp
        self.label.setText(f"XP: {self.xp_atual} / {self.xp_maximo}")
        self.progress.setValue(self.xp_atual)
        self.progress.setFormat(f"{self.get_porcentagem()}%")

class linha(QLabel):
    def __init__(self, texto):
        super().__init__()
        self.setStyleSheet("color: white; font-size: 19px; font-weight: bold ;")
        self.setText(texto)

class framedireita(QFrame):
    def __init__(self, indice):
        super().__init__()
        self.setFixedSize(350, 680)
        self.setStyleSheet("background-color: #2C2F33; border-radius: 10px;")
        self.users = load_json.load_file()
        self.user = self.users[indice]
        
        # frame para coisas do XP
        self.frameXP = QFrame()
        self.frameXP.setFixedSize(330, 140)
        self.layout_xp  = QVBoxLayout()
        self.frameXP.setLayout(self.layout_xp)
        self.frameXP.setStyleSheet("background-color: #23272A; border-radius: 10px;")
        self.progres_bar = BarraDeXP(int(self.user["xp_variavel"]))
        self.xp_total = linha("XP TOTAL")
        self.xp = linha(str(self.user["xp"]))
        self.layout_xp.addWidget(self.progres_bar, alignment=Qt.AlignTop | Qt.AlignCenter)
        self.layout_xp.addWidget(self.xp_total, alignment=Qt.AlignTop | Qt.AlignCenter)
        self.layout_xp.addWidget(self.xp, alignment=Qt.AlignTop | Qt.AlignCenter)


        self.central_layout = QVBoxLayout()
        self.setLayout(self.central_layout)

        self.texto_nivel = linha("NÍVEL")
        self.Patente = QLabel()
        self.Patente.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.Patente.setFixedSize(290, 290)
        self.Patente.setScaledContents(True)
        self.proxima_patente = linha("PRÓXIMA PATENTE")
        self.Next_patente = QLabel()
        self.Next_patente.setFixedSize(130, 130)
        self.Next_patente.setScaledContents(True)
        
        
        self.central_layout.addWidget(self.texto_nivel, alignment=Qt.AlignTop | Qt.AlignCenter)
        self.central_layout.addWidget(self.frameXP, alignment=Qt.AlignTop | Qt.AlignCenter)
        self.central_layout.addWidget(self.Patente, alignment=Qt.AlignTop | Qt.AlignCenter)
        self.central_layout.addWidget(self.proxima_patente, alignment=Qt.AlignTop | Qt.AlignCenter)
        self.central_layout.addWidget(self.Next_patente, alignment=Qt.AlignTop | Qt.AlignCenter)

        self.patente_inicial()  

    def patente_inicial(self):
        xp = int(self.user["xp"])
        print(xp)
        for i in range(111, -1, -1):
            if xp >= i * 1000:
                pixmap = QPixmap(patentes[i][1])
                pixmap2 = QPixmap(patentes[i + 1][1])
                self.Patente.setPixmap(pixmap)
                self.Next_patente.setPixmap(pixmap2)
                break
        
class frameesquerda(QFrame):
    def __init__(self, indice):
        super().__init__()
        self.setFixedSize(650, 740)
        self.setStyleSheet("background-color: #2C2F33; border-radius: 10px;")
        self.central_layout = QVBoxLayout()
        self.setLayout(self.central_layout)
        self.texto_principal = linha("    Tarefa Principal")
        self.tarefa_principal = widget(indice)
        self.frame_botoes = frame_botoes()
        self.spacer = QSpacerItem(510, 510)
        
        
        
        
        self.central_layout.addWidget(self.texto_principal, alignment=Qt.AlignTop | Qt.AlignLeft)
        self.central_layout.addWidget(self.tarefa_principal, alignment=Qt.AlignTop | Qt.AlignCenter)
        self.central_layout.addLayout(self.frame_botoes)
        self.central_layout.addItem(self.spacer)



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
        self.frame_esquerda = frameesquerda(indice)
        self.frame_direita = framedireita(indice)
        self.spacer = QSpacerItem(30, 30)
        
        
        self.Central_layout.addWidget(self.frame_esquerda, alignment=Qt.AlignLeft)
        self.Central_layout.addWidget(self.frame_direita, alignment=Qt.AlignRight | Qt.AlignTop)
        self.Central_layout.addItem(self.spacer)
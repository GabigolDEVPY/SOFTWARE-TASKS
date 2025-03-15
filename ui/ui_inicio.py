from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from backend import load_json
import os
from datetime import datetime



local = os.path.dirname(os.path.abspath(__file__))
raiz = os.path.dirname(local)  # Volta uma pasta
local_patentes = os.path.join(raiz, "icons")
xp = os.path.join(raiz, "backgrounds", "xp.png")
print("caminhoooooooooooooo",xp)
patentes = [(i * 1000, os.path.join(local_patentes, f"Prancheta {i + 1}.png")) for i in range(111)]

class resgatar_xp(QDialog):
    def __init__(self):
        super().__init__()
        self.setFixedSize(400, 450)
        self.setWindowTitle("RESGATAR XP DIÁRIO")
        self.setWindowModality(Qt.ApplicationModal)
        self.central_layout = QVBoxLayout()
        self.setLayout(self.central_layout)
        self.label = linha("Resgatar XP", 20)
        self.labelXP = linha("XP 500", 20)
        self.botao = botoes("Resgatar", 50, 180)
        self.central_layout.addWidget(self.label, alignment=Qt.AlignTop | Qt.AlignCenter)
        self.xpicone = QLabel()
        self.xpicone.setAlignment(Qt.AlignCenter) 
        self.xpicone.setScaledContents(True)
        self.xpicone.setFixedSize(150, 110) 
        self.Opixmap = QPixmap(xp)
        self.xpicone.setPixmap(self.Opixmap)
        
        self.central_layout.addWidget(self.xpicone, alignment=Qt.AlignCenter | Qt.AlignTop)
        self.central_layout.addWidget(self.labelXP, alignment=Qt.AlignCenter | Qt.AlignTop)
        self.central_layout.addWidget(self.botao, alignment=Qt.AlignCenter | Qt.AlignTop)
        
        self.botao.clicked.connect(lambda: self.close())
        
        # Exibir a janela
        self.show()
        self.exec()

class framezinho(QFrame):
    def __init__(self, texto, indice):
        super().__init__()
        users = load_json.load_file()
        self.user = users[indice]
        self.setStyleSheet("background-color: #23272A;")
        self.Central_layout = QVBoxLayout()
        self.setLayout(self.Central_layout)
        self.setFixedSize(150, 150)
        self.linha = linha(texto, 18)
        self.quantidade = linha("0", 18)
        self.Central_layout.addWidget(self.linha, alignment=Qt.AlignTop | Qt.AlignCenter)
        self.Central_layout.addWidget(self.quantidade, alignment=Qt.AlignTop | Qt.AlignCenter)
        
    def trocar_concluidas(self):
        concluidas = str(self.user["feitas"])
        self.quantidade.setText(concluidas)
        
    def trocar_restantes(self):
        restantes = str(self.user["restantes"])
        self.quantidade.setText(restantes)
        
class botoes(QPushButton):
    def __init__(self, nome, altura, largura):
        super().__init__()
        self.setStyleSheet("QPushButton {background-color: #f87000; border-radius: 10px; color: #ffffff; font-weight: bold;} QPushButton:Hover {background-color: #000000;}")
        self.setText(nome)
        self.setFixedSize(largura, altura)
        
class frame_botoes(QGridLayout):
    def __init__(self, indice, status_patente):
        super().__init__()
        
        self.status_patente = status_patente
        self.users = load_json.load_file()
        self.hora_recompensa = self.users[indice]["ultimo-login"]
        self.users[indice]["ultimo-login"] = str(datetime.now())[:10]
        load_json.save_file(self.users)
        
        self.spacer = QSpacerItem(50, 50)
        self.botao = botoes(" RESGATAR", 60, 180)
        self.resgatar = linha("Resgatar xp", 15)
        self.addItem(self.spacer, 3, 1)
        self.addWidget(self.resgatar, 1, 1)
        self.addWidget(self.botao, 2, 1)
        
        self.botao.clicked.connect(self.resgatar_xp)
        
    def resgatar_xp(self):
        print("Ta chamando")
        if self.hora_recompensa != str(datetime.now())[:10]:
            print("hora recompensa")
            self.hora_recompensa = str(datetime.now())[:10]
            self.status_patente.atualizar_xp(500, self.users)
            resgatar_xp()
        
        
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
    def __init__(self, texto, tamanho):
        super().__init__()
        self.setStyleSheet(f"color: white; font-size: {tamanho}px; font-weight: bold ;")
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
        self.frameXP.setFixedSize(330, 190)
        self.layout_xp  = QVBoxLayout()
        self.frameXP.setLayout(self.layout_xp)
        self.frameXP.setStyleSheet("background-color: #23272A; border-radius: 10px;")
        self.progres_bar = BarraDeXP(int(self.user["xp_variavel"]))
        self.xp_total = linha("XP TOTAL", 18)
        self.xp = linha(str(self.user["xp"]), 18)
        self.texto_nivel = linha("NÍVEL", 18)
        self.layout_xp.addWidget(self.texto_nivel, alignment=Qt.AlignTop | Qt.AlignCenter)
        self.layout_xp.addWidget(self.progres_bar, alignment=Qt.AlignTop | Qt.AlignCenter)
        self.layout_xp.addWidget(self.xp_total, alignment=Qt.AlignTop | Qt.AlignCenter)
        self.layout_xp.addWidget(self.xp, alignment=Qt.AlignTop | Qt.AlignCenter)


        self.central_layout = QVBoxLayout()
        self.setLayout(self.central_layout)

        self.Patente = QLabel()
        self.Patente.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.Patente.setFixedSize(240, 240)
        self.Patente.setScaledContents(True)
        self.proxima_patente = linha("Próxima patente", 18)
        self.Next_patente = QLabel()
        self.Next_patente.setFixedSize(130, 130)
        self.Next_patente.setScaledContents(True)
        
        
        self.central_layout.addWidget(self.frameXP, alignment=Qt.AlignTop | Qt.AlignCenter)
        self.central_layout.addWidget(self.Patente, alignment=Qt.AlignTop | Qt.AlignCenter)
        self.central_layout.addWidget(self.proxima_patente, alignment=Qt.AlignBottom | Qt.AlignCenter)
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
    def __init__(self, indice, status_patente):
        super().__init__()

        self.setFixedSize(650, 740)
        self.setStyleSheet("background-color: #2C2F33; border-radius: 10px;")
        self.central_layout = QVBoxLayout()
        self.setLayout(self.central_layout)
        self.texto_principal = linha("    Tarefa Principal", 18)
        self.tarefa_principal = widget(indice)
        self.frame_botoes = frame_botoes(indice, status_patente)
        self.spacer2 = QSpacerItem(150, 150)
        self.spacer3 = QSpacerItem(300, 300)
        
        
        self.layout_frames = QHBoxLayout()
        self.layout_frames.addLayout(self.frame_botoes)
        self.concluidas = framezinho("Concluídas", indice)
        self.concluidas.trocar_concluidas()
        self.restantes = framezinho("Restantes", indice)
        self.restantes.trocar_restantes()
        
        self.layout_frames.addWidget(self.concluidas)
        self.layout_frames.addWidget(self.restantes)
        
        
        self.central_layout.addWidget(self.texto_principal, alignment=Qt.AlignTop | Qt.AlignLeft)
        self.central_layout.addWidget(self.tarefa_principal, alignment=Qt.AlignTop | Qt.AlignCenter)
        self.central_layout.addLayout(self.layout_frames)
        self.central_layout.addItem(self.spacer2)
        self.central_layout.addItem(self.spacer3)



class Ui_inicio(QFrame):
    def __init__(self, expanded, indice, status_patente):
        super().__init__()
        if expanded:
            self.setFixedSize(1050, 760)
        else:
            self.setFixedSize(1125, 760)
            
            
            
        self.setStyleSheet("background-color: #23272A; border-radius: 10px;")
        self.Central_layout = QHBoxLayout()
        self.Central_layout.setSpacing(10)
        self.setLayout(self.Central_layout)
        self.frame_esquerda = frameesquerda(indice, status_patente)
        self.frame_direita = framedireita(indice)
        self.spacer = QSpacerItem(30, 30)
        
        
        self.Central_layout.addWidget(self.frame_esquerda, alignment=Qt.AlignLeft)
        self.Central_layout.addWidget(self.frame_direita, alignment=Qt.AlignRight | Qt.AlignTop)
        self.Central_layout.addItem(self.spacer)
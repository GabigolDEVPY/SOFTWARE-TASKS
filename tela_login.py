from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
import sys
from backend import load_json, verificar_login
import os

local = os.path.dirname(os.path.abspath(__file__))
local_bg = os.path.join(local, "backgrounds\\")
print(local_bg)


class botoes(QPushButton):
    def __init__(self, nome, cor):
        super().__init__()
        self.setText(nome)
        self.setFixedSize(260, 40)
        self.setStyleSheet("QPushButton {border: None; background-color: #f87000; font-weight: bold; color: #ffffff; border-radius: 10px;} QPushButton:Hover {background-color: #000000;}")

# criar layouts
class layouts(QVBoxLayout):
    def __init__(self, texto, botao):
        super().__init__()
        self.addWidget(texto)
        self.addWidget(botao)
        self.configstyle()
        
    def configstyle(self):
        self.setSpacing(10)
        
# criador e estilizador dos textos
class texto(QLabel):
    def __init__(self, nome, tamanho, color):
        super().__init__()
        self.configstyle(nome, tamanho, color)
    def configstyle(self, nome, tamanho, color):
        self.setStyleSheet(f"font-size: {tamanho}px; font-weight: bold; color: #{color}")
        self.setText(nome)
        self.setContentsMargins(50, 0, 20, 0)

            

# criador e estilizador de linhas 
class linha(QLineEdit):
    def __init__(self, nome):
        super().__init__()
        self.configStyle(nome)
    def configStyle(self, nome):
        self.setStyleSheet("QLineEdit {border: 1px solid #f87000; color: #f87000; border-radius: 10px;} QLineEdit:Focus {border: 2px solid #f87000;}")
        self.setFixedSize(330, 40)
        self.setPlaceholderText(nome) 
        self.setContentsMargins(50, 0, 30, 0)

class login(QFrame):
    def __init__(self, tela):
        super().__init__()

        image_path = os.path.join(local_bg, "3.png")  # Ajuste a extensão correta!

        self.setStyleSheet(f"""
            QFrame {{
                background-image: url('{image_path.replace("\\", "/")}'); 
                background-repeat: no-repeat;
                background-attachment: fixed;
                border-radius: 10px;
            }}
        """)
        self.tela = tela
        self.vlayout = QVBoxLayout()
        self.vlayout.setContentsMargins(0, 0, 0, 50)
        # criando olho botão
        self.olho = QPushButton("🙈")
        self.olho.setStyleSheet("border: 1px solid #f87000; border-radius: 4px;")
        self.olho.setFixedSize(30, 30)
        
        # criando botões
        self.botao_login = botoes("LOGIN", None)
        self.botao_registrar = botoes("REGISTRAR", None)
        

        
        # textos, Usuário, Senha
        self.titulo = texto("          LOGIN", "30", "f87000")
        self.titulo.setFixedSize(350, 60)
        self.texto_login = texto("Usuário", "14", "f87000")
        self.texto_senha = texto("Senha", "14", "f87000")
        
        # campos de digitar senha e usuário
        self.campo_usuario = linha("Digite o nome...")
        self.campo_senha = linha('Digite a senha...')
        self.campo_senha.setEchoMode(QLineEdit.Password)
        
        # layout login
        self.layout_login = layouts(self.texto_login, self.campo_usuario)
        self.layout_login.setContentsMargins(0, 50, 0, 0)
        
        
        
        # layout senha
        # mensagem de status
        self.mensagemStatus = texto(None, "15", "FFFFFF")
        self.spacer = QSpacerItem(90, 90)
        self.layout_senha = QVBoxLayout()
        self.layout_senha.addWidget(self.texto_senha)
        # layout senha mais olho 
        self.layoutSenhaOlho = QHBoxLayout()
        self.layoutSenhaOlho.setContentsMargins(0, 0, 15, 10)
        self.layoutSenhaOlho.addWidget(self.campo_senha)
        self.layoutSenhaOlho.addWidget(self.olho, alignment=Qt.AlignmentFlag.AlignLeft)
        self.layout_senha.addLayout(self.layoutSenhaOlho)
        self.layout_senha.addWidget(self.mensagemStatus)
        self.layout_senha.addItem(self.spacer)
        
        
        #adicionando na tela

        # layout principal
        self.vlayout.addWidget(self.titulo, alignment=Qt.AlignTop)
        self.vlayout.addLayout(self.layout_login)
        self.vlayout.addLayout(self.layout_senha)
        self.vlayout.addWidget(self.botao_login, alignment=Qt.AlignCenter)
        self.vlayout.addWidget(self.botao_registrar, alignment=Qt.AlignCenter)
        self.setLayout(self.vlayout)
        self.setFixedSize(350, 500)
        
        self.olho.clicked.connect(lambda: trocar_status_senha())
        self.botao_login.clicked.connect(lambda: verificar_login.verificar_login(self.tela, self.campo_usuario.text(), self.campo_senha.text()))
        self.botao_registrar.clicked.connect(lambda: verificar_login.cadastrar(self, self.campo_usuario.text(), self.campo_senha.text()))
        
        def trocar_status_senha():
            if self.olho.text() == "🙈":
                self.campo_senha.setEchoMode(QLineEdit.Normal)
                self.olho.setText("👀")
            else:
                self.campo_senha.setEchoMode(QLineEdit.Password)
                self.olho.setText("🙈")
                
class tela_principal(QFrame):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TELA LOGIN")
        
        # Aplicando a imagem de fundo ao QFrame da tela principal
        image_path = os.path.join(local_bg, "1.png")  # Ajuste a extensão correta!

        self.setStyleSheet(f"""
            QFrame {{
                background-image: url('{image_path.replace("\\", "/")}'); 
                background-repeat: no-repeat;
                background-attachment: fixed;
                border-radius: 10px;
            }}
        """)
        
        self.titulo = QLabel("                KANBAN DA SHOPEE")
        self.titulo.setFixedSize(800, 60)
        self.titulo.setStyleSheet("font-size: 40px; font-weight: bold; color: #f87000;")
        self.setFixedSize(1200, 700)
        self.layoutCentral = QVBoxLayout()
        self.layoutCanto = QHBoxLayout()
        
        # Adicionando o QFrame de login à tela principal
        self.login = login(self)
        
        # sombra
        
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setXOffset(10)
        shadow.setYOffset(10)
        shadow.setColor(QColor(100, 100, 100, 100))  # Cor preta com transparência
        
        self.login.setGraphicsEffect(shadow)
        self.spacer = QSpacerItem(70, 70)
        self.layoutCanto.addWidget(self.login, alignment=Qt.AlignRight | Qt.AlignmentFlag.AlignTop)
        self.layoutCanto.addItem(self.spacer)
        self.layoutCentral.addWidget(self.titulo)
        self.layoutCentral.addLayout(self.layoutCanto)
        
        self.setLayout(self.layoutCentral)

                    
if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    app.setStyle("windows11")
    window = tela_principal()
    window.show()
    app.exec()
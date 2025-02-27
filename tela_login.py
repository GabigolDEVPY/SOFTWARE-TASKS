from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
import sys
from backend import load_json, verificar_login


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
    def __init__(self, nome, tamanho):
        super().__init__()
        self.configstyle(nome, tamanho)
    def configstyle(self, nome, tamanho):
        self.setStyleSheet(f"font-size: {tamanho}px; font-weight: bold; color: #ffffff;")
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

class login(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # criando a janela
        self.widget_central = QWidget()
        self.widget_central.setStyleSheet("background-color: #1b1b1b;")

        self.vlayout = QVBoxLayout()
        self.vlayout.setContentsMargins(0, 0, 0, 50)
        self.widget_central.setLayout(self.vlayout)
        self.setCentralWidget(self.widget_central)
        # criando olho botão
        self.olho = QPushButton("🙈")
        self.olho.setStyleSheet("border: 1px solid #400040; border-radius: 4px;")
        self.olho.setFixedSize(30, 30)
        
        # criando botões
        self.botao_login = botoes("LOGIN", None)
        self.botao_registrar = botoes("REGISTRAR", None)
        

        
        # textos, Usuário, Senha
        self.titulo = texto("     BEM-VINDO", "30")
        self.texto_login = texto("Usuário", "14")
        self.texto_senha = texto("Senha", "14")
        
        # campos de digitar senha e usuário
        self.campo_usuario = linha("Digite o nome...")
        self.campo_senha = linha('Digite a senha...')
        self.campo_senha.setEchoMode(QLineEdit.Password)
        
        # layout login
        self.layout_login = layouts(self.texto_login, self.campo_usuario)
        self.layout_login.setContentsMargins(0, 50, 0, 0)
        
        # layout senha
        self.layout_senha = QGridLayout()
        self.layout_senha.addWidget(self.texto_senha, 0, 0)
        self.layout_senha.addWidget(self.campo_senha, 1, 0)
        self.layout_senha.addWidget(self.olho, 1, 2)
        self.layout_senha.setContentsMargins(0, 20, 15, 100)
        
        #adicionando na tela

        # layout principal
        self.vlayout.addWidget(self.titulo, alignment=Qt.AlignTop)
        self.vlayout.addLayout(self.layout_login)
        self.vlayout.addLayout(self.layout_senha)
        self.vlayout.addWidget(self.botao_login, alignment=Qt.AlignCenter)
        self.vlayout.addWidget(self.botao_registrar, alignment=Qt.AlignCenter)
        self.setFixedSize(350, 500)
    
        self.olho.clicked.connect(lambda: trocar_status_senha())
        self.botao_login.clicked.connect(lambda: verificar_login.verificar_login(self, self.campo_usuario.text(), self.campo_senha.text()))
        self.botao_registrar.clicked.connect(lambda: verificar_login.cadastrar(self, self.campo_usuario.text(), self.campo_senha.text()))
        
        def trocar_status_senha():
            if self.olho.text() == "🙈":
                self.campo_senha.setEchoMode(QLineEdit.Normal)
                self.olho.setText("👀")
            else:
                self.campo_senha.setEchoMode(QLineEdit.Password)
                self.olho.setText("🙈")
        self.show()        
                
if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    app.setStyle("windows11")
    window = login()
    app.exec()
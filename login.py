from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *


class botoes(QPushButton):
    def __init__(self, nome, cor):
        super().__init__()
        self.setText(nome)
        self.setFixedSize(300, 40)
        self.setStyleSheet(f"QPushButton {{color:{cor} ; background-color: #0b8e1f}}")

# criar layouts
class layouts(QVBoxLayout):
    def __init__(self, texto, botao):
        super().__init__()
        self.addWidget(texto)
        self.addWidget(botao)
        self.configstyle()
        
    def configstyle(self):
        self.setSpacing(8)
        

# criador e estilizador dos textos
class texto(QLabel):
    def __init__(self, nome, tamanho):
        super().__init__()
        self.configstyle(nome, tamanho)
    def configstyle(self, nome, tamanho):
        self.setText(nome)
        self.setContentsMargins(30, 0, 30, 0)
        self.setStyleSheet(f"font-size: {tamanho}px;")

# criador e estilizador de linhas 
class linha(QLineEdit):
    def __init__(self, nome):
        super().__init__()
        self.configStyle(nome)
    def configStyle(self, nome):
        self.setStyleSheet("font-size: 16px;")
        self.setFixedSize(330, 40)
        self.setPlaceholderText(nome) 
        self.setContentsMargins(30, 0, 30, 0)

class login(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # criando a janela
        self.widget_central = QWidget()
        self.vlayout = QVBoxLayout()
        self.widget_central.setLayout(self.vlayout)
        self.setCentralWidget(self.widget_central)
        
        
        # criando botões
        self.botao_login = botoes("LOGIN", "#ffffff")
        self.botao_registrar = botoes("REGISTRAR", "#ffffff")
                    
        # textos, Usuário, Senha
        self.titulo = texto("BEM-VINDO", "30")
        self.texto_login = texto("Usuário", None)
        self.texto_senha = texto("Senha", None)
        
        # campos de digitar senha e usuário
        self.campo_usuario = linha("Digite o nome...")
        self.campo_senha = linha('Digite a senha...')
        
        # layout login
        self.layout_login = layouts(self.texto_login, self.campo_usuario)
        self.layout_login.setContentsMargins(0, 10, 0, 20)
        
        # layout senha
        self.layout_senha = layouts(self.texto_senha, self.campo_senha)
        self.layout_senha.setContentsMargins(0, 0, 0, 110)
        
        
        #adicionando na tela
        self.vlayout.addWidget(self.titulo)
        self.vlayout.addLayout(self.layout_login)
        self.vlayout.addLayout(self.layout_senha)
        self.vlayout.addWidget(self.botao_login)
        self.vlayout.addWidget(self.botao_registrar)

        self.setFixedSize(350, 500)

        

    
    
if __name__ == "__main__":
    app = QApplication([])
    app.setStyle("windows11")
    janela_login = login()
    janela_login.show()
    app.exec()    
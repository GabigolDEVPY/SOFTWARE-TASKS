from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *

class layouts(QVBoxLayout):
    def __init__(self, texto, botao):
        super().__init__()
        self.addWidget(texto)
        self.addWidget(botao)
        self.configstyle()
        
    def configstyle(self):
        self.setSpacing(10)
        self.setContentsMargins(4, 0, 0, 110)

# criador e estilizador dos textos
class texto(QLabel):
    def __init__(self, nome):
        super().__init__()
        self.configstyle(nome)
    def configstyle(self, nome):
        self.setText(nome)
        self.setContentsMargins(30, 0, 30, 0)


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
                    
        # textos, Usuário, Senha
        self.titulo = texto("BEM-VINDO")
        self.texto_login = texto("Usuário")
        self.texto_senha = texto("Senha")
        
        # campos de digitar senha e usuário
        self.campo_usuario = linha("Digite o nome...")
        self.campo_senha = linha('Digite a senha...')
        
        # layout login
        self.layout_login = layouts(self.texto_login, self.campo_usuario)
        
        # layout senha
        self.layout_senha = layouts(self.texto_senha, self.campo_senha)
        #adicionando na tela
        self.vlayout.addWidget(self.titulo)
        self.vlayout.addLayout(self.layout_login)
        self.vlayout.addLayout(self.layout_senha)

        self.setFixedSize(350, 500)

        

    
    
if __name__ == "__main__":
    app = QApplication([])
    app.setStyle("windows11")
    janela_login = login()
    janela_login.show()
    app.exec()    
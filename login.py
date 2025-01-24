from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *

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
        self.vlayout.setSpacing(0) 
        self.widget_central.setLayout(self.vlayout)
        self.setCentralWidget(self.widget_central)
                    
        # textos
        self.titulo = texto("BEM-VINDO")
        self.texto_login = texto("Usuário")
        self.texto_senha = texto("Senha")
        
        # campos de digitar senha e usuário
        self.campo_usuario = linha("Digite o nome...")
        self.campo_senha = linha('Digite a senha...')
        
        
        #adicionando na tela
        self.vlayout.addWidget(self.titulo)
        self.vlayout.addWidget(self.texto_login)
        self.vlayout.addWidget(self.campo_usuario)
        self.vlayout.addWidget(self.texto_senha)
        self.vlayout.addWidget(self.campo_senha)
        self.setFixedSize(350, 500)

        

    
    
if __name__ == "__main__":
    app = QApplication([])
    app.setStyle("windows11")
    janela_login = login()
    janela_login.show()
    app.exec()    
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *


class login(QMainWindow):
    def __init__(self):
        super().__init__()
        self.widget_central = QWidget()
        self.vlayout = QVBoxLayout() 
        self.widget_central.setLayout(self.vlayout)
        self.setCentralWidget(self.widget_central)
        
        #textos
        self.titulo = QLabel("BEM-VINDO")
        self.texto_login = QLabel("Usuário")
        
        
        #adicionando na tela
        self.vlayout.addWidget(self.titulo)
        self.vlayout.addWidget(self.texto_login)
        self.setFixedSize(350, 500)

    
    
if __name__ == "__main__":
    app = QApplication([])
    janela_login = login()
    janela_login.show()
    app.exec()    
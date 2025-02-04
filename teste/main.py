from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from status_patente import StatusPatente
from sidebar import Sidebar
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Criando a instância de StatusPatente
        self.status_patente = StatusPatente()

        # Criando a Sidebar e passando a instância de StatusPatente para ela
        self.sidebar = Sidebar(self.status_patente)

        # Layout principal da janela
        self.layout = QHBoxLayout()

        # Adicionando a Sidebar e o StatusPatente
        self.layout.addWidget(self.sidebar)
        self.layout.addWidget(self.status_patente)

        # Criando o widget central
        central_widget = QWidget()
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)

        # Configurações da janela
        self.setWindowTitle("Exemplo de Sidebar e Status de Patente")
        self.setFixedSize(400, 200)

# Rodando a aplicação
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

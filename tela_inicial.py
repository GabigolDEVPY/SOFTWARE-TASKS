from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from custom_sidebar import Sidebar
from tema import aplicar_tema_dark
import sys

class janela_principal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(900, 600)
        self.widget_central = QWidget()
        self.setCentralWidget(self.widget_central)
        self.CentralLayout = QHBoxLayout()
        self.widget_central.setStyleSheet("background-color: #161616;")
        self.sideBar = Sidebar(self)
        self.sideBar.setParent(self)
        self.widget_central.setLayout(self.CentralLayout)
        self.CentralLayout.addWidget(self.sideBar, alignment=Qt.AlignLeft)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    tema = aplicar_tema_dark(app)
    window = janela_principal()
    window.show()
    app.exec()        
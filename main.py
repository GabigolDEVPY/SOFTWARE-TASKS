from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from tela_login import login
import sys


if __name__ == "__main__":
    
    def comecar():
        app = QApplication(sys.argv)
        tela_login = login()
        app.exec()
        
    comecar()    
    
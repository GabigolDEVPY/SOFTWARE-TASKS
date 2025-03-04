from PySide6.QtWidgets import QApplication, QVBoxLayout, QFrame, QSpinBox, QPushButton
from PySide6.QtCore import Qt
import sys

class App(QFrame):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Exemplo de SpinBox")
        self.setFixedSize(300, 150)
        
        layout = QVBoxLayout()
        
        # Criando o SpinBox
        self.spinbox = QSpinBox()
        self.spinbox.setRange(0, 100)  # Intervalo entre 0 e 100
        self.spinbox.setValue(0)  # Valor inicial
        self.spinbox.setSingleStep(1)  # Incremento de 1 unidade
        
        # Criando um botão para mostrar o valor selecionado
        self.button = QPushButton("Mostrar Valor")
        self.button.clicked.connect(self.show_value)
        
        layout.addWidget(self.spinbox)
        layout.addWidget(self.button)
        
        self.setLayout(layout)
    
    def show_value(self):
        # Exibe o valor atual do SpinBox
        print(f"O valor selecionado é: {self.spinbox.value()}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec())

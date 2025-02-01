from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from tema import aplicar_tema_dark
import sys

class Sidebar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.expanded = False  # 🔹 Estado inicial: recolhida
        self.setFixedWidth(60)  # 🔹 Começa mostrando só os ícones
        
        # Layout vertical da sidebar
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(5, 5, 5, 5)
        self.layout.setSpacing(0)

        # 🔹 Botão de menu (três barras)
        self.btn_menu = QPushButton(" ☰ ")
        self.btn_menu.setStyleSheet("color: white; background: #000000; border: none; font-size: 20px;")
        self.btn_menu.clicked.connect(self.toggle_sidebar)  # Conecta ao método de expandir/retrair
        self.layout.addWidget(self.btn_menu)

        # 🔹 Botões da sidebar
        self.buttons = []
        button_data = [
            ("🏠", " Home"),
            ("📊", " Dashboard"),
            ("📦", " Orders"),
            ("🛒", " Products"),
            ("👥", " Customers")
        ]

        # Criar botões e adicionar ao layout
        for icon, text in button_data:
            btn = QPushButton(icon if not self.expanded else icon + text)
            btn.setStyleSheet("""
                QPushButton {
                    color: white;
                    background: #ff1e0057;
                    border: none;
                    text-align: left;
                    font-size: 16px;
                    padding: 10px;
                }
                QPushButton:hover {
                    background-color: #000000;
                }
            """)
            btn.setMinimumHeight(70)
            self.buttons.append(btn)
            self.layout.setSpacing(0)
            self.layout.addWidget(btn)

        self.layout.addStretch()  # 🔹 Mantém alinhamento correto
        self.setLayout(self.layout)

        # 🔹 Criando animação para suavizar a expansão
        self.animation = QPropertyAnimation(self, b"minimumWidth")

    def toggle_sidebar(self):
        """ Expande ou retrai a sidebar com animação """
        if self.expanded:
            new_width = 60
            for btn in self.buttons:
                btn.setText(btn.text()[0])  # Mantém só o ícone
        else:
            new_width = 200
            for i, btn in enumerate(self.buttons):
                btn.setText(["🏠 Home", "📊 Dashboard", "📦 Orders", "🛒 Products", "👥 Customers"][i])

        self.expanded = not self.expanded
        self.animation.setDuration(300)  # 🔹 Tempo da animação (300ms)
        self.animation.setStartValue(self.width())
        self.animation.setEndValue(new_width)
        self.animation.start()      

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
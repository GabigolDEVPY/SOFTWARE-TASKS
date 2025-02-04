from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from status_patente import statusPatente
import sys

class botoes(QPushButton):
    def __init__(self, nome):
        super().__init__()
        self.setMinimumSize(40, 60)
        self.setText(nome)
        self.setMinimumHeight(70)
        self.setStyleSheet("QPushButton {background-color: #400080; border: None; border-radius: None; font-size: 16px; font-weight: bold; color: #ffffff;} QPushButton:Hover {Background-color: #000000;}")
        

class Sidebar(QWidget):
    def __init__(self, status_patente, parent=None):
        super().__init__(parent)
        self.status_patentes = statusPatente
        self.expanded = False  # 🔹 Estado inicial: recolhida
        self.setFixedWidth(70)  # 🔹 Começa mostrando só os ícones
        
        # VerticalLayout vertical da sidebar
        self.VerticalLayout = QVBoxLayout()
        self.VerticalLayout.setContentsMargins(5, 5, 5, 5)
        self.VerticalLayout.setSpacing(0)

        # 🔹 Botão de menu (três barras)
        self.btn_menu = QPushButton(" ☰ ")
        self.btn_menu.setStyleSheet("QPushButton {color: white; background: #000000; border: None; font-size: 20px; border-radius: None;} QPushButton:Hover {background-color: #400040;}")
        self.btn_menu.clicked.connect(self.toggle_sidebar)  # Conecta ao método de expandir/retrair

        # Criar botões e adicionar ao VerticalLayout
        self.botao_dashboard = botoes("🏠")
        self.botao_tarefas = botoes("📋")
        self.botao_diarias = botoes("📅")
        self.botao_concluidos = botoes("✅")
        self.botao_patente = botoes("🎖️")
        
        
        self.botao_dashboard.clicked.connect(self.status_patentes.atualizar_xp)


        self.VerticalLayout.addStretch()  # 🔹 Mantém alinhamento correto
        self.setLayout(self.VerticalLayout)

        # 🔹 Criando animação para suavizar a expansão
        self.animation = QPropertyAnimation(self, b"minimumWidth")
        self.animation.setDuration(400)
        self.animation.setEasingCurve(QEasingCurve.InOutQuad)
        
        self.VerticalLayout.addWidget(self.btn_menu)
        self.VerticalLayout.addWidget(self.botao_dashboard)
        self.VerticalLayout.addWidget(self.botao_tarefas)
        self.VerticalLayout.addWidget(self.botao_diarias)
        self.VerticalLayout.addWidget(self.botao_concluidos)
        self.VerticalLayout.addWidget(self.botao_patente)

    def toggle_sidebar(self):
        self.expanded = not self.expanded
        
        if self.expanded:
            self.animation.setStartValue(70)
            self.animation.setEndValue(145)
            self.botao_dashboard.setText("🏠 Dashboard")
            self.botao_tarefas.setText("📋 Tarefas")
            self.botao_diarias.setText("📅 Diarias")
            self.botao_concluidos.setText("✅ Concluidos")
            self.botao_patente.setText("🎖️ Patente")
        else:
            self.animation.setStartValue(145)
            self.animation.setEndValue(70)
            self.botao_dashboard.setText("🏠")
            self.botao_tarefas.setText("📋")
            self.botao_diarias.setText("📅")
            self.botao_concluidos.setText("✅")
            self.botao_patente.setText("🎖️")
        self.animation.start()
        




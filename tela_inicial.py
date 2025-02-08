from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from custom_sidebar import Sidebar
from status_patente import statusPatente
from ui.ui_diarias import ui_diarias
import sys

class janela_principal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.expanded = False
        
        def mudar_tamanhos(self):
            """Anima a mudança de tamanho de `widgetcentro` e `status_patente` ao mesmo tempo, mas com tamanhos diferentes."""

            # Alterna o estado expanded
            self.expanded = not self.expanded
            
            # Tamanho para o widgetcentro
            widgetcentro_width = 750 if self.expanded else 825

            # Tamanho para o status_patente
            status_patente_width = 750 if self.expanded else 825 # Exemplo de valores diferentes

            # Animação para `widgetcentro`
            anim_central = QPropertyAnimation(self.widgetcentro, b"minimumWidth")
            anim_central.setDuration(400)
            anim_central.setEasingCurve(QEasingCurve.InOutQuad)
            anim_central.setStartValue(self.widgetcentro.width())
            anim_central.setEndValue(widgetcentro_width)

            # Animação para `status_patente`
            anim_patente = QPropertyAnimation(self.status_patente, b"minimumWidth")
            anim_patente.setDuration(400)
            anim_patente.setEasingCurve(QEasingCurve.InOutQuad)
            anim_patente.setStartValue(self.status_patente.width())
            anim_patente.setEndValue(status_patente_width)

            # Criando um grupo de animação para rodar tudo junto
            self.animation_group = QParallelAnimationGroup()
            self.animation_group.addAnimation(anim_central)
            self.animation_group.addAnimation(anim_patente)

            # Inicia a animação
            self.animation_group.start()
            
        self.setFixedSize(900, 600)
        self.widget_central = QWidget()
        self.setCentralWidget(self.widget_central)
        self.CentralLayout = QHBoxLayout()
        self.CentralLayout.setSpacing(0)
        self.CentralLayout.setContentsMargins(0, 0, 0, 0)
        self.widget_central.setStyleSheet("background-color: #161616;")
        
        # frame centro
        self.layoutCENTRO = QHBoxLayout()


        
        # criando status patente
        self.status_patente = statusPatente()
        self.widgetcentro = ui_diarias(self.status_patente)
        
        # criando a sidebar
        self.sideBar = Sidebar(self.status_patente)
        self.sideBar.btn_menu.clicked.connect(lambda: self.sideBar.toggle_sidebar())
        self.sideBar.btn_menu.clicked.connect(lambda: mudar_tamanhos(self))
        self.sideBar.setParent(self)
        
        # layout para o frma e o status patente
        self.Vlayout = QVBoxLayout()
        self.Vlayout.setContentsMargins(5, 0, 5, 5)
        self.Vlayout.addWidget(self.status_patente, alignment=Qt.AlignTop | Qt.AlignRight)
        self.Vlayout.addWidget(self.widgetcentro, alignment=Qt.AlignRight)
        
        # layout engloba tudo
        self.widget_central.setLayout(self.CentralLayout)
        self.CentralLayout.addWidget(self.sideBar, alignment=Qt.AlignTop | Qt.AlignLeft)
        self.CentralLayout.addLayout(self.Vlayout)


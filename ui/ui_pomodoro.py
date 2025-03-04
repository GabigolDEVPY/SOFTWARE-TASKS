import pygame
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
import sys
import math

# Inicialize o pygame para tocar o áudio
pygame.mixer.init()

# Carregar o som MP3 local
pygame.mixer.music.load("D:/WINDOWS/PROGRAMACAO_TUDO/SOFTWARE-TASKS/audio.mp3")  # Ajuste o caminho do arquivo

class PomodoroClock(QFrame):
    def __init__(self):
        super().__init__()
        self.setFixedSize(400, 400)
        self.setStyleSheet("background-color: #2f2f2f;")
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_clock)
        self.pomodoro_time = 25 * 60  # 25 minutos em segundos
        self.break_time = 5 * 60  # 5 minutos em segundos
        self.total_seconds = self.pomodoro_time
        self.major_segments = self.pomodoro_time // 60  # Grandes marcações a cada 1 min
        self.minor_segments = self.total_seconds // 10  # Pequenos a cada 10 segundos
        self.time_elapsed = 0
        self.running = False
        self.on_break = False

    def start_timer(self):
        if not self.running:
            self.running = True
            self.timer.start(1000)
    
    def pause_timer(self):
        self.running = False
        self.timer.stop()
    
    def reset_timer(self):
        self.running = False
        self.time_elapsed = 0
        self.on_break = False
        self.total_seconds = self.pomodoro_time
        self.timer.stop()
        self.update()
    
    def update_clock(self):
        if self.running:
            if self.time_elapsed < self.total_seconds:
                self.time_elapsed += 1
            else:
                self.running = False
                self.time_elapsed = 0
                if not self.on_break:
                    self.on_break = True
                    self.total_seconds = self.break_time  # Inicia o tempo de descanso
                    pygame.mixer.music.play()  # Toca o som quando o Pomodoro acaba
                else:
                    self.on_break = False
                    self.total_seconds = self.pomodoro_time  # Volta ao Pomodoro
                    pygame.mixer.music.play()  # Toca o som quando o intervalo acaba
                
            self.update()
    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        center = self.rect().center()
        radius = min(self.width(), self.height()) // 2 - 10
        
        # Fundo do relógio
        painter.setBrush(QColor("#23272A"))
        painter.drawEllipse(center.x() - radius, center.y() - radius, radius * 2, radius * 2)
        
        # Desenha as marcações principais (1 min) e menores (10s), preenchendo progressivamente
        for i in range(self.minor_segments):
            angle_deg = -90 + (i * (360 / self.minor_segments))
            angle_rad = math.radians(angle_deg)
            
            if i % 6 == 0:
                inner_offset = 20  # Marcações principais a cada 1 min
                pen_width = 3
            else:
                inner_offset = 10  # Marcações menores a cada 10s
                pen_width = 2
            
            inner_x = center.x() + math.cos(angle_rad) * (radius - inner_offset)
            inner_y = center.y() + math.sin(angle_rad) * (radius - inner_offset)
            outer_x = center.x() + math.cos(angle_rad) * radius
            outer_y = center.y() + math.sin(angle_rad) * radius
            
            # Alterando cores dependendo do tempo
            if i < self.time_elapsed // 10:
                if self.on_break:
                    painter.setPen(QPen(QColor(255, 165, 0), pen_width))  # Cor para pausa
                else:
                    painter.setPen(QPen(QColor(0, 200, 0), pen_width))  # Cor para Pomodoro
            else:
                painter.setPen(QPen(QColor(255, 255, 255), pen_width))
            
            painter.drawLine(QPointF(inner_x, inner_y), QPointF(outer_x, outer_y))
        
        # Exibe o tempo restante
        remaining_seconds = self.total_seconds - self.time_elapsed
        minutes_left = remaining_seconds // 60
        seconds_left = remaining_seconds % 60
        time_text = f"{minutes_left:02}:{seconds_left:02}"
        painter.setPen(QPen(QColor('#f87000')))
        painter.setFont(QFont("Arial", 50, QFont.Bold))
        painter.drawText(self.rect(), Qt.AlignCenter, time_text)

    def update_pomodoro_time(self, new_time):
        self.pomodoro_time = new_time * 60  # Em minutos
        if not self.on_break:
            self.total_seconds = self.pomodoro_time

    def update_break_time(self, new_time):
        self.break_time = new_time * 60  # Em minutos
        if self.on_break:
            self.total_seconds = self.break_time


class botoes(QPushButton):
    def __init__(self, nome):
        super().__init__()
        self.setStyleSheet("QPushButton {background-color: #f87000; color: white; font-weight: bold; font-size: 18px;} QPushButton:Hover {background-color: #000000; color: white; font-weight: bold; font-size: 20px;}")
        self.setFixedSize(170, 60)
        self.setText(nome)

class spin(QSpinBox):
    def __init__(self):
        super().__init__()
        self.setFixedSize(120, 40)
        self.setRange(1, 25)
        self.setValue(25)
        self.setSingleStep(1)
        self.setStyleSheet("""
            QSpinBox {
                background-color: #23272A;
                color: white;
                border: 2px solid #f87000;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
                padding: 5px;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                width: 20px;
                background-color: #f87000;
                border: none;
            }
        """)
        
class TelaRelogio(QFrame):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pomodoro Timer")
        self.setFixedSize(580, 720)
        self.setStyleSheet("background-color: #2f2f2f; border-radius: 20px;")
        
        layout = QVBoxLayout()
        layout_spins = QHBoxLayout()
        layout_spins.setContentsMargins(20, 20, 20, 50)
        layout_spin_descanso = QVBoxLayout()
        layout_spin_pomodoro = QVBoxLayout()
        layout_botoes = QHBoxLayout()
        layout_botoes.setContentsMargins(20, 0, 20, 0)
        
        
        self.aumentartempo = spin()
        self.texto_tempo = QLabel("Descanso")
        self.texto_tempo.setStyleSheet("font-weight: bold; font-size: 18px;")
        
        self.aumentarpomodoro = spin()
        self.texto_estudo = QLabel("Estudo")
        self.texto_estudo.setStyleSheet("font-weight: bold; font-size: 18px ;")
        
        layout_spin_pomodoro.addWidget(self.texto_estudo)
        layout_spin_pomodoro.addWidget(self.aumentarpomodoro)
        layout_spin_descanso.addWidget(self.texto_tempo)
        layout_spin_descanso.addWidget(self.aumentartempo)
        
        layout_spins.addLayout(layout_spin_descanso)
        layout_spins.addLayout(layout_spin_pomodoro)
        

        
        
        self.aumentartempo.valueChanged.connect(self.update_break_time)
        self.aumentarpomodoro.valueChanged.connect(self.update_pomodoro_time)
        
        self.clock = PomodoroClock()
        layout.addWidget(self.clock, alignment=Qt.AlignCenter)
        layout.addLayout(layout_spins)
        
        self.start_button = botoes("Iniciar")
        self.start_button.clicked.connect(self.clock.start_timer)
        layout_botoes.addWidget(self.start_button, alignment=Qt.AlignCenter)
        
        self.pause_button = botoes("Pausar")
        self.pause_button.clicked.connect(self.clock.pause_timer)
        layout_botoes.addWidget(self.pause_button, alignment=Qt.AlignCenter)
        
        self.reset_button = botoes("Reset")
        self.reset_button.clicked.connect(self.clock.reset_timer)
        layout_botoes.addWidget(self.reset_button, alignment=Qt.AlignCenter)
        
        layout.addLayout(layout_botoes)
        self.setLayout(layout)

    def update_pomodoro_time(self, value):
        print(f"Atualizando tempo Pomodoro: {value}")
        self.clock.update_pomodoro_time(value)
    
    def update_break_time(self, value):
        print(f"Atualizando tempo de pausa: {value}")
        self.clock.update_break_time(value)

class TelaDireita(QFrame):
    def __init__(self):
        super().__init__()
        self.setMinimumSize(450, 720)
        self.setStyleSheet("background-color: #2f2f2f; border-radius: 20px;")


class PomodoroApp(QFrame):
    def __init__(self):
        super().__init__()
        self.setFixedSize(1125, 750)
        self.setStyleSheet("background-color: #23272A;")
        self.CentralLayout = QHBoxLayout()
        self.setLayout(self.CentralLayout)
        self.Tela_Relogio = TelaRelogio()
        self.tela_direita = TelaDireita()
        self.CentralLayout.addWidget(self.Tela_Relogio, alignment=Qt.AlignCenter | Qt.AlignLeft)
        self.CentralLayout.addWidget(self.tela_direita, alignment=Qt.AlignCenter | Qt.AlignRight)



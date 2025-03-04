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
        self.setFixedSize(500, 500)
        self.setStyleSheet("background-color: #2f2f2f; border: 2px solid black; border-radius: 10px;")
        
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
        painter.setBrush(QColor(100, 100, 100))
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
                painter.setPen(QPen(Qt.black, pen_width))
            
            painter.drawLine(QPointF(inner_x, inner_y), QPointF(outer_x, outer_y))
        
        # Exibe o tempo restante
        remaining_seconds = self.total_seconds - self.time_elapsed
        minutes_left = remaining_seconds // 60
        seconds_left = remaining_seconds % 60
        time_text = f"{minutes_left:02}:{seconds_left:02}"
        painter.setPen(Qt.black)
        painter.setFont(QFont("Arial", 20, QFont.Bold))
        painter.drawText(self.rect(), Qt.AlignCenter, time_text)

class PomodoroApp(QFrame):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pomodoro Timer")
        self.setFixedSize(600, 720)  # Tamanho da janela ajustado
        self.setStyleSheet("background-color: #2f2f2f;")
        
        layout = QVBoxLayout()
        self.clock = PomodoroClock()
        layout.addWidget(self.clock)
        
        # Adicionando os botões ao layout
        self.start_button = QPushButton("Iniciar")
        self.start_button.setStyleSheet("background-color: #400040; color: white;")
        self.start_button.clicked.connect(self.clock.start_timer)
        layout.addWidget(self.start_button)
        
        self.pause_button = QPushButton("Pausar")
        self.pause_button.setStyleSheet("background-color: #400040; color: white;")
        self.pause_button.clicked.connect(self.clock.pause_timer)
        layout.addWidget(self.pause_button)
        
        self.reset_button = QPushButton("Resetar")
        self.reset_button.setStyleSheet("background-color: #400040; color: white;")
        self.reset_button.clicked.connect(self.clock.reset_timer)
        layout.addWidget(self.reset_button)
        
        self.setLayout(layout)
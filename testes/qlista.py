from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QListWidget, QListWidgetItem, QHBoxLayout, QLabel, QPushButton, QCheckBox, QLineEdit
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt

class TaskItem(QWidget):
    """Widget personalizado para cada item da lista de tarefas"""
    def __init__(self, task_name, parent_list, item):
        super().__init__()
        self.parent_list = parent_list  # Lista de tarefas onde este item está
        self.item = item  # Item da lista associado a este widget

        # Layout horizontal (para alinhar os elementos na linha)
        layout = QHBoxLayout(self)

        # Checkbox (para marcar a tarefa como concluída)
        self.checkbox = QCheckBox()
        layout.addWidget(self.checkbox)

        # Nome da tarefa
        self.label = QLabel(task_name)
        layout.addWidget(self.label)

        # Botão de estrela (favorito/concluir)
        self.star_button = QPushButton()
        self.star_button.setIcon(QIcon("⭐"))  # Ícone de estrela
        self.star_button.setCheckable(True)  # Torna o botão "alternável"
        self.star_button.clicked.connect(self.complete_task)  # Conectar ao evento de remoção
        layout.addWidget(self.star_button)

        self.setLayout(layout)

    def complete_task(self):
        """Remove a tarefa da lista ao clicar na estrela"""
        row = self.parent_list.row(self.item)  # Obtém o índice do item
        self.parent_list.takeItem(row)  # Remove o item da lista


class TaskListApp(QWidget):
    """Janela principal com a lista de tarefas"""
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Lista de Tarefas - PySide6")
        self.setGeometry(100, 100, 400, 500)

        # Layout principal
        layout = QVBoxLayout(self)

        # Campo de entrada para adicionar novas tarefas
        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Digite uma nova tarefa...")  # Texto guia
        layout.addWidget(self.task_input)

        # Botão para adicionar tarefas
        self.add_button = QPushButton("Adicionar Tarefa")
        self.add_button.clicked.connect(self.add_task_from_input)  # Conectar ao método
        layout.addWidget(self.add_button)

        # Lista de tarefas
        self.task_list = QListWidget()
        layout.addWidget(self.task_list)

        self.setLayout(layout)

    def add_task(self, task_name):
        """Adiciona uma nova tarefa à lista"""
        item = QListWidgetItem(self.task_list)  # Cria um item na lista
        task_widget = TaskItem(task_name, self.task_list, item)  # Cria o widget personalizado

        item.setSizeHint(task_widget.sizeHint())  # Ajusta o tamanho do item
        self.task_list.addItem(item)  # Adiciona o item à lista
        self.task_list.setItemWidget(item, task_widget)  # Define o widget do item

    def add_task_from_input(self):
        """Adiciona uma tarefa ao clicar no botão"""
        task_text = self.task_input.text().strip()  # Pega o texto e remove espaços extras
        if task_text:  # Só adiciona se não estiver vazio
            self.add_task(task_text)
            self.task_input.clear()  # Limpa o campo de entrada


if __name__ == "__main__":
    app = QApplication([])
    window = TaskListApp()
    window.show()
    app.exec()

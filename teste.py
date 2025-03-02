import json
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *

TASKS_FILE = "tasks.json"

class TaskWidget(QFrame):
    def __init__(self, text, color):
        super().__init__()
        self.setStyleSheet(f"""
            background-color: {color};
            border-radius: 10px;
            padding: 10px;
            font-size: 14px;
            font-weight: bold;
            color: white;
        """)
        self.label = QLabel(text, self)
        self.label.setAlignment(Qt.AlignCenter)
        self.setFixedSize(330, 70)
        self.text = text

class DragDropList(QListWidget):
    def __init__(self, name):
        super().__init__()
        self.setObjectName(name)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDefaultDropAction(Qt.MoveAction)
        self.setSelectionMode(QListWidget.SingleSelection)
        self.setSpacing(8)
        self.setStyleSheet("""
            QListWidget {
                background: #2C2F33;
                border: none;
                border-radius: 10px;
                padding: 10px;
            }
        """)

    def startDrag(self, supported_actions):
        item = self.currentItem()
        if not item:
            return
        widget = self.itemWidget(item)
        if widget:
            drag = QDrag(self)
            mime_data = QMimeData()
            mime_data.setText(widget.text)
            mime_data.setData("application/list-source", self.objectName().encode())
            drag.setMimeData(mime_data)
            pixmap = QPixmap(widget.size())
            pixmap.fill(Qt.transparent)
            painter = QPainter(pixmap)
            widget.render(painter, QPoint(), QRect(), QWidget.RenderFlag.DrawChildren)
            painter.end()
            drag.setPixmap(pixmap)
            if drag.exec(Qt.MoveAction) == Qt.MoveAction:
                self.takeItem(self.row(item))

    def dragEnterEvent(self, event):
        event.acceptProposedAction()

    def dragMoveEvent(self, event):
        event.acceptProposedAction()

    def dropEvent(self, event):
        if event.mimeData().hasText():
            text = event.mimeData().text()
            source_list = event.mimeData().data("application/list-source").data().decode()

            # Verifique se a tarefa já está na lista de destino
            if not any(self.itemWidget(item).text == text for item in self.findItems(text, Qt.MatchExactly)):
                new_item = QListWidgetItem()
                new_item.setSizeHint(QSize(180, 50))
                self.addItem(new_item)

                # Define a cor da nova lista
                color = "#FF5733" if "ToDo" in self.objectName() else "#3498db" if "Doing" in self.objectName() else "#2ecc71"
                widget = TaskWidget(text, color)
                self.setItemWidget(new_item, widget)

                # Remove a tarefa da lista de origem
                list_widget = self.window().findChild(QListWidget, source_list)
                if list_widget:
                    for index in range(list_widget.count()):
                        item = list_widget.item(index)
                        if list_widget.itemWidget(item).text == text:
                            list_widget.takeItem(index)  # Remover item da lista de origem
                            break

                # Salva as mudanças nas tarefas
                self.save_tasks()
                event.acceptProposedAction()

    def save_tasks(self):
        tasks = {
            "ToDo": [],
            "Doing": [],
            "Done": []
        }

        for list_name in tasks.keys():
            list_widget = self.window().findChild(QListWidget, list_name)
            if list_widget:
                for index in range(list_widget.count()):
                    item = list_widget.item(index)
                    widget = list_widget.itemWidget(item)
                    if widget:
                        tasks[list_name].append(widget.text)

        # Agora, vamos salvar a estrutura das tarefas atualizada
        with open(TASKS_FILE, "w") as file:
            json.dump(tasks, file, indent=4)

class AddTaskDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Adicionar Tarefa")
        layout = QVBoxLayout(self)
        self.task_input = QLineEdit(self)
        self.task_input.setPlaceholderText("Digite a nova tarefa...")
        self.add_button = QPushButton("Adicionar")
        self.add_button.clicked.connect(self.accept)
        layout.addWidget(self.task_input)
        layout.addWidget(self.add_button)
        self.setLayout(layout)

class MainWindow(QFrame):
    def __init__(self, expanded):
        super().__init__()
        self.setWindowTitle("Kanban Personalizado")
        self.setStyleSheet("background: #23272A; color: white; font-size: 16px;")
        self.expanded = expanded
        if expanded:
            self.setFixedSize(1050, 850)
        else:
            self.setFixedSize(1125, 850)
        layout = QVBoxLayout(self)

        # Criando um QHBoxLayout para organizar as listas horizontalmente
        horizontal_layout = QHBoxLayout()

        # Criando layouts verticais para cada lista (nome + lista)
        todo_layout = QVBoxLayout()
        doing_layout = QVBoxLayout()
        done_layout = QVBoxLayout()

        self.todo_list = DragDropList("ToDo")
        self.doing_list = DragDropList("Doing")
        self.done_list = DragDropList("Done")

        # Adicionando o nome da lista e a lista de tarefas em cada layout
        todo_layout.addWidget(QLabel("To Do"))
        todo_layout.addWidget(self.todo_list)

        doing_layout.addWidget(QLabel("Doing"))
        doing_layout.addWidget(self.doing_list)

        done_layout.addWidget(QLabel("Done"))
        done_layout.addWidget(self.done_list)

        # Adicionando os layouts verticais ao layout horizontal
        horizontal_layout.addLayout(todo_layout)
        horizontal_layout.addLayout(doing_layout)
        horizontal_layout.addLayout(done_layout)

        self.add_task_button = QPushButton("Adicionar Tarefa")
        self.add_task_button.clicked.connect(self.open_add_task_dialog)

        # Adicionando o layout horizontal com as listas ao layout principal
        layout.addLayout(horizontal_layout)  # Usando addLayout para adicionar um QHBoxLayout

        # Adicionando o botão de adicionar tarefa ao layout principal
        layout.addWidget(self.add_task_button)
        self.setLayout(layout)
        self.load_tasks()

    def open_add_task_dialog(self):
        dialog = AddTaskDialog(self)
        if dialog.exec():
            task_text = dialog.task_input.text().strip()
            if task_text:
                self.add_task(self.todo_list, task_text, "#FF5733")
                self.todo_list.save_tasks()

    def add_task(self, list_widget, text, color):
        item = QListWidgetItem()
        item.setSizeHint(QSize(180, 70))
        list_widget.addItem(item)
        task_widget = TaskWidget(text, color)
        list_widget.setItemWidget(item, task_widget)

    def load_tasks(self):
        try:
            with open(TASKS_FILE, "r") as file:
                tasks = json.load(file)
                for list_name, items in tasks.items():
                    list_widget = self.findChild(QListWidget, list_name)
                    if list_widget:
                        # Adiciona as tarefas carregadas, mas não cria duplicados
                        existing_items = [list_widget.item(index).text() for index in range(list_widget.count())]

                        for task in items:
                            if task not in existing_items:
                                color = "#FF5733" if "ToDo" in list_name else "#3498db" if "Doing" in list_name else "#2ecc71"
                                self.add_task(list_widget, task, color)
        except FileNotFoundError:
            pass

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
        self.setMinimumSize(310, 70)
        self.text = text

class DragDropList(QListWidget):
    # Sinal para indicar que essa lista foi ativada
    listActivated = Signal(QListWidget)
    
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
        # Conecta o sinal de mudança de seleção para emitir o sinal listActivated
        self.itemSelectionChanged.connect(self.on_item_selection_changed)

    def on_item_selection_changed(self):
        if self.currentItem() is not None:
            self.listActivated.emit(self)

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
            if not any(self.itemWidget(item).text == text for item in self.findItems(text, Qt.MatchExactly)):
                new_item = QListWidgetItem()
                new_item.setSizeHint(QSize(180, 80))
                self.addItem(new_item)
                color = "#FF5733" if "ToDo" in self.objectName() else "#3498db" if "Doing" in self.objectName() else "#2ecc71"
                widget = TaskWidget(text, color)
                self.setItemWidget(new_item, widget)
                list_widget = self.window().findChild(QListWidget, source_list)
                if list_widget:
                    for index in range(list_widget.count()):
                        item = list_widget.item(index)
                        if list_widget.itemWidget(item).text == text:
                            list_widget.takeItem(index)
                            break
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
            self.setFixedSize(1050, 760)
        else:
            self.setFixedSize(1125, 760)
        layout = QVBoxLayout(self)

        self.last_active_list = None

        horizontal_layout = QHBoxLayout()
        todo_layout = QVBoxLayout()
        doing_layout = QVBoxLayout()
        done_layout = QVBoxLayout()

        self.todo_list = DragDropList("ToDo")
        self.doing_list = DragDropList("Doing")
        self.done_list = DragDropList("Done")

        # Conecta os sinais para atualizar a última lista ativa
        self.todo_list.listActivated.connect(self.set_last_active_list)
        self.doing_list.listActivated.connect(self.set_last_active_list)
        self.done_list.listActivated.connect(self.set_last_active_list)

        # Criando os labels com bold para os títulos
        todo_label = QLabel("                          To Do")
        todo_label.setStyleSheet("font-weight: bold; font-size: 22px;")
        doing_label = QLabel("                         Doing")
        doing_label.setStyleSheet("font-weight: bold; font-size: 22px;")
        done_label = QLabel("                          Done")
        done_label.setStyleSheet("font-weight: bold; font-size: 22px;")

        todo_layout.addWidget(todo_label)
        todo_layout.addWidget(self.todo_list)
        doing_layout.addWidget(doing_label)
        doing_layout.addWidget(self.doing_list)
        done_layout.addWidget(done_label)
        done_layout.addWidget(self.done_list)

        horizontal_layout.addLayout(todo_layout)
        horizontal_layout.addLayout(doing_layout)
        horizontal_layout.addLayout(done_layout)

        self.add_task_button = QPushButton("Adicionar Tarefa")
        self.add_task_button.setStyleSheet("""
            font-weight: bold;
            background-color: orange;
            color: white;
            padding: 8px;
            border: none;
            border-radius: 5px;
        """)
        self.add_task_button.clicked.connect(self.open_add_task_dialog)

        self.delete_task_button = QPushButton("Excluir Tarefa")
        self.delete_task_button.setStyleSheet("""
            font-weight: bold;
            background-color: orange;
            color: white;
            padding: 8px;
            border: none;
            border-radius: 5px;
        """)
        self.delete_task_button.clicked.connect(self.delete_selected_task)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.add_task_button)
        buttons_layout.addWidget(self.delete_task_button)

        layout.addLayout(horizontal_layout)
        layout.addLayout(buttons_layout)
        self.setLayout(layout)
        self.load_tasks()

    def set_last_active_list(self, list_widget):
        self.last_active_list = list_widget

    def open_add_task_dialog(self):
        dialog = AddTaskDialog(self)
        if dialog.exec():
            task_text = dialog.task_input.text().strip()
            if task_text:
                self.add_task(self.todo_list, task_text, "#FF5733")
                self.todo_list.save_tasks()

    def add_task(self, list_widget, text, color):
        item = QListWidgetItem()
        item.setSizeHint(QSize(180, 80))
        list_widget.addItem(item)
        task_widget = TaskWidget(text, color)
        list_widget.setItemWidget(item, task_widget)

    def delete_selected_task(self):
        if self.last_active_list is not None:
            current_item = self.last_active_list.currentItem()
            if current_item is not None:
                self.last_active_list.takeItem(self.last_active_list.row(current_item))
                self.last_active_list.save_tasks()

    def load_tasks(self):
        try:
            with open(TASKS_FILE, "r") as file:
                tasks = json.load(file)
                for list_name, items in tasks.items():
                    list_widget = self.findChild(QListWidget, list_name)
                    if list_widget:
                        existing_items = [list_widget.item(index).text() for index in range(list_widget.count())]
                        for task in items:
                            if task not in existing_items:
                                color = "#FF5733" if "ToDo" in list_name else "#3498db" if "Doing" in list_name else "#2ecc71"
                                self.add_task(list_widget, task, color)
        except FileNotFoundError:
            pass


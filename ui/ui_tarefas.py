from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from backend import load_json

class TaskWidget(QFrame):
    def __init__(self, text, color, checked=False):  # Adiciona parâmetro checked
        super().__init__()
        self.layoutCentral = QHBoxLayout()
        self.Vlayout = QVBoxLayout()
        self.setLayout(self.layoutCentral)
        self.setStyleSheet(f"""
            background-color: {color};
            border-radius: 10px;
            padding: 10px;
            font-size: 14px;
            font-weight: bold;
            color: white;
        """)
        self.checkbox = QCheckBox(self)
        self.checkbox.setChecked(checked)  # Define o estado inicial do checkbox
        self.checkbox.stateChanged.connect(self.on_checkbox_changed)  # Conecta o sinal de mudança
        self.spacer = QSpacerItem(1,1)
        self.label = QTextEdit(text)
        self.label.setReadOnly(True)
        self.label.setFixedSize(230, 70)
        self.label.setStyleSheet(f"background-color: #ffffff; color: {color};") 
        self.layoutCentral.addWidget(self.checkbox, alignment=Qt.AlignTop)
        self.layoutCentral.addLayout(self.Vlayout)
        self.Vlayout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignLeft)
        self.Vlayout.addItem(self.spacer)
        self.setFixedSize(310, 100)
        self.text = text

    def on_checkbox_changed(self, state):
        # Quando o checkbox mudar, salva o estado nas tarefas
        list_widget = self.parent().parent()  # Acessa o QListWidget que contém este TaskWidget
        if isinstance(list_widget, DragDropList):
            list_widget.save_tasks()

class DragDropList(QListWidget):
    listActivated = Signal(QListWidget)
    
    def __init__(self, name, indice):
        super().__init__()
        self.setObjectName(name)
        self.indice = indice
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
                new_item.setSizeHint(QSize(310, 100))
                self.addItem(new_item)
                color = "#FF5733" if "ToDo" in self.objectName() else "#3498db" if "Doing" in self.objectName() else "#2ecc71"
                widget = TaskWidget(text, color)  # Cria com checked=False por padrão ao arrastar
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
        users = load_json.load_file()  # Carrega o JSON
        tasks = []
        
        for list_name in ["ToDo", "Doing", "Done"]:
            list_widget = self.window().findChild(QListWidget, list_name)
            if list_widget:
                for index in range(list_widget.count()):
                    item = list_widget.item(index)
                    widget = list_widget.itemWidget(item)
                    if widget:
                        tasks.append({
                            "text": widget.text,
                            "status": list_name,
                            "checked": 1 if widget.checkbox.isChecked() else 0
                        })
        
        users[self.indice]["tarefas"] = tasks
        load_json.save_file(users)  # Salva no JSON
        print("JSON atualizado:", users[self.indice]["tarefas"])  # Debug

class AddTaskDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(400, 310)
        self.setWindowTitle("Adicionar Tarefa")
        layout = QVBoxLayout(self)
        layout_botoes = QHBoxLayout()
        self.titulo = QLabel("ADICIONAR TASK")
        self.titulo.setStyleSheet("font-size: 20px; font-weight: bold ;")
        self.task_input = QTextEdit(self)
        self.task_input.setFixedSize(360, 200)
        self.task_input.setStyleSheet("border-radius: 5px; background-color: #2C2F33;")
        self.task_input.setPlaceholderText("Digite a nova tarefa...")
        self.botao_cancelar = QPushButton("Cancelar")
        self.botao_cancelar.setStyleSheet("background-color: #f87000; font-weight: bold ; border-radius: 10px ;")
        self.botao_cancelar.setFixedSize(170, 40)
        self.add_button = QPushButton("Adicionar")
        self.add_button.setFixedSize(170, 40)
        self.add_button.setStyleSheet("background-color: #f87000; font-weight: bold ; border-radius: 10px ;")
        self.add_button.clicked.connect(self.verificar)  # Chama o método verificar
        self.botao_cancelar.clicked.connect(lambda: self.close())

        layout.addWidget(self.titulo, alignment=Qt.AlignCenter)
        layout.addWidget(self.task_input, alignment=Qt.AlignCenter)
        layout.addLayout(layout_botoes)
        layout_botoes.addWidget(self.add_button)
        layout_botoes.addWidget(self.botao_cancelar)
        self.setLayout(layout)

    def verificar(self):
        print("ta aqui")
        if len(self.task_input.toPlainText()) >= 5:
            self.accept()

class MainWindow(QFrame):
    def __init__(self, expanded, indice, status):
        super().__init__()
        self.setWindowTitle("Kanban Personalizado")
        self.setStyleSheet("background: #23272A; color: white; font-size: 16px;")
        self.expanded = expanded
        self.statusPatente = status
        self.indice = indice
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

        self.todo_list = DragDropList("ToDo", self.indice)
        self.doing_list = DragDropList("Doing", self.indice)
        self.done_list = DragDropList("Done", self.indice)

        self.todo_list.listActivated.connect(self.set_last_active_list)
        self.doing_list.listActivated.connect(self.set_last_active_list)
        self.done_list.listActivated.connect(self.set_last_active_list)

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
        self.add_task_button.setMinimumHeight(50)
        self.add_task_button.setStyleSheet("QPushButton {background-color: #f87000; color: white; font-weight: bold; font-size: 18px;} QPushButton:hover {background-color: #000000; color: white; font-size: 19px;}")
        self.add_task_button.clicked.connect(self.open_add_task_dialog)

        self.delete_task_button = QPushButton("Excluir Tarefa")
        self.delete_task_button.setMinimumHeight(50)
        self.delete_task_button.setStyleSheet("QPushButton {background-color: #f87000; color: white; font-weight: bold; font-size: 18px;} QPushButton:hover {background-color: #000000; color: white; font-weight: bold; font-size: 19px;}")
        self.delete_task_button.clicked.connect(self.delete_selected_task)

        self.complete_task_button = QPushButton("Concluir Agora")
        self.complete_task_button.setMinimumHeight(50)
        self.complete_task_button.setStyleSheet("QPushButton {background-color: #f87000; color: white; font-weight: bold; font-size: 18px;} QPushButton:hover {background-color: #000000; color: white; font-weight: bold; font-size: 19px;}")
        self.complete_task_button.clicked.connect(self.conclued_selected_task)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.add_task_button)
        buttons_layout.addWidget(self.delete_task_button)
        buttons_layout.addWidget(self.complete_task_button)

        layout.addLayout(horizontal_layout)
        layout.addLayout(buttons_layout)
        self.setLayout(layout)
        self.load_tasks()

    def set_last_active_list(self, list_widget):
        self.last_active_list = list_widget

    def open_add_task_dialog(self):
        dialog = AddTaskDialog(self)
        if dialog.exec():
            task_text = dialog.task_input.toPlainText()
            if task_text:
                self.add_task(self.todo_list, task_text, "#FF5733")
                self.todo_list.save_tasks()

    def add_task(self, list_widget, text, color, checked=False):  # Adiciona parâmetro checked
        item = QListWidgetItem()
        item.setSizeHint(QSize(180, 100))
        list_widget.addItem(item)
        task_widget = TaskWidget(text, color, checked)  # Passa o estado do checkbox
        list_widget.setItemWidget(item, task_widget)

    def conclued_selected_task(self):
        if self.last_active_list is not None:
            current_item = self.last_active_list.currentItem()
            if current_item is not None:
                self.statusPatente.atualizar_xp(100)
                self.last_active_list.takeItem(self.last_active_list.row(current_item))
                self.last_active_list.save_tasks()  # Salva as alterações no JSON
                return

    def delete_selected_task(self):
        if self.last_active_list is not None:
            current_item = self.last_active_list.currentItem()
            if current_item is not None:
                self.last_active_list.takeItem(self.last_active_list.row(current_item))
                self.last_active_list.save_tasks()  # Salva as alterações no JSON

    def load_tasks(self):
        users = load_json.load_file()
        print("Carregando tarefas:", users[self.indice]["tarefas"])  # Debug
        tarefas = users[self.indice]["tarefas"]
        
        list_widgets = {
            "ToDo": self.todo_list,
            "Doing": self.doing_list,
            "Done": self.done_list
        }
        
        # Limpa as listas antes de recarregar
        for list_widget in list_widgets.values():
            list_widget.clear()
        
        # Recarrega as tarefas
        for task in tarefas:
            text = task.get("text", "")
            status = task.get("status", "ToDo")
            checked = bool(task.get("checked", 0))
            color = "#FF5733" if status == "ToDo" else "#3498db" if status == "Doing" else "#2ecc71"
            list_widget = list_widgets.get(status)
            if list_widget and text:
                self.add_task(list_widget, text, color, checked)
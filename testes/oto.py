from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QListWidget, QListWidgetItem
import sys

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Criação do QListWidget
        self.list_widget = QListWidget(self)

        # Adicionar item com widget personalizado
        item = QListWidgetItem()
        self.list_widget.addItem(item)

        # Criar o TaskItem com nome de tarefa
        task_widget = TaskItem("Comprar leite")

        # Associar o widget personalizado ao item
        self.list_widget.setItemWidget(item, task_widget)

        # Layout principal
        layout = QVBoxLayout()
        layout.addWidget(self.list_widget)
        self.setLayout(layout)

        self.setWindowTitle("QListWidget com TaskItem")
        self.resize(300, 200)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())

import qt_material
import qdarktheme
import qdarkstyle
import customtkinter as ctk
from qt_material import list_themes

print(list_themes())  # Exibe todos os temas disponíveis 

class aplicar_tema_dark:
    def __init__(self, app):
        # qt_material.apply_stylesheet(app, theme="dark_cyan.xml")
        # app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyside6'))
        # ctk.set_appearance_mode("dark")
        app.setStyleSheet(qdarktheme.load_stylesheet("dark"))



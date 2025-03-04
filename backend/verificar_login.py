from backend import load_json
from tela_inicial import janela_principal
import re
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *

def verificar_login(self, login, senha):
    users = load_json.load_file()
    if users == []:
        self.mensagemStatus.configstyle("Usuário não existente", 12, "d91717")
        return
    print(users)
    indice = -1
    for user in users:
        indice += 1
        if user["login"] == login and user["senha"] == senha:
            self.janela = janela_principal(user, indice)
            self.janela.show()
            self.close()
        else:
            self.mensagemStatus.configstyle("Usuário ou senha incorretos", 12, "d91717")
            print("usuário não encontrado")   

def cadastrar(self, login, senha):
    
    if not (3 <= len(login) <=15):
        self.mensagemStatus.configstyle("Nome deve conter 3 a 15 digitos", 12, "d91717")
        return
    
    if not bool(re.fullmatch(r'[A-Za-z0-9]+', login)):
        self.mensagemStatus.configstyle("Nome deve conter apenas letras e numeros ", 12, "d91717")
        return
    
    
    if not (8 <= len(senha) <=20):
        self.mensagemStatus.configstyle("A senha deve conter 8 a 20 digitos", 12, "d91717")
        return
    if not re.search(r'[A-Z]', senha):
        self.mensagemStatus.configstyle("A senha deve conter uma letra maiúscula", 12, "d91717")
        return
    if not re.search(r'\d', senha):
        self.mensagemStatus.configstyle("A senha deve conter um número", 12, "d91717")
        return
    if not re.search(r'[#@*!&]', senha):
        self.mensagemStatus.configstyle("A senha deve conter um caractere especial", 12, "d91717")
        return
    if " " in senha:
        self.mensagemStatus.configstyle("A senha deve conter espaços", 12, "d91717")
        return
    
    users = load_json.load_file()
    print(users)
    for user in users:
        if user["login"] == login:
            self.mensagemStatus.configstyle("Usuário Já existente escolha outro, BURRO", 12, "d91717")
            return 
        
        
    users.append(
        {
            "login": login,
            "senha": senha,
            "xp": 0,
            "xp_variavel": 0,
            "diarias": [],
            "tarefas": [], 
            "principal": " "
        }
    )
    self.mensagemStatus.configstyle("Usuário cadastrado com sucesso", 12, "b7ff44")
    print(users)
    load_json.save_file(users)  


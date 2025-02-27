from backend import load_json
from tela_inicial import janela_principal

def verificar_login(self, login, senha):
    users = load_json.load_file()
    print(users)
    indice = -1
    for user in users:
        indice += 1
        if user["login"] == login and user["senha"] == senha:
            self.janela = janela_principal(user, indice)
            self.janela.show()
            self.close()
        else: 
            print("usuário não encontrado")   

def cadastrar(self, login, senha):
    users = load_json.load_file()
    print(users)
    for user in users:
        if user["login"] == login:
            return print("usuário já existe")
        
    users.append(
        {
            "login": login,
            "senha": senha,
            "xp": 0,
            "xp_variavel": 0,
            "tarefas": []
        }
    )
    print(users)
    load_json.save_file(users)  


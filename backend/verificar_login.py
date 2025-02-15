def verificar_login(self, dados, login, senha, janela):
    users = dados
    for user in users:
        if user["login"] == login and user["senha"] == senha:
            self.janela = janela
            self.janela.show()
            self.close()
        else: 
            print("usuário não encontrado")   

def cadastrar(self, dados, login, senha):
    users = dados
    for user in users:
        if user["login"] == login:
            return print("usuário já existe")
        
        dados.append(
            {
                "login": login,
                "senha": senha,
                "xp": 0,
                "tarefas": []
            }
        )   


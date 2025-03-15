import os
import json
from cryptography.fernet import Fernet

# === CHAVE EMBUTIDA DIRETO NO CÓDIGO ===
# Isso aqui é tipo tatuagem no código: "Gabi e Moranguinha para sempre" 😍
CHAVE_FIXA = b"9IUXyHhJ8mWd1LGL3PnGAnV9h31uxBu3TUfsM1PcRpM="

fernet = Fernet(CHAVE_FIXA)

# === DEFININDO CAMINHOS DE ARQUIVOS ===

user = os.getlogin()
base_dir = os.path.join("C:\\Users", user, "Documents", "Register Program")
json_file = os.path.join(base_dir, "dados.json")

if not os.path.exists(base_dir):
    os.makedirs(base_dir, exist_ok=False)

# === FUNÇÃO PARA LER OS DADOS (descriptografado) ===

def load_file():
    try:
        with open(json_file, "rb") as f:
            encrypted_data = f.read()
        decrypted_data = fernet.decrypt(encrypted_data)
        return json.loads(decrypted_data.decode('utf-8'))
    except (FileNotFoundError, json.JSONDecodeError, Exception):
        return []

# === FUNÇÃO PARA SALVAR OS DADOS (criptografado) ===

def save_file(dados):
    json_data = json.dumps(dados, ensure_ascii=False, indent=4).encode('utf-8')
    encrypted_data = fernet.encrypt(json_data)
    with open(json_file, "wb") as f:
        f.write(encrypted_data)

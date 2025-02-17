import os
import json

local = os.path.dirname(os.path.abspath(__file__))
local_dados = os.path.join(local, "dados.json")

def load_file():
    try:
        with open(local_dados, "r") as f:
            return json.load(f)
    except (FileNotFoundError | FileNotFoundError):
        return []
    
def save_file(dados):
    with open(local_dados, 'w') as f:
        json.dump(dados, f)    
    
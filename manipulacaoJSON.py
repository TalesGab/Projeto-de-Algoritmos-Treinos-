import json
caminho = "treinoUsuario.json"

def treinoUsuarioAtualizado() -> dict:
    with open(caminho, 'r', encoding= "UTF-8") as arquivo:
        bd = json.load(arquivo)
    return bd

def atualizarTreino(bd: dict) -> None:
    with open(caminho, 'w', encoding="UTF-8") as arquivo:
        json.dump(bd, arquivo, indent=4)
    return
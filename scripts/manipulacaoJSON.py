import json
caminho = "data/treinoUsuario.json"

def treinoUsuarioAtualizado() -> dict:
    with open(caminho, 'r', encoding= "UTF-8") as arquivo:
        bd = json.load(arquivo)
    return bd

def atualizarTreino(treino: dict, nome: str) -> None:
    bd = treinoUsuarioAtualizado()
    bd[nome] = treino
    with open(caminho, 'w', encoding="UTF-8") as arquivo:
        json.dump(bd, arquivo, indent=4)
    return
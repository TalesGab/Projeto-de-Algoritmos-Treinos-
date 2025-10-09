import json
caminho = "treinoUsuario.json"

def treinoUsuarioAtualizado() -> dict:
    with open(caminho, 'r', encoding= "UTF-8") as arquivo:
        bd = json.load(arquivo)
    return bd

def excluirTreino(dia):
    bd = treinoUsuarioAtualizado()
    treino = bd[dia]
    dicionarioItens = treino["exercicios"][0]

    treino["nomeTreino"] = "OFF"
    dicionarioItens.clear()
    
    with open(caminho, 'w', encoding="UTF-8") as arquivo:
        json.dump(bd, arquivo, indent=4)

def adicionarTreino(dia):
    bd = treinoUsuarioAtualizado()

    treino = bd[dia]
    # Ver lógica que será criada

def editarInformações(dia, editarExercicios):
    bd = treinoUsuarioAtualizado()

    treino = bd[dia]
    
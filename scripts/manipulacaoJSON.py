import json
from rich.console import Console
caminhoTreinosPersonalizados = "data/treinoUsuario.json"
caminhoUsuarios = "data/usuario.json"
caminhoTreinosPadroes = "data/exercicios.json"

console = Console()

def treinoUsuarioAtualizado() -> dict:
    with open(caminhoTreinosPersonalizados, 'r', encoding= "UTF-8") as arquivo:
        bd = json.load(arquivo)
    return bd

def atualizarTreino(treino: dict, usuario: str) -> None:
    usuarioJson = treinoUsuarioAtualizado()
    usuarioJson[usuario] = treino
    with open(caminhoTreinosPersonalizados, 'w', encoding="UTF-8") as arquivo:
        json.dump(usuarioJson, arquivo, indent=4)
    console.print("[bold green]Treino Salvo ✅[/bold green]")
    return

def divisoesExerciciosPadroes() -> dict:
    with open(caminhoTreinosPadroes, 'r', encoding= "UTF-8") as arquivo:
        bd = json.load(arquivo)
    return bd
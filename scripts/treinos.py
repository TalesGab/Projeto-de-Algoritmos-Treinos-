import time
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from scripts.manipulacaoJSON import atualizarTreino, treinoUsuarioAtualizado
from scripts.Menu import loading
from scripts.exercicios import listarExercicios, adicionarExercicio, buscarExercicio
import pandas as pd

console = Console()

def treinos():
    while True:
        bd = treinoUsuarioAtualizado()
        console.clear()
        console.print(Panel("[bold green]💪 Treinos[/bold green]", expand= False))
        qntItens, mapaOpcoes = listarTreinos()
        
        try:
            opcao = int(console.input("\n[bold cyan]Escolha uma opção: [/bold cyan]"))

            if opcao == qntItens + 1:
                buscarTreino()
            elif opcao == qntItens + 2:
                criarTreino()
            elif opcao == qntItens + 3:
                # menuAnterior()
                break
            elif opcao in mapaOpcoes:
                diaEscolhido = mapaOpcoes[opcao]
                nomeTreinoEscolhido = bd[diaEscolhido]["nomeTreino"]

                loading(f"Acessando treino {nomeTreinoEscolhido} ({diaEscolhido})")
                treinoSelecionado(diaEscolhido)
            else:
                console.print("[red]⚠ Opção inválida, tente novamente.[/red]")
                time.sleep(2)
        except ValueError:
            console.print("[red]⚠ Digite um número válido.[/red]")
            time.sleep(2)

def listarTreinos():
    bd = treinoUsuarioAtualizado()
    contador = 0
    mapaOpcoes = {}

    for dia, treino in bd.items():
        if treino["nomeTreino"] != "OFF":
            contador += 1
            mapaOpcoes[contador] = dia
            console.print(f"🗓️  {dia}")
            console.print(f"[grey19]|[/grey19] [yellow]{contador}[/yellow] - {treino["nomeTreino"]}\n")
        else: 
            console.print(f"🗓️  {dia}")
            console.print(f"[grey19]|[/grey19] [grey19]{treino["nomeTreino"]}[/grey19]\n")

    console.print("[grey19]---------------------[/grey19]")
    console.print(f"[yellow]{contador + 1}[/yellow] - Buscar treino 🔎")
    console.print(f"[yellow]{contador + 2}[/yellow] - Criar treino ➕️")
    console.print(f"[yellow]{contador + 3}[/yellow] - Voltar 🔙")

    return contador, mapaOpcoes

def buscarTreino():
    while True:
        bd = treinoUsuarioAtualizado()
        busca = console.input("[bold cyan]Digite o nome do treino: [/bold cyan]")
        loading(f"Procurando treino: {busca}")
        time.sleep(2)
        while True:
            contador = 0
            console.clear()
            console.print(Panel("[bold green]💪 Treinos[/bold green]", expand= False))
            opcoesDisponiveis = []   
            
            for dia, treino in bd.items():
                nomeTreino = treino["nomeTreino"]
                if busca.lower() in nomeTreino.lower() and treino["nomeTreino"] != "OFF":
                    contador += 1
                    opcoesDisponiveis.append({
                        "indice": (contador),
                        "dia": dia,
                        "nomeTreino": nomeTreino
                    })

            if opcoesDisponiveis:
                for item in opcoesDisponiveis:
                    console.print(f"🗓️  {item["dia"]}")
                    console.print(f"[grey19]|[/grey19] [yellow]{item["indice"]}[/yellow] - {item["nomeTreino"]}\n") 
                opcaoMax = contador + 1
            else:
                console.print("[bold red]⚠ Nenhum treino encontrado com essa busca.[/bold red]\n")
                opcaoMax = 1

            console.print("[grey19]---------------------[/grey19]")
            console.print(f"[yellow]{opcaoMax}[/yellow] - Voltar 🔙")

            try:
                opcao = int(console.input("\n[bold cyan]Escolha uma opção: [/bold cyan]"))

                if opcao == opcaoMax:
                    return
                elif 1 <= opcao <= contador:
                    itemEscolhido = opcoesDisponiveis[opcao - 1]
                    diaEscolhido = itemEscolhido["dia"]
                    nomeTreinoEscolhido = itemEscolhido["nomeTreino"]

                    loading(f"Acessando treino {nomeTreinoEscolhido} ({diaEscolhido})")
                    treinoSelecionado(bd, diaEscolhido)
                    return
                else: 
                    console.print("[red]⚠ Opção inválida, tente novamente.[/red]")
                    time.sleep(2)
            except ValueError:
                console.print("[red]⚠ Digite um número válido.[/red]")
                time.sleep(2)
    
def treinoSelecionado(dia: str):
    while True:
        bd = treinoUsuarioAtualizado()
        console.clear()
        treino = bd[dia]
        nome = treino["nomeTreino"]

        console.print(Panel(f"[bold green]🗓️  {dia}[/bold green]", expand=False))
        console.print(f"[bold]🏋️  {nome}[/bold]")

        listarExercicios(treino)

        console.print("[grey19]---------------------[/grey19]")
        console.print(f"[yellow]1[/yellow] - Editar treino ✏️")
        console.print(f"[bold red]2 - EXCLUIR treino[/bold red] ❌")
        console.print(f"[yellow]3[/yellow] - Voltar 🔙")

        try:
            opcao = int(console.input("\n[bold cyan]Escolha uma opção: [/bold cyan]"))

            if opcao == 1:
                loading(f"Editando treino {nome}")
                editarTreino(dia)
            elif opcao == 2:
                while True:    
                    resposta = console.input("[bold yellow]⚠ Tem certeza que deseja EXCLUIR o treino (S/N)? [/bold yellow]").upper()
                    
                    if resposta == 'S':
                        excluirTreino(dia)
                        return
                    elif resposta == 'N':
                        break
                    else:
                        console.print("[red]⚠ Digite uma opção válida.[/red]")
            elif opcao == 3:
                return
            else:
                console.print("[red]⚠ Opção inválida, tente novamente.[/red]")
                time.sleep(2)
        except ValueError:
            console.print("[red]⚠ Digite um número válido.[/red]")
            time.sleep(2)

def criarTreino():
    while True:
        bd = treinoUsuarioAtualizado()
        console.clear()
        dicioAux = {}
        contador = 0

        console.print(Panel("[bold green]📌  Semana[/bold green]", expand=False))
        for diaSemana in bd.keys():
            treino = bd[diaSemana]
            if treino["nomeTreino"] != "OFF":
                contador += 1
                dicioAux[contador] = diaSemana

        if dicioAux:
            for key, valor in dicioAux.items():
                console.print(f"[yellow]{key}[/yellow] - 🗓️  {valor}")
            numVoltar = max(dicioAux, key=dicioAux.get) + 1
            console.print("\n[grey19]---------------------[/grey19]")
            console.print(f"[yellow]{numVoltar}[/yellow] - Voltar 🔙")
        else: 
            console.print("[bold red]⚠ Nenhum dia vago.[/bold red]\n")

        try:
            opcao = int(console.input("\n[bold cyan]Escolha uma opção: [/bold cyan]"))


            if opcao == numVoltar:
                return
            elif opcao in dicioAux.keys():
                nomeTreinoNovo = console.input("\n[bold cyan]Digite o nome do novo treino: [/bold cyan]")
                loading(f"Criando treino {nomeTreinoNovo}")
                adicionarExercicio(dicioAux[opcao], nomeTreinoNovo)
            else:
                console.print("[red]⚠ Opção inválida, tente novamente.[/red]")
                time.sleep(2)
        except ValueError:
            console.print("[red]⚠ Digite um número válido.[/red]")
            time.sleep(2)

def editarTreino(dia: str):
    while True:
        bd = treinoUsuarioAtualizado()
        console.clear()
        treino = bd[dia]
        nome = treino["nomeTreino"]

        console.print(Panel(f"[bold green]🗓️  {dia}[/bold green]", expand=False))
        console.print(f"[bold]🏋️  {nome} (editando...)[/bold]")

        maiorID, IDs = listarExercicios(treino, None, True)
        console.print("[grey19]--------------------------------[/grey19]")
        console.print(f"[yellow]{maiorID + 1}[/yellow] - Editar nome do treino ✏️")
        console.print(f"[yellow]{maiorID + 2}[/yellow] - Buscar exercício 🔎")
        console.print(f"[yellow]{maiorID + 3}[/yellow] - Voltar 🔙")
        
        try:
            opcao = int(console.input("\n[bold cyan]Escolha uma opção: [/bold cyan]"))
        
            if opcao == (maiorID + 1):
                nomeNovoTreino = console.input("\n[bold cyan]Digite o novo nome do treino: [/bold cyan]")
                loading(f"Alterando nome do treino {nome} para {nomeNovoTreino}")
                editarNomeTreino(dia, nomeNovoTreino)
                return
            elif opcao == (maiorID + 2):
                buscarExercicio(dia)
            elif opcao == (maiorID + 3):
                return
            elif opcao :
                pass
            else:
                console.print("[red]⚠ Digite um número válido.[/red]")
                time.sleep(2)
        except ValueError:
            console.print("[red]⚠ Digite um número válido.[/red]")
            time.sleep(2)

def excluirTreino(dia: str):
    bd = treinoUsuarioAtualizado()
    treino = bd[dia]
    dicionarioItens = treino["exercicios"][0]

    treino["nomeTreino"] = "OFF"
    dicionarioItens.clear()
    atualizarTreino(bd)
    return
    
def editarNomeTreino(dia: str, nomeNovo: str):
    bd = treinoUsuarioAtualizado()
    treino = bd[dia]
    treino["nomeTreino"] = nomeNovo.upper()
    
    atualizarTreino(bd)
    return

#console.print("[yellow]2[/yellow] - Adicionar exercício ➕️")
      #  console.print("[yellow]3[/yellow] - Excluir exercício ❌")#
if __name__ == "__main__":
    treinos()

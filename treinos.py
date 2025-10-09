import time
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from manipulacaoJSON import *
from Menu import loading
from exercicios import listarExercicios, adicionarExercicio
import pandas as pd

console = Console()

def treinos():
    while True:
        bd = treinoUsuarioAtualizado()
        console.clear()
        console.print(Panel("[bold green]💪 Treinos[/bold green]", expand= False))
        qntItens, mapaOpcoes = listarTreinos(bd)
        
        try:
            opcao = int(console.input("\n[bold cyan]Escolha uma opção: [/bold cyan]"))

            if opcao == qntItens + 1:
                buscarTreino(bd)
            elif opcao == qntItens + 2:
                criarTreino(bd)
            elif opcao == qntItens + 3:
                # menuAnterior()
                break
            elif opcao in mapaOpcoes:
                diaEscolhido = mapaOpcoes[opcao]
                nomeTreinoEscolhido = bd[diaEscolhido]["nomeTreino"]

                loading(f"Acessando treino {nomeTreinoEscolhido} ({diaEscolhido})")
                treinoSelecionado(bd, diaEscolhido)
            else:
                console.print("[red]⚠ Opção inválida, tente novamente.[/red]")
                time.sleep(2)
        except ValueError:
            console.print("[red]⚠ Digite um número válido.[/red]")
            time.sleep(2)

def listarTreinos(bd: dict):
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

def buscarTreino(bd: dict):
    while True:
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
    
def treinoSelecionado(bd: dict, dia: str):
    while True:
        console.clear()
        treino = bd[dia]
        nome = treino["nomeTreino"]

        console.print(Panel(f"[bold green]🗓️  {dia}[/bold green]", expand=False))
        console.print(f"[bold]🏋️  {nome}[/bold]")

        MaiorID, IDs = listarExercicios(treino)

        console.print("[grey19]---------------------[/grey19]")
        console.print(f"[yellow]{MaiorID + 1}[/yellow] - Editar treino ✏️")
        console.print(f"[bold red]{MaiorID + 2} - EXCLUIR treino[/bold red] ❌")
        console.print(f"[yellow]{MaiorID + 3}[/yellow] - Voltar 🔙")

        try:
            opcao = int(console.input("\n[bold cyan]Escolha uma opção: [/bold cyan]"))

            if opcao == (MaiorID + 1):
                # Chamar função para editar os exercicios e ter a opção de editar nome
                editarTreino(bd, dia)
            elif opcao == (MaiorID + 2):
                while True:    
                    resposta = console.input("[bold yellow]⚠ Tem certeza que deseja EXCLUIR o treino (S/N)? [/bold yellow]").upper()
                    
                    if resposta == 'S':
                        excluirTreino(dia)
                        return
                    elif resposta == 'N':
                        break
                    else:
                        console.print("[red]⚠ Digite uma opção válida.[/red]")
            elif opcao == (MaiorID + 3):
                return
            else:
                console.print("[red]⚠ Opção inválida, tente novamente.[/red]")
                time.sleep(2)
        except ValueError:
            console.print("[red]⚠ Digite um número válido.[/red]")
            time.sleep(2)

def criarTreino(bd: dict):
    while True:
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
                console.print("[red]⚠ Digite um número válido.[/red]")
                time.sleep(2)
        except ValueError:
            console.print("[red]⚠ Digite um número válido.[/red]")
            time.sleep(2)

def editarTreino(bd: dict, dia: str):
    while True:
        console.clear()
        treino = bd[dia]
        nome = treino["nomeTreino"]

        console.print(Panel(f"[bold green]🗓️  {dia}[/bold green]", expand=False))
        console.print(f"[bold]🏋️  {nome}[/bold]")

        maiorID, IDs = listarExercicios(treino)
        console.print("[grey19]--------------------------------[/grey19]")
        console.print(f"[yellow]{maiorID + 1}[/yellow] - Editar nome do treino ✏️")
        console.print(f"[yellow]{maiorID + 2}[/yellow] - Buscar exercício ✏️")
        console.print(f"[yellow]{maiorID + 3}[/yellow] - Voltar 🔙")
        
        try:
            opcao = console.input("\n[bold cyan]Escolha uma opção: [/bold cyan]")
        
            if opcao == (maiorID + 1):
                nomeNovoTreino = console.input("\n[bold cyan]Digite o novo nome do treino: [/bold cyan]")
                loading(f"Alterando nome do treino {nome} para {nomeNovoTreino}")
                editarNomeTreino(nome, nomeNovoTreino)
                time.sleep(4)
            elif opcao == (maiorID + 2):
                pass
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

#console.print("[yellow]2[/yellow] - Adicionar exercício ➕️")
      #  console.print("[yellow]3[/yellow] - Excluir exercício ❌")#
if __name__ == "__main__":
    treinos()

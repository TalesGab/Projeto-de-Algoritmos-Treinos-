import time
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from manipulacaoJSON import atualizarTreino, treinoUsuarioAtualizado
from Menu import loading
from exercicios import listarExercicios, ordenarExercicios, adicionarExercicio, buscarExercicio, edicaoDoExercicioSelecionado, editarInformacoesExercicio
import pandas as pd

console = Console()

def treinos(usuario):
    
    while True:
        usuarioJson = treinoUsuarioAtualizado()
        bd = usuarioJson[usuario]
        console.clear()
        console.print(Panel("[bold green]💪 Treinos[/bold green]", expand= False))
        qntItens, mapaOpcoes = listarTreinos(usuario)
        
        try:
            opcao = int(console.input("\n[bold cyan]Escolha uma opção: [/bold cyan]"))

            if opcao == qntItens + 1:
                buscarTreino(usuario)
            elif opcao == qntItens + 2:
                criarTreino(usuario)
            elif opcao == qntItens + 3:
                break
            elif opcao in mapaOpcoes:
                diaEscolhido = mapaOpcoes[opcao]
                for dicionario in bd:
                    if dicionario.get(diaEscolhido):
                        nomeTreinoEscolhido = dicionario[diaEscolhido]["nomeTreino"]

                loading(f"Acessando treino {nomeTreinoEscolhido} ({diaEscolhido})")
                treinoSelecionado(diaEscolhido, usuario)
            else:
                console.print("[red]⚠ Opção inválida, tente novamente.[/red]")
                time.sleep(2)
        except ValueError:
            console.print("[red]⚠ Digite um número válido.[/red]")
            time.sleep(2)

def listarTreinos(usuario: str):
    usuarioJson = treinoUsuarioAtualizado()
    bd = usuarioJson[usuario]
    contador = 0
    mapaOpcoes = {}
    for dicionario in bd:
        for dia, treino in dicionario.items():
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

def buscarTreino(usuario: str) -> None:
    while True:
        usuarioJson = treinoUsuarioAtualizado()
        bd = usuarioJson[usuario]
        busca = console.input("[bold cyan]Digite o nome do treino: [/bold cyan]")
        loading(f"Procurando treino: {busca}")
        time.sleep(2)
        while True:
            contador = 0
            console.clear()
            console.print(Panel("[bold green]💪 Treinos[/bold green]", expand= False))
            opcoesDisponiveis = []   
            
            for dicionario in bd:
                for dia, treino in dicionario.items():
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
                    treinoSelecionado(diaEscolhido, usuario)
                    return
                else: 
                    console.print("[red]⚠ Opção inválida, tente novamente.[/red]")
                    time.sleep(2)
            except ValueError:
                console.print("[red]⚠ Digite um número válido.[/red]")
                time.sleep(2)
    
def treinoSelecionado(dia: str, usuario: str):
    while True:
        ordenarExercicios(usuario, dia)
        usuarioJson = treinoUsuarioAtualizado()
        bd = usuarioJson[usuario]
        console.clear()
        for dicionario in bd:
            if dicionario.get(dia):
                treino = dicionario[dia]
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
                        editarTreino(dia, usuario)
                        break
                    elif opcao == 2:
                        while True:    
                            resposta = console.input("[bold yellow]⚠ Tem certeza que deseja EXCLUIR o treino (S/N)? [/bold yellow]").upper()
                            
                            if resposta == 'S':
                                loading("Excluindo treino")
                                excluirTreino(dia, usuario)
                                console.print("[bold green]Treino excluído com sucesso![/bold green]")
                                time.sleep(2)
                                return
                            elif resposta == 'N':
                                break
                            else:
                                console.print("[red]⚠ Digite uma opção válida.[/red]")
                                time.sleep(2)
                    elif opcao == 3:
                        return
                    else:
                        console.print("[red]⚠ Opção inválida, tente novamente.[/red]")
                        time.sleep(2)
                except ValueError:
                    console.print("[red]⚠ Digite um número válido.[/red]")
                    time.sleep(2)

def criarTreino(usuario: str):
    while True:
        usuarioJson = treinoUsuarioAtualizado()
        bd = usuarioJson[usuario]
        console.clear()
        dicioAux = {}
        contador = 0

        console.print(Panel("[bold green]📌  Semana[/bold green]", expand=False))
        for dicionario in bd:
            for diaSemana in dicionario.keys():
                treino = dicionario[diaSemana]
                if treino["nomeTreino"] == "OFF":
                    contador += 1
                    dicioAux[contador] = diaSemana

        if dicioAux:
            for key, valor in dicioAux.items():
                console.print(f"[yellow]{key}[/yellow] - 🗓️  {valor}")
            numVoltar = len(dicioAux) + 1
            console.print("\n[grey19]---------------------[/grey19]")
            console.print(f"[yellow]{numVoltar}[/yellow] - Voltar 🔙")
        else: 
            numVoltar = 1
            console.print("[bold red]⚠ Nenhum dia vago.[/bold red]\n")
            console.print("\n[grey19]---------------------[/grey19]")
            console.print(f"[yellow]{numVoltar}[/yellow] - Voltar 🔙")

        try:
            opcao = int(console.input("\n[bold cyan]Escolha uma opção: [/bold cyan]"))

            if opcao == numVoltar:
                return
            elif opcao in dicioAux.keys():
                nomeTreinoNovo = console.input("\n[bold cyan]Digite o nome do novo treino: [/bold cyan]")
                loading(f"Criando treino {nomeTreinoNovo}")
                semanaNaLista = dicioAux[opcao]
                adicionarExercicio(semanaNaLista,  nomeTreinoNovo, usuario)
            else:
                console.print("[red]⚠ Opção inválida, tente novamente.[/red]")
                time.sleep(2)
        except ValueError:
            console.print("[red]⚠ Digite um número válido.[/red]")
            time.sleep(2)

def editarTreino(dia: str, usuario: str):
    while True:
        ordenarExercicios(usuario, dia)
        usuarioJson = treinoUsuarioAtualizado()
        bd = usuarioJson[usuario]
        console.clear()
        for dicionario in bd:
            if dicionario.get(dia):
                treino = dicionario[dia]
                nome = treino["nomeTreino"]

                console.print(Panel(f"[bold green]🗓️  {dia}[/bold green]", expand=False))
                console.print(f"[bold]🏋️  {nome} (editando...)[/bold]")

                maiorID, IDs = listarExercicios(treino, None, None, True)
                console.print("[grey19]--------------------------------[/grey19]")
                console.print(f"[yellow]{maiorID}[/yellow] - Editar nome do treino ✏️")
                console.print(f"[yellow]{maiorID + 1}[/yellow] - Buscar exercício 🔎")
                console.print(f"[yellow]{maiorID + 2}[/yellow] - Adicionar exercício ➕")
                console.print(f"[yellow]{maiorID + 3}[/yellow] - Voltar 🔙")
                
                try:
                    opcao = int(console.input("\n[bold cyan]Escolha uma opção: [/bold cyan]"))
                
                    if opcao == maiorID:
                        nomeNovoTreino = console.input("\n[bold cyan]Digite o novo nome do treino: [/bold cyan]")
                        loading(f"Alterando nome do treino {nome} para {nomeNovoTreino}")
                        editarNomeTreino(dia, nomeNovoTreino, usuario)
                        console.print("[bold green]Nome do treino alterado com sucesso![/bold green]")
                        time.sleep(2)
                        break
                    elif opcao == (maiorID + 1):
                        buscarExercicio(dia, usuario)
                        break
                    elif opcao == (maiorID + 2):
                        loading("Adicionando novo exercício")

                        exerciciosTreino = editarInformacoesExercicio(nome, maiorID, treino["exercicios"], True)

                        treino["exercicios"] = exerciciosTreino
                        atualizarTreino(bd, usuario)
                        console.print("[bold green]Treino Salvo![/bold green]")
                        time.sleep(2)
                        break
                    elif opcao == (maiorID + 3):
                        return
                    elif 1 <= opcao <= maiorID:
                        nomeExercicio = treino["exercicios"][opcao - 1]
                        edicaoDoExercicioSelecionado(opcao, dia, usuario, nomeExercicio["nome"])
                        return
                    else:
                        console.print("[red]⚠ Opção inválida, tente novamente.[/red]")
                        time.sleep(2)
                except ValueError:
                    console.print("[red]⚠ Digite um número válido.[/red]")
                    time.sleep(2)

def excluirTreino(dia: str, usuario: str) -> None:
    usuarioJson = treinoUsuarioAtualizado()
    bd = usuarioJson[usuario]
    for dicionario in bd:
            if dicionario.get(dia):
                treino = dicionario[dia]
    dicionarioItens = treino["exercicios"]

    treino["nomeTreino"] = "OFF"
    dicionarioItens.clear()

    atualizarTreino(bd, usuario)
    return
    
def editarNomeTreino(dia: str, nomeNovo: str, usuario: str) -> None:
    usuarioJson = treinoUsuarioAtualizado()
    bd = usuarioJson[usuario]
    for dicionario in bd:
            if dicionario.get(dia):
                treino = dicionario[dia]
    dicionarioItens = treino["exercicios"]

    treino["nomeTreino"] = nomeNovo.upper()
    
    atualizarTreino(bd, usuario)
    console.print("[bold green]Treino Salvo![/bold green]")
    time.sleep(2)
    return
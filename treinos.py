import time
from rich.console import Console
from rich.panel import Panel
from Menu import loading
import json
import pandas as pd

caminho = "treinos.json"

with open(caminho, 'r', encoding= "utf-8") as arquivo:
    bd = json.load(arquivo)

console = Console()

def treinos():
    while True:
        console.clear()
        console.print(Panel("[bold green]💪 Treinos[/bold green]", expand= False))
        qntItens = listarTreinos(bd)
        
        try:
            opcao = int(console.input("\n[bold cyan]Escolha uma opção: [/bold cyan]"))

            if opcao == qntItens + 1:
                buscarTreino(bd)
            elif opcao == qntItens + 2:
                criarTreino(bd)
            elif opcao == qntItens + 3:
                # menuAnterior()
                pass
            elif opcao in [num for num in range(1, (qntItens + 1))]:
                loading("Acessando treino")
            else:
                console.print("[red]⚠ Opção inválida, tente novamente.[/red]")
                time.sleep(2)
        except ValueError:
            console.print("[red]⚠ Opção inválida, tente novamente.[/red]")

def listarTreinos(bd: dict) -> int:
    contador = 0
    for dia, treino in bd.items():
        if treino["nomeTreino"] != "OFF":
            contador += 1
            console.print(f"🗓️  {dia}")
            console.print(f"[grey19]|[/grey19] [yellow]{contador}[/yellow] - {treino["nomeTreino"]}\n")
        else: 
            console.print(f"🗓️  {dia}")
            console.print(f"[grey19]|[/grey19] [grey19]{treino["nomeTreino"]}[/grey19]\n")
    console.print("[grey19]---------------------[/grey19]")
    console.print(f"[yellow]{contador + 1}[/yellow] - Buscar treino 🔎")
    console.print(f"[yellow]{contador + 2}[/yellow] - Criar treino ➕️")
    console.print(f"[yellow]{contador + 3}[/yellow] - Voltar 🔙")
    return contador

def buscarTreino(bd: dict) -> str:
    while True:
        busca = console.input("[bold cyan]Digite o nome do treino: [/bold cyan]")
        while True:
            console.clear()
            console.print(Panel("[bold green]💪 Treinos[/bold green]", expand= False))
            opcoesDisponiveis = []   
            
            for i, (dia, treino) in enumerate(bd.items(), start=1):
                nomeTreino = treino["nomeTreino"]
                if nomeTreino.lower().count(busca.lower()):
                    opcoesDisponiveis.append({
                        "indice": i,
                        "dia": dia,
                        "nomeTreino": nomeTreino
                    })

            if opcoesDisponiveis:
                opcaoMax = opcoesDisponiveis[-1]["indice"] + 1
                for item in opcoesDisponiveis:
                    console.print(f"🗓️  {item[dia]}")
                    console.print(f"| [yellow]{item[i]}[/yellow] - {item["nomeTreino"]}\n") 
            else:
                opcaoMax = 1
                console.print("[bold red]⚠ Nenhum treino encontrado com essa busca.[/bold red]\n")

            console.print("---------------------")
            console.print(f"[yellow]{opcaoMax}[/yellow] - Voltar 🔙")

            try:
                opcao = int(console.input("\n[bold cyan]Escolha uma opção: [/bold cyan]"))

                if opcao == opcaoMax:
                    treinos()
                elif opcoesDisponiveis:
                    loading("Acessando treino")
                else: 
                    console.print("[red]⚠ Opção inválida, tente novamente.[/red]")
                    time.sleep(2)
            except ValueError:
                console.print("[red]⚠ Opção inválida, tente novamente.[/red]")
                time.sleep(2)
    

def criarTreino(bd):
    pass

def voltar():
    #menuPrincipal()
    pass

if __name__ == "__main__":
    treinos()

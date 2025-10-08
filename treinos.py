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
        listarTreinos(bd)
        
        opcao = console.input("\n[bold cyan]Escolha uma opção: [/bold cyan]")

        if opcao in [str(num) for num in range(1, 8)]:
            loading("Acessando treino")

        elif opcao == '8':
            buscarTreino(bd)
        elif opcao == '9':
            # menu()
            pass
        else:
            console.print("[red]⚠ Opção inválida, tente novamente.[/red]")
            time.sleep(2)

def listarTreinos(bd: dict) -> str:
    for i, (dia, treino) in enumerate(bd.items(), start=1):
        console.print(f"🗓️  {dia}")
        console.print(f"| [yellow]{i}[/yellow] - {treino["nomeTreino"]}\n")
    console.print("---------------------")
    console.print("[yellow]8[/yellow] - Buscar treino 🔎")
    console.print("[yellow]9[/yellow] - Voltar")

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
    

def criarTreino():
    pass

def voltar():
    #menuPrincipal()
    pass

if __name__ == "__main__":
    treinos()

import time
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from Menu import loading
import json
import pandas as pd

def treinoUsuario():
    caminho = "treinoUsuario.json"
    with open(caminho, 'r', encoding= "utf-8") as arquivo:
        bd = json.load(arquivo)
    return bd

console = Console()

def treinos(bd: dict):
    while True:
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
                return
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

        console.print(Panel(f"[bold green]🗓️  {dia}[/bold green]", expand=False))
        console.print(f"[bold]🏋️  {treino["nomeTreino"]}[/bold]")

        # Pandas
        df = pd.DataFrame(treino["exercicios"])
        df = df.sort_values("idExercicio").reset_index(drop=True)
        df_Arrumado = df.rename(columns={
            "nomeDivisao": "Divisão",
            "nome": "Exercício",
            "equipamento": "Equipamento",
            "repeticao": "Repetições",
            "series": "Séries",
            "peso": "Peso"
        })
        
        colunas = ["Divisão", "Exercício", "Equipamento", "Repetições", "Séries", "Peso"]

        # Rich Table
        tabela = Table(show_header=True, header_style="bold")
        tabela.add_column("Índice", justify="center")

        for coluna in colunas:
            tabela.add_column(coluna, justify="center")

        for indice, linha in df_Arrumado.iterrows():
            tabela.add_row(
                f"[yellow]{indice}[/yellow]",
                str(linha["Divisão"]),
                str(linha["Exercício"]),
                str(linha["Equipamento"]),
                str(linha["Repetições"]),
                str(linha["Séries"]),
                str(linha["Peso"])
            )

        console.print(tabela)

        console.print("[yellow]1[/yellow] - Editar treino ✏️")
        console.print("[bold red]2 - EXCLUIR treino[/bold red] ❌")
        console.print("[yellow]3[/yellow] - Voltar 🔙")

        try:
            opcao = int(console.input("\n[bold cyan]Escolha uma opção: [/bold cyan]"))

            if opcao == 1:
                return
            elif opcao == 2:
                while True:    
                    resposta = console.input("[bold yellow]⚠ Tem certeza que deseja EXCLUIR o treino (S/N)? [/bold yellow]").upper()
                    
                    if resposta == 'S':
                        # apagar
                        break
                    elif resposta == 'N':
                        break
                    else:
                        console.print("[red]⚠ Opção inválida, tente novamente.[/red]")
        except ValueError:
            console.print("[red]⚠ Digite um número válido.[/red]")

def criarTreino(bd):
    pass

if __name__ == "__main__":
    bd = treinoUsuario()
    treinos(bd)

import time
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from Menu import loading
from manipulacaoJSON import treinoUsuarioAtualizado
import pandas as pd

console = Console()

def listarExercicios(treino: dict, existeFiltro: list = None, mostrarIDs: bool = False) -> tuple[int, list[int]]:
    # Pandas
    df = pd.DataFrame(treino["exercicios"])
    df = df.sort_values("idExercicio").reset_index(drop=True)

    existeFiltro = existeFiltro if existeFiltro is not None else []
    existeFiltroLower = [nome.lower() for nome in existeFiltro]

    df_utilizado = df.copy()

    if existeFiltroLower:
        df_utilizado = df[df["nome"].str.lower().isin(existeFiltroLower)].copy()

        if df_utilizado.empty:
            console.print("[bold red]⚠ Nenhum exercício encontrado com essa busca.")
            return 0, []

        # console.print(f"[bold cyan]Visualizando exercícios filtrados por nome:[/bold cyan]")

    maiorID = int(df_utilizado["idExercicio"].max()) if not df.empty else 0

    df_Arrumado = df_utilizado.rename(columns={
        "nome": "Exercício",
        "nomeDivisao": "Divisão",
        "equipamento": "Equipamento",
        "repeticao": "Repetições",
        "series": "Séries",
        "peso": "Peso"
    })
    
    colunas = ["Exercício", "Divisão", "Equipamento", "Repetições", "Séries", "Peso"]

    # Rich Table
    tabela = Table(show_header=True, header_style="bold")

    if mostrarIDs:
        tabela.add_column("ID", justify="center")

    for coluna in colunas:
        tabela.add_column(coluna, justify="center")

    for indice, linha in df_Arrumado.iterrows():
        ID = int(linha["idExercicio"])
        linhasUtilizadas = [
            str(linha["Exercício"]),
            str(linha["Divisão"]),
            str(linha["Equipamento"]),
            str(linha["Repetições"]),
            str(linha["Séries"]),
            str(linha["Peso"])
        ]

        if mostrarIDs:
            linhasUtilizadas.insert(0, f"[yellow]{ID}[/yellow]")
        
        tabela.add_row(*linhasUtilizadas)

    IDs = df_utilizado["idExercicio"].to_list()

    console.print(tabela)
    return maiorID, IDs

def adicionarExercicio(dia: str, nomeEscolhido: str):
    bd = treinoUsuarioAtualizado()
    treino = bd[dia]

    while True:
        console.print(Panel(f"[bold green]🗓️  {dia}[/bold green]", expand=False))
        console.print(f"[bold]🏋️  {nomeEscolhido}[/bold]")

def buscarExercicio(dia: str):
    while True:
        bd = treinoUsuarioAtualizado()
        treino = bd[dia]

        busca = console.input("[bold cyan]Digite o nome do exercício: [/bold cyan]")
        loading(f"Procurando exercício: {busca}")
        time.sleep(2)
        while True:
            console.clear()
            console.print(Panel(f"[bold green]🏋️  {treino}[/bold green]", expand= False))
            exerciciosEscolhidos = []   
            
            for exercicio in treino["exercicios"]:
                for chave, valor in exercicio.items():
                    nomeExercicio = exercicio[chave]
                    if busca.lower() in nomeExercicio.lower() and treino[chave] != "OFF":
                        exerciciosEscolhidos.append(nomeExercicio)

            if nomeExercicio:
                opcaoMax, IDs = listarExercicios(treino, exerciciosEscolhidos)
            else:
                console.print("[bold red]⚠ Nenhum treino encontrado com essa busca.[/bold red]\n")
                opcaoMax = 1

            console.print("\n[grey19]---------------------[/grey19]")
            console.print(f"[yellow]{opcaoMax}[/yellow] - Voltar 🔙")

            try:
                opcao = int(console.input("\n[bold cyan]Escolha uma opção: [/bold cyan]"))

                if opcao == opcaoMax:
                    return
                elif 1 <= opcao <= max(IDs):
                    itemEscolhido = exerciciosEscolhidos[opcao - 1]

                    loading(f"Acessando exercício {itemEscolhido}")
                    # chamar função para edição do exercício
                    return
                else: 
                    console.print("[red]⚠ Opção inválida, tente novamente.[/red]")
                    time.sleep(2)
            except ValueError:
                console.print("[red]⚠ Digite um número válido.[/red]")
                time.sleep(2)
import time
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from Menu import loading
from manipulacaoJSON import treinoUsuarioAtualizado
import pandas as pd

console = Console()

def listarExercicios(treino: dict) -> int:
    # Pandas
    df = pd.DataFrame(treino["exercicios"])
    df = df.sort_values("idExercicio").reset_index(drop=True)

    maiorID = df["idExercicio"].max() if not df.empty else 0

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
    tabela.add_column("ID", justify="center")

    for coluna in colunas:
        tabela.add_column(coluna, justify="center")

    for indice, linha in df_Arrumado.iterrows():
        ID = int(linha["idExercicio"])
        tabela.add_row(
            f"[yellow]{ID}[/yellow]",
            str(linha["Divisão"]),
            str(linha["Exercício"]),
            str(linha["Equipamento"]),
            str(linha["Repetições"]),
            str(linha["Séries"]),
            str(linha["Peso"])
        )

    console.print(tabela)
    return maiorID

def adicionarExercicio(dia: str, nomeEscolhido: str):
    bd = treinoUsuarioAtualizado()
    treino = bd[dia]

    while True:
        console.print(Panel(f"[bold green]🗓️  {dia}[/bold green]", expand=False))
        console.print(f"[bold]🏋️  {nomeEscolhido}[/bold]")


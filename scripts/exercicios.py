import time
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from Menu import loading
from manipulacaoJSON import treinoUsuarioAtualizado, atualizarTreino, divisoesExerciciosPadroes
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
        "series": "Séries",
        "repeticao": "Repetições",
        "peso": "Peso"
    })
    
    colunas = ["Exercício", "Divisão", "Séries", "Repetições", "Peso"]

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
            str(linha["Séries"]),
            str(linha["Repetições"]),
            str(linha["Peso"])
        ]

        if mostrarIDs:
            linhasUtilizadas.insert(0, f"[yellow]{ID}[/yellow]")
        
        tabela.add_row(*linhasUtilizadas)

    IDs = df_utilizado["idExercicio"].to_list()

    console.print(tabela)
    return maiorID, IDs

def adicionarExercicio(dia: str, numeroNaLista: int, nomeEscolhido: str, usuario: str):
    usuarioJson = treinoUsuarioAtualizado()
    treinoUsuario = usuarioJson[usuario]
    semana = treinoUsuario[numeroNaLista]
    treino = semana[dia]
    exerciciosTreino = treino["exercicios"]

    treino["nomeTreino"] = nomeEscolhido
    while True: 
        if len(exerciciosTreino) > 0:
            while True:
                console.clear()
                console.print(Panel(f"[bold green]{nomeEscolhido}[/bold green]", expand=False))
                escolha = console.input("[yellow]Deseja adicionar mais exercícios (s/n)? [yellow]").lower()
                if escolha == 's':
                    idExercicio = (len(exerciciosTreino) + 1) if len(exerciciosTreino) == 1 else len(exerciciosTreino)
                    exerciciosTreino = editarInformacoesExercicio(nomeEscolhido, idExercicio, exerciciosTreino, True)
                    continue
                elif escolha == 'n':
                    treino["exercicios"] = exerciciosTreino
                    atualizarTreino(treinoUsuario, usuario)
                    return
                else: 
                    console.print("[red]⚠ Opção inválida, tente novamente.[/red]")
                    time.sleep(2)
        else:
            while True:
                console.clear()
                console.print(Panel(f"[bold green]{nomeEscolhido}[/bold green]", expand=False))
                idExercicio = (len(exerciciosTreino) + 1) if len(exerciciosTreino) == 1 else len(exerciciosTreino)
                exerciciosTreino = editarInformacoesExercicio(nomeEscolhido, idExercicio, exerciciosTreino, True)
                break

def editarInformacoesExercicio(nomeTreino: str, idExercicio: int, exerciciosTreino: list, eNovo: bool = False) -> list:
    if eNovo:
        treino = {
            "idExercicio": 1,
            "nome": "",
            "nomeDivisao": "",
            "series": "",
            "repeticao": "",
            "peso": ""
        }
    else:
        treino = "pass"

    for key in treino.keys():
        if key == "idExercicio":
            treino[key] = idExercicio
        elif key == "nome": 
            bd = divisoesExerciciosPadroes()

            while True:
                console.clear()
                console.print(Panel(f"[bold green]Divisões[/bold green]", expand=False))
                if not eNovo:
                    console.print(f"[bold]Divisão atual: {treino['nomeDivisao']}[/bold]\n")

                dicioAuxDivisao = {}

                for i, divisao in enumerate(bd.keys(), start= 1):
                    console.print(f"[yellow]{i}[/yellow] - {divisao}")
                    dicioAuxDivisao[i] = divisao

                buscar = len(dicioAuxDivisao) + 1

                console.print("\n[grey19]--------------------------------[/grey19]")
                console.print(f"[yellow]{buscar}[/yellow] - Buscar divisão 🔎")
                
                try:
                    opcao = int(console.input("\n[bold cyan]Escolha uma opção: [/bold cyan]"))

                    if opcao == buscar:
                        voltou, item = buscarDivisaoJSON(dicioAuxDivisao)
                        if voltou:
                            continue
                        else:
                            treino["nome"] = dicioAuxExercicio[item]
                            break
                    elif 1 <= opcao < buscar:
                        treino["nomeDivisao"] = dicioAuxDivisao[opcao]
                        break
                    else: 
                        console.print("[red]⚠ Opção inválida, tente novamente.[/red]")
                        time.sleep(2)     
                except ValueError:
                    console.print("[red]⚠ Digite um número válido.[/red]")
                    time.sleep(2)

            while True:
                console.clear()
                console.print(Panel(f"[bold green]{treino["nomeDivisao"]}[/bold green]", expand=False))
                if not eNovo:
                    console.print(f"[bold]Exercício atual: {treino['nome']}[/bold]\n")

                dicioAuxExercicio = {}

                for i, exercicio in enumerate(bd[treino["nomeDivisao"]], start= 1):
                    console.print(f"[yellow]{i}[/yellow] - {exercicio}")
                    dicioAuxExercicio[i] = exercicio

                buscarEx = len(dicioAuxExercicio) + 1

                console.print("\n[grey19]--------------------------------[/grey19]")
                console.print(f"[yellow]{buscarEx}[/yellow] - Buscar exercício 🔎")
                
                try:
                    opcaoEx = int(console.input("\n[bold cyan]Escolha uma opção: [/bold cyan]"))

                    if opcaoEx == buscarEx:
                        voltou, item = buscarExercicioJSON(dicioAuxExercicio, treino["nomeDivisao"])
                        if voltou:
                            continue
                        else:
                            treino["nome"] = dicioAuxExercicio[item]
                            break
                    elif 1 <= opcaoEx < buscarEx:
                        treino["nome"] = dicioAuxExercicio[opcaoEx]
                        break
                    else: 
                        console.print("[red]⚠ Opção inválida, tente novamente.[/red]")
                        time.sleep(2)     
                except ValueError:
                    console.print("[red]⚠ Digite um número válido.[/red]")
                    time.sleep(2)


        elif key == "series":
            while True:
                console.clear()
                console.print(Panel(f"[bold green]{nomeTreino}[/bold green]", expand=False))
                if not eNovo:
                    console.print(f"[bold]Repetição atual: {treino['series']}[/bold]\n")
                try:
                    opcaoSeries = int(console.input("\n[bold cyan]Digite a quantidade de séries: [/bold cyan]"))   
                    
                    treino["series"] = opcaoSeries
                    break
                except ValueError:
                    console.print("[red]⚠ Digite um número válido.[/red]")
                    time.sleep(2)

        elif key == "repeticao":
            while True:
                console.clear()
                console.print(Panel(f"[bold green]{nomeTreino}[/bold green]", expand=False))
                if not eNovo:
                    console.print(f"[bold]Repetição atual: {treino['repeticao']}[/bold]\n")
                try:
                    opcaoRept = int(console.input("\n[bold cyan]Digite a quantidade de repetições: [/bold cyan]"))   

                    treino["repeticao"] = opcaoRept
                    break
                except ValueError:
                    console.print("[red]⚠ Digite um número válido.[/red]")
                    time.sleep(2)

        elif key == "peso":
            while True:
                console.clear()
                console.print(Panel(f"[bold green]{nomeTreino}[/bold green]", expand=False))
                if not eNovo:
                    console.print(f"[bold]Repetição atual: {treino['peso']}[/bold]\n")
                try:
                    opcaoPeso = int(console.input("\n[bold cyan]Digite o peso (Kg): [/bold cyan]"))   
                    
                    treino["peso"] = opcaoPeso
                    break
                except ValueError:
                    console.print("[red]⚠ Digite um número válido.[/red]")
                    time.sleep(2)

    exerciciosTreino.append(treino)
    return exerciciosTreino
            

def buscarDivisaoJSON(dicioAuxDivisao: dict) -> bool | str:
    while True:
        busca = console.input("[bold cyan]Digite o nome da divisão: [/bold cyan]")
        loading(f"Procurando divisão: {busca}")
        time.sleep(2)
        while True:
            console.clear()
            console.print(Panel(f"[bold green]Divisões[/bold green]", expand= False))
            divisaoEscolhida = []   
            
            for key in dicioAuxDivisao.keys():
                nomeDivisao = dicioAuxDivisao[key]
                if busca.lower() in nomeDivisao.lower():
                    divisaoEscolhida.append(divisaoEscolhida) 
            
            if divisaoEscolhida:
                IDs = 0
                for i, divisao in enumerate(divisaoEscolhida):
                    console.print(f"[yellow]{i}[/yellow] - {divisao}")
                    IDs += 1
            else:
                console.print("[bold red]⚠ Nenhuma divisão encontrada com essa busca.[/bold red]\n")
                opcaoMax = 1

            console.print("\n[grey19]---------------------[/grey19]")
            console.print(f"[yellow]{opcaoMax}[/yellow] - Voltar 🔙")

            try:
                opcao = int(console.input("\n[bold cyan]Escolha uma opção: [/bold cyan]"))

                if opcao == opcaoMax:
                    return True
                elif 1 <= opcao <= IDs:
                    itemEscolhido = divisaoEscolhida[opcao - 1]
                    return False, itemEscolhido
                else: 
                    console.print("[red]⚠ Opção inválida, tente novamente.[/red]")
                    time.sleep(2)
            except ValueError:
                console.print("[red]⚠ Digite um número válido.[/red]")
                time.sleep(2)
    
def buscarExercicioJSON(dicioAuxExercicio: dict, divisao: str) -> bool | str:
    while True:
        busca = console.input("[bold cyan]Digite o nome do exercício: [/bold cyan]")
        loading(f"Procurando exercício: {busca}")
        time.sleep(2)
        while True:
            console.clear()
            console.print(Panel(f"[bold green]{divisao}[/bold green]", expand= False))
            exercicioEscolhido = []   
            
            for key in dicioAuxExercicio.keys():
                nomeExercicio = dicioAuxExercicio[key]
                if busca.lower() in nomeExercicio.lower():
                    exercicioEscolhido.append(exercicioEscolhido) 
            
            if exercicioEscolhido:
                IDs = 0
                for i, exercicio in enumerate(exercicioEscolhido):
                    console.print(f"[yellow]{i}[/yellow] - {exercicio}")
                    IDs += 1
            else:
                console.print("[bold red]⚠ Nenhum exercício encontrado com essa busca.[/bold red]\n")
                opcaoMax = 1

            console.print("\n[grey19]---------------------[/grey19]")
            console.print(f"[yellow]{opcaoMax}[/yellow] - Voltar 🔙")

            try:
                opcao = int(console.input("\n[bold cyan]Escolha uma opção: [/bold cyan]"))

                if opcao == opcaoMax:
                    return True
                elif 1 <= opcao <= IDs:
                    itemEscolhido = exercicioEscolhido[opcao - 1]
                    return False, itemEscolhido
                else: 
                    console.print("[red]⚠ Opção inválida, tente novamente.[/red]")
                    time.sleep(2)
            except ValueError:
                console.print("[red]⚠ Digite um número válido.[/red]")
                time.sleep(2)

def buscarExercicio(dia: str, usuario):
    while True:
        usuarioJson = treinoUsuarioAtualizado()
        bd = usuarioJson[usuario]
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
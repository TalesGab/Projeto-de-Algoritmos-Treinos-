import time
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from Menu import loading
from manipulacaoJSON import treinoUsuarioAtualizado, atualizarTreino, divisoesExerciciosPadroes
import pandas as pd

console = Console()

def listarExercicios(treino: dict, existeFiltro: list = None, eEscolha: int = None, mostrarIDs: bool = False) -> tuple[int, list[int]]:
    # Pandas
    df = pd.DataFrame(treino["exercicios"])
    df = df.sort_values("idExercicio").reset_index(drop=True)

    existeFiltro = existeFiltro if existeFiltro is not None else []
    existeFiltroLower = [nome.lower() for nome in existeFiltro]

    df_utilizado = df.copy()

    if existeFiltroLower:
        df_utilizado = df[df["nome"].str.lower().isin(existeFiltroLower)].copy()
    elif eEscolha is not None and isinstance(eEscolha, int):
        df_utilizado = df[df["idExercicio"] == eEscolha].copy()

    if df_utilizado.empty:
        console.print("[bold red]⚠ Nenhum exercício encontrado com essa busca.")
        return 0, []

    maiorID = 1 + int(df_utilizado["idExercicio"].max()) if not df.empty else 1

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

def adicionarExercicio(dia: str, nomeEscolhido: str, usuario: str):
    tabelaDias = {0: "DOMINGO",
                  1: "SEGUNDA-FEIRA",
                  2: "TERÇA-FEIRA",
                  3: "QUARTA-FEIRA",
                  4: "QUINTA-FEIRA",
                  5: "SEXTA-FEIRA",
                  6: "SÁBADO"}

    usuarioJson = treinoUsuarioAtualizado()
    treinoUsuario = usuarioJson[usuario]

    for i, valor in tabelaDias.items():
        if valor == dia:
            semana = treinoUsuario[i]
    treino = semana[dia]
    exerciciosTreino = treino["exercicios"]

    treino["nomeTreino"] = nomeEscolhido
    while True: 
        if len(exerciciosTreino) > 0:
            while True:
                console.clear()
                console.print(Panel(f"[bold green]{nomeEscolhido}[/bold green]", expand=False))
                escolha = console.input("\n[yellow]Deseja adicionar mais exercícios (s/n)? [yellow]").lower()
                if escolha == 's':
                    idExercicio = len(exerciciosTreino) + 1
                    exerciciosTreino = editarInformacoesExercicio(nomeEscolhido, idExercicio, exerciciosTreino, True)
                    continue
                elif escolha == 'n':
                    treino["exercicios"] = exerciciosTreino
                    atualizarTreino(treinoUsuario, usuario)
                    console.print("[bold green]Treino Salvo![/bold green]")
                    time.sleep(2)
                    return
                else: 
                    console.print("[red]⚠ Opção inválida, tente novamente.[/red]")
                    time.sleep(2)
        else:
            while True:
                console.clear()
                console.print(Panel(f"[bold green]{nomeEscolhido}[/bold green]", expand=False))
                idExercicio = 1
                exerciciosTreino = editarInformacoesExercicio(nomeEscolhido, idExercicio, exerciciosTreino, True)
                break

def edicaoDoExercicioSelecionado(idExercicio: int, dia: str, usuario: str, nomeExercicio: str) -> None:
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

                listarExercicios(treino, None, idExercicio)
                console.print("[grey19]--------------------------------[/grey19]")
                console.print(f"[yellow]1[/yellow] - Editar exercício ✏️")
                console.print(f"[bold red]2 - Excluir exercício[/bold red] ❌")
                console.print(f"[yellow]3[/yellow] - Voltar 🔙")

                while True: 
                    try:
                        opcao = int(console.input("\n[bold cyan]Escolha uma opção: [/bold cyan]"))
                    
                        if opcao == 1:
                            loading(f"Editando exercício {nomeExercicio}")
                            exerciciosTreino = editarInformacoesExercicio(nome, idExercicio, treino["exercicios"], False, True)

                            treino["exercicios"] = exerciciosTreino
                            atualizarTreino(bd, usuario)
                            console.print("[bold green]Exercício atualizado com sucesso![/bold green]")
                            time.sleep(2)
                            return
                        elif opcao == 2:
                            while True:    
                                resposta = console.input("[bold yellow]⚠ Tem certeza que deseja EXCLUIR o exercício (S/N)? [/bold yellow]").upper()
                                
                                if resposta == 'S':
                                    loading("Excluindo exercício")
                                    treino["exercicios"].pop(idExercicio - 1)
                                    
                                    atualizarTreino(bd, usuario)
                                    console.print("[bold green]Exercício excluído com sucesso![/bold green]")
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

def editarInformacoesExercicio(nomeTreino: str, idExercicio: int, exerciciosTreino: list, eNovo: bool = False, eEdicao: bool = False) -> list:
    
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
        for i in exerciciosTreino:
            for j, valor in i.items():
                if j == "idExercicio" and valor == idExercicio:
                    treino = i

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

                for k, divisao in enumerate(bd.keys(), start= 1):
                    console.print(f"[yellow]{k}[/yellow] - {divisao}")
                    dicioAuxDivisao[k] = divisao

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

                for l, exercicio in enumerate(bd[treino["nomeDivisao"]], start= 1):
                    console.print(f"[yellow]{l}[/yellow] - {exercicio}")
                    dicioAuxExercicio[l] = exercicio

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

    if not eEdicao:
        exerciciosTreino.append(treino)
    return exerciciosTreino
            
def ordenarExercicios(usuario: str, dia: str) -> None:
    usuarioJson = treinoUsuarioAtualizado()
    bd = usuarioJson[usuario]
    
    for dicionario in bd:
        if dicionario.get(dia):
            treino = dicionario[dia]
            break
    
    listaExercicios = treino["exercicios"].copy()
    treino["exercicios"].clear()

    for i, elemento in enumerate(listaExercicios, start=1):
        elemento["idExercicio"] = i
        treino["exercicios"].append(elemento)
    
    atualizarTreino(bd, usuario)
    return

ordenarExercicios("João Paulo", "SEXTA-FEIRA")
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

def buscarExercicio(dia: str, usuario: str) -> None:
    while True:
        usuarioJson = treinoUsuarioAtualizado()
        treinoUsuario = usuarioJson[usuario]

        tabelaDias = {0: "DOMINGO",
                  1: "SEGUNDA-FEIRA",
                  2: "TERÇA-FEIRA",
                  3: "QUARTA-FEIRA",
                  4: "QUINTA-FEIRA",
                  5: "SEXTA-FEIRA",
                  6: "SÁBADO"}

        for i, valor in tabelaDias.items():
            if valor == dia:
                semana = treinoUsuario[i]
        treino = semana[dia]

        busca = console.input("[bold cyan]Digite o nome do exercício: [/bold cyan]")
        loading(f"Procurando exercício: {busca}")
        time.sleep(2)
        while True:
            console.clear()
            console.print(Panel(f"[bold green]🏋️  {treino["nomeTreino"]}[/bold green]", expand= False))
            exerciciosEscolhidos = []   
            
            for exercicio in treino["exercicios"]:
                for chave in exercicio.keys():
                    if chave == "nome":
                        nomeExercicio = exercicio[chave]
                        idExercicio = exercicio["idExercicio"]
                        if busca.lower() in nomeExercicio.lower():
                            exerciciosEscolhidos.append(nomeExercicio)

            if exerciciosEscolhidos:
                opcaoMax, IDs = listarExercicios(treino, exerciciosEscolhidos, None, True)
            else:
                console.print("[bold red]⚠ Nenhum exercício encontrado com essa busca.[/bold red]\n")
                opcaoMax = 1

            console.print("\n[grey19]---------------------[/grey19]")
            console.print(f"[yellow]{opcaoMax}[/yellow] - Voltar 🔙")

            try:
                opcao = int(console.input("\n[bold cyan]Escolha uma opção: [/bold cyan]"))

                if opcao == opcaoMax:
                    return
                elif min(IDs) <= opcao <= max(IDs):
                    nomeExercicio = treino["exercicios"][opcao - 1]

                    loading(f"Acessando exercício {nomeExercicio["nome"]}")
                    edicaoDoExercicioSelecionado(opcao, dia, usuario, nomeExercicio["nome"])
                    return
                else: 
                    console.print("[red]⚠ Opção inválida, tente novamente.[/red]")
                    time.sleep(2)
            except ValueError:
                console.print("[red]⚠ Digite um número válido.[/red]")
                time.sleep(2)
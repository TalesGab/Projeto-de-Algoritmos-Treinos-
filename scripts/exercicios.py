import time
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from utils import loading
from manipulacaoJSON import treinoUsuarioAtualizado, atualizarTreino, divisoesExerciciosPadroes
import pandas as pd
from limpeza import clear_screen

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

    def formatarDetalhes(row):
        if row["nomeDivisao"].upper() == "CARDIO" and row["nome"].upper() != "POLICHINELO":
            # Para cardio, prioriza tempo, depois distância
            if "tempo" in row and pd.notna(row["tempo"]) and row["tempo"] != "":
                return f"⏱️  {row['tempo']} min"
            elif "distancia" in row and pd.notna(row["distancia"]) and row["distancia"] != "":
                return f"↔️  {row['distancia']} km"
            else:
                return "Cardio"
        else:
            # Para outros exercícios, mostra séries, repetições e peso
            detalhes = []
            if "series" in row and pd.notna(row["series"]) and row["series"] != "":
                detalhes.append(f"📊  {row['series']} séries")
            if "repeticao" in row and pd.notna(row["repeticao"]) and row["repeticao"] != "":
                detalhes.append(f"🔄  {row['repeticao']} reps")
            if "peso" in row and pd.notna(row["peso"]) and row["peso"] != "" and row["nome"].upper() != "POLICHINELO":
                detalhes.append(f"🏋️  {row['peso']} kg")
            return " | ".join(detalhes) if detalhes else ""
    
    df_utilizado["Detalhes"] = df_utilizado.apply(formatarDetalhes, axis=1)

    df_Arrumado = df_utilizado.rename(columns={
        "nome": "Exercício",
        "nomeDivisao": "Divisão",
    })
    
    colunas = ["Exercício", "Divisão", "Detalhes"]

    # Rich Table
    tabela = Table(show_header=True, header_style="bold")

    if mostrarIDs:
        tabela.add_column("ID", justify="center")

    for coluna in colunas:
        if coluna == "Detalhes":
            tabela.add_column("Detalhes", justify="center", style="cyan")
        else:
            tabela.add_column(coluna, justify="center")

    for indice, linha in df_Arrumado.iterrows():
        ID = int(linha["idExercicio"])
        linhasUtilizadas = [
            str(linha["Exercício"]),
            str(linha["Divisão"]),
            str(linha["Detalhes"])
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
                clear_screen()
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
                clear_screen()
                loading("Adicionando novo exercício")
                idExercicio = 1
                exerciciosTreino = editarInformacoesExercicio(nomeEscolhido, idExercicio, exerciciosTreino, True)
                break
            if len(exerciciosTreino) == 0:
                console.print("[bold red]É necessário adicionar um exercício ao treino![/bold red]")
                time.sleep(2)

def edicaoDoExercicioSelecionado(idExercicio: int, dia: str, usuario: str, nomeExercicio: str) -> None:
    while True:
        ordenarExercicios(usuario, dia)
        usuarioJson = treinoUsuarioAtualizado()
        bd = usuarioJson[usuario]
        clear_screen()
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
                                    if len(treino["exercicios"]) == 1:
                                        addExercicioObrigatorio = True

                                    loading("Excluindo exercício")
                                    treino["exercicios"].pop(idExercicio - 1)
                                    
                                    atualizarTreino(bd, usuario)
                                    console.print("[bold green]Exercício excluído com sucesso![/bold green]")
                                    time.sleep(2)

                                    if addExercicioObrigatorio:
                                        while True:
                                            console.print("[cyan]Atenção: Treino sem exercícios.[/cyan]")
                                            time.sleep(2)
                                            loading("Redirecionando para criação de novo exercício")
                                            exerciciosTreino = editarInformacoesExercicio(nome, 1, treino["exercicios"], True)
                                            if len(exerciciosTreino) != 0:
                                                break
                                            else:
                                                clear_screen()
                                                continue

                                        treino["exercicios"] = exerciciosTreino
                                        atualizarTreino(bd, usuario)
                                        console.print("[bold green]Treino Salvo![/bold green]")
                                        time.sleep(2)
                                        return
                                    else:
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


def verificarDivisoes(exerciciosTreino: list) -> list:
    divisoesEscolhidas = []

    pernas = []
    biceps = []
    triceps = []
    gluteos = []
    costas = []
    peito = []
    ombros = []
    abdomen = []
    cardio = []

    for i in exerciciosTreino:
        if i["nomeDivisao"] == "Pernas":
            pernas.append(i["nome"])
        if i["nomeDivisao"] == "Bíceps":
            biceps.append(i["nome"])
        if i["nomeDivisao"] == "Tríceps":
            triceps.append(i["nome"])
        if i["nomeDivisao"] == "Glúteos":
            gluteos.append(i["nome"])
        if i["nomeDivisao"] == "Peito":
            peito.append(i["nome"])
        if i["nomeDivisao"] == "Costas":
            costas.append(i["nome"])
        if i["nomeDivisao"] == "Ombros":
            ombros.append(i["nome"])
        if i["nomeDivisao"] == "Abdômen":
            abdomen.append(i["nome"])
        if i["nomeDivisao"] == "Cardio":
                cardio.append(i["nome"])
    
    if len(pernas) == 8:
        divisoesEscolhidas.append("Pernas")
    if len(biceps) == 5:
        divisoesEscolhidas.append("Bíceps")
    if len(triceps) == 5:
        divisoesEscolhidas.append("Tríceps")
    if len(gluteos) == 5:
        divisoesEscolhidas.append("Glúteos")
    if len(peito) == 6:
        divisoesEscolhidas.append("Peito")
    if len(costas) == 6:
        divisoesEscolhidas.append("Costas")
    if len(ombros) == 5:
        divisoesEscolhidas.append("Ombros")
    if len(abdomen) == 6:
        divisoesEscolhidas.append("Abdômen")
    if len(cardio) == 6:
        divisoesEscolhidas.append("Cardio")

    return divisoesEscolhidas

def verificarExercicios(exerciciosTreino: list) -> list:
    exercicios = []

    for i in exerciciosTreino:
        exercicios.append(i["nome"])

    return exercicios

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
        exerciciosExistentes = []
        for i in exerciciosTreino:
            for j, valor in i.items():
                if j == "idExercicio" and valor == idExercicio:
                    treino = i
                if j == "nome" and i["idExercicio"] != idExercicio:
                    exerciciosExistentes.append(valor)

    FoiProcessadoCardio = False

    for key in ["idExercicio", "nome", "nomeDivisao", "series", "repeticao", "peso"]:
        if key == "idExercicio":
            treino[key] = idExercicio
        elif key == "nome": 
            bd = divisoesExerciciosPadroes()
            escolhasPrimarias = True

            while escolhasPrimarias:
                while True:
                    clear_screen()
                    console.print(Panel(f"[bold green]Divisões[/bold green]", expand=False))
                    if not eNovo:
                        console.print(f"[bold]Divisão atual: {treino['nomeDivisao']}[/bold]\n")

                    dicioAuxDivisao = {}
                    contador = 0
                    divisoesEscolhidas = verificarDivisoes(exerciciosTreino)

                    for divisao in bd.keys():
                        if not divisao in divisoesEscolhidas:
                            contador += 1
                            console.print(f"[yellow]{contador}[/yellow] - {divisao}")
                            dicioAuxDivisao[contador] = divisao

                    buscar = len(dicioAuxDivisao) + 1

                    console.print("\n[grey19]--------------------------------[/grey19]")
                    console.print(f"[yellow]{buscar}[/yellow] - Buscar divisão 🔎")
                    console.print(f"[yellow]{buscar + 1}[/yellow] - Voltar 🔙")
                    
                    try:
                        opcao = int(console.input("\n[bold cyan]Escolha uma opção: [/bold cyan]"))

                        if opcao == buscar:
                            voltou, item = buscarDivisaoJSON(dicioAuxDivisao)
                            if voltou:
                                continue
                            else:
                                treino["nomeDivisao"] = ''.join(dicioAuxDivisao[num]  for num, nome in dicioAuxDivisao.items() if nome == item)
                                break
                        elif opcao == (buscar + 1):
                            return exerciciosTreino
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
                    clear_screen()
                    console.print(Panel(f"[bold green]{treino["nomeDivisao"]}[/bold green]", expand=False))
                    if not eNovo:
                        console.print(f"[bold]Exercício atual: {treino['nome']}[/bold]\n")

                    dicioAuxExercicio = {}
                    contador = 0
                    exerciciosEscolhidos = verificarExercicios(exerciciosTreino)

                    for exercicio in bd[treino["nomeDivisao"]]:
                        if not exercicio in exerciciosEscolhidos:
                            contador += 1
                            console.print(f"[yellow]{contador}[/yellow] - {exercicio}")
                            dicioAuxExercicio[contador] = exercicio

                    buscarEx = len(dicioAuxExercicio) + 1

                    console.print("\n[grey19]--------------------------------[/grey19]")
                    console.print(f"[yellow]{buscarEx}[/yellow] - Buscar exercício 🔎")
                    console.print(f"[yellow]{buscarEx + 1}[/yellow] - Voltar 🔙")
                    
                    try:
                        opcaoEx = int(console.input("\n[bold cyan]Escolha uma opção: [/bold cyan]"))

                        if opcaoEx == buscarEx:
                            voltou, item = buscarExercicioJSON(dicioAuxExercicio, treino["nomeDivisao"])
                            if voltou:
                                continue
                            else:
                                treino["nome"] = ''.join(dicioAuxExercicio[numEx]  for numEx, nomeEx in dicioAuxExercicio.items() if nomeEx == item)
                                escolhasPrimarias = False
                                break
                        elif opcaoEx == (buscarEx + 1):
                            break
                        elif 1 <= opcaoEx < buscarEx:
                            treino["nome"] = dicioAuxExercicio[opcaoEx]
                            escolhasPrimarias =  False
                            break
                        else: 
                            console.print("[red]⚠ Opção inválida, tente novamente.[/red]")
                            time.sleep(2)     
                    except ValueError:
                        console.print("[red]⚠ Digite um número válido.[/red]")
                        time.sleep(2)

        elif key in ["series", "repeticao", "peso"]:
            if treino["nomeDivisao"] == "Cardio" and treino["nome"] != "Polichinelo" and not FoiProcessadoCardio:
                
                FoiProcessadoCardio = True
                
                if "series" in treino:
                    treino.pop("series")
                if "repeticao" in treino:
                    treino.pop("repeticao")
                if "peso" in treino:
                    treino.pop("peso")

                if "tempo" in treino:
                    treino.pop("tempo")
                if "distancia" in treino:
                    treino.pop("distancia")

                if treino["nome"] in ["Escada", "Corda"]:
                    while True:
                        clear_screen()
                        console.print(Panel(f"[bold green]{nomeTreino}[/bold green]", expand=False))
                        try:
                            opcaoTempo = int(console.input("\n[bold cyan]Digite o tempo (min): [/bold cyan]"))   
                            
                            treino["tempo"] = opcaoTempo
                            break
                        except ValueError:
                            console.print("[red]⚠ Digite um número válido.[/red]")
                            time.sleep(2)
                else:
                    while True:
                        clear_screen()
                        console.print(Panel(f"[bold green]{nomeTreino}[/bold green]", expand=False))
                        console.print(f"[yellow]1[/yellow] - Tempo ⏱️")
                        console.print(f"[yellow]2[/yellow] - Distância ↔️")
                        try:
                            opcaoTempoOuDistancia = int(console.input("\n[bold cyan]Deseja definir um tempo ou uma distância? [/bold cyan]")) 

                            if opcaoTempoOuDistancia == 1:  
                                try:
                                    opcaoTempo = int(console.input("\n[bold cyan]Digite o tempo (min): [/bold cyan]"))   
                                    
                                    if "distancia" in treino:
                                        treino.pop("distancia")
                                    treino["tempo"] = opcaoTempo
                                    break
                                except ValueError:
                                    console.print("[red]⚠ Digite um número válido.[/red]")
                                    time.sleep(2)
                            elif opcaoTempoOuDistancia == 2:
                                try:
                                    opcaoDistancia = int(console.input("\n[bold cyan]Digite a distância (Km): [/bold cyan]"))   
                                    
                                    if "tempo" in treino:
                                        treino.pop("tempo")
                                    treino["distancia"] = opcaoDistancia
                                    break
                                except ValueError:
                                    console.print("[red]⚠ Digite um número válido.[/red]")
                                    time.sleep(2)
                            else:
                                console.print("[red]⚠ Opção inválida, tente novamente.[/red]")
                                time.sleep(2)
                        except ValueError:
                            console.print("[red]⚠ Digite um número válido.[/red]")
                            time.sleep(2)
                continue
            elif FoiProcessadoCardio:
                continue
            else:
                if treino.get("series") == None:
                    treino["series"] = ""
                if treino.get("repeticao") == None:
                    treino["repeticao"] = ""
                if treino.get("peso") == None:
                    treino["peso"] = ""
                
                if key == "series":
                    while True:
                        clear_screen()
                        console.print(Panel(f"[bold green]{nomeTreino}[/bold green]", expand=False))
                        if not eNovo and treino['series'] != None:
                            console.print(f"[bold]Séries atuais: {treino['series']}[/bold]\n")
                        try:
                            opcaoSeries = int(console.input("\n[bold cyan]Digite a quantidade de séries: [/bold cyan]"))   
                            
                            treino["series"] = opcaoSeries
                            break
                        except ValueError:
                            console.print("[red]⚠ Digite um número válido.[/red]")
                            time.sleep(2)

                elif key == "repeticao":
                    while True:
                        clear_screen()
                        console.print(Panel(f"[bold green]{nomeTreino}[/bold green]", expand=False))
                        if not eNovo and treino['repeticao'] != None:
                            console.print(f"[bold]Repetições atuais: {treino['repeticao']}[/bold]\n")
                        try:
                            opcaoRept = int(console.input("\n[bold cyan]Digite a quantidade de repetições: [/bold cyan]"))   

                            treino["repeticao"] = opcaoRept
                            break
                        except ValueError:
                            console.print("[red]⚠ Digite um número válido.[/red]")
                            time.sleep(2)

                elif key == "peso":
                    if treino["nome"] == "Polichinelo":
                        treino.pop("peso")
                    else:
                        while True:
                            clear_screen()
                            console.print(Panel(f"[bold green]{nomeTreino}[/bold green]", expand=False))
                            if not eNovo and treino['peso'] != None:
                                console.print(f"[bold]Peso atual: {treino['peso']}[/bold]\n")
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

    if treino["exercicios"] == []:
        return
    
    listaExercicios = treino["exercicios"].copy()
    treino["exercicios"].clear()

    for i, elemento in enumerate(listaExercicios, start=1):
        elemento["idExercicio"] = i
        treino["exercicios"].append(elemento)
    
    atualizarTreino(bd, usuario)
    return

def buscarDivisaoJSON(dicioAuxDivisao: dict) -> bool | str:
    while True:
        busca = console.input("[bold cyan]Digite o nome da divisão: [/bold cyan]")
        loading(f"Procurando divisão: {busca}")
        time.sleep(2)
        while True:
            clear_screen()
            console.print(Panel(f"[bold green]Divisões[/bold green]", expand= False))
            divisaoEscolhida = []   
            
            for key in dicioAuxDivisao.keys():
                nomeDivisao = dicioAuxDivisao[key][1]
                if busca.lower() in nomeDivisao.lower():
                    divisaoEscolhida.append(nomeDivisao) 
            
            if divisaoEscolhida:
                opcaoMax = 1
                for i, divisao in enumerate(divisaoEscolhida):
                    console.print(f"[yellow]{i + 1}[/yellow] - {divisao}")
                    opcaoMax += 1 
            else:
                console.print("[bold red]⚠ Nenhuma divisão encontrada com essa busca.[/bold red]\n")
                opcaoMax = 1

            console.print("\n[grey19]---------------------[/grey19]")
            console.print(f"[yellow]{opcaoMax}[/yellow] - Voltar 🔙")

            try:
                opcao = int(console.input("\n[bold cyan]Escolha uma opção: [/bold cyan]"))

                if opcao == opcaoMax:
                    return True, None
                elif 1 <= opcao <= opcaoMax:
                    itemEscolhido = divisaoEscolhida[opcao - 1][1]
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
            clear_screen()
            console.print(Panel(f"[bold green]{divisao}[/bold green]", expand= False))
            exercicioEscolhido = []   
            
            for key in dicioAuxExercicio.keys():
                nomeExercicio = dicioAuxExercicio[key]
                if busca.lower() in nomeExercicio.lower():
                    exercicioEscolhido.append(nomeExercicio) 
            
            if exercicioEscolhido:
                opcaoMax = 1
                for i, exercicio in enumerate(exercicioEscolhido):
                    console.print(f"[yellow]{i + 1}[/yellow] - {exercicio}")
                    opcaoMax += 1
            else:
                console.print("[bold red]⚠ Nenhum exercício encontrado com essa busca.[/bold red]\n")
                opcaoMax = 1

            console.print("\n[grey19]---------------------[/grey19]")
            console.print(f"[yellow]{opcaoMax}[/yellow] - Voltar 🔙")

            try:
                opcao = int(console.input("\n[bold cyan]Escolha uma opção: [/bold cyan]"))

                if opcao == opcaoMax:
                    return True, None
                elif 1 <= opcao <= opcaoMax:
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
            clear_screen()
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
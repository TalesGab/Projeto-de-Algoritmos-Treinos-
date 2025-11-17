import pandas as pd
import time
import datetime
import sys
import json
import os
import numpy as np
from criar_usuario import criar_usuario
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from utils import loading
from treinos import treinos
from limpeza import clear_screen

console = Console()

# =================================================================
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(PROJECT_ROOT, "..", "data")

USUARIO_FILE_PATH = os.path.join(DATA_DIR, "usuario.json")
EXERCICIOS_FILE_PATH = os.path.join(DATA_DIR, "exercicios.json")
EXERCICIOS_USER_FILE_PATH = os.path.join(DATA_DIR, "treinoUsuario.json")
DADOS = "data/treinoUsuario.json"

# ===== Carregamento de arquivos =====
try:
    with open(EXERCICIOS_FILE_PATH, "r", encoding="utf-8") as f:
        exercicios = json.load(f)
except FileNotFoundError:
    print(f"ERRO: Arquivo de exercícios não encontrado em: {EXERCICIOS_FILE_PATH}")
    exercicios = {}

# ===== Funções base =====

def carregar_usuarios():
    clear_screen()
    caminho = "data/usuario.json"

    if not os.path.exists(caminho):
        console.print("[bold red]⚠ Erro![/bold red]")
        time.sleep(2)
        return

    with open(caminho, "r", encoding="utf-8") as arq:
        usuarios = json.load(arq)

    if not usuarios:
        console.print("[bold red]⚠ Voltando![/bold red]")
        time.sleep(2)
        return

    console.print(Panel("[bold magenta]Escolha um usuário para entrar:[/bold magenta]", expand=False))
    for i, user in enumerate(usuarios, start=1):
        console.print(f"[yellow]{i}[/yellow] - {user['Nome']} [blue]({user['Idade']} anos)[/blue]")

    console.print("\n[cyan]0 - Voltar[/cyan]")

    while True:
        try:
            opc = int(console.input("[bold cyan]Digite o número do usuário: [/bold cyan]"))
            if opc == 0:
                return  # Volta para o menu anterior
            elif 1 <= opc <= len(usuarios):
                usuario = usuarios[opc - 1]
                break
            else:
                console.print("[red]⚠ Opção inválida![/red]")
        except ValueError:
            console.print("[red]⚠ Digite apenas números![/red]")

    # ===== LOGIN COM OPÇÃO DE VOLTAR =====
    while True:
        clear_screen()
        console.print(Panel(f"[bold magenta]Bem-vindo, {usuario['Nome']}![/bold magenta]\nDigite sua senha para continuar:", expand=False))
        console.print("[yellow]Digite 0 para voltar[/yellow]\n")

        senha_digitada = console.input("[bold cyan]Senha: [/bold cyan]").strip()
        if senha_digitada == "0":
            clear_screen()
            return  # 🔹 Volta para a escolha de usuário

        senha_salva = usuario.get("Senha", "")

        if senha_digitada == senha_salva:
            console.print("[bold green]✅ Acesso permitido![/bold green]")
            time.sleep(1)
            menu_usuario(usuario)
            return
        else:
            console.print("[red]❌ Senha incorreta! Tente novamente.[/red]")
            time.sleep(1.5)

# ===== Verificação de Erros =====

def verificarTodosTreinosVazios() -> None:
    """
    Verifica silenciosamente todos os usuários e corrige treinos com exercicios vazios
    """
    if not os.path.exists(EXERCICIOS_USER_FILE_PATH):
        return

    with open(EXERCICIOS_USER_FILE_PATH, "r", encoding="utf-8") as f:
        try:
            usuarioJson = json.load(f)
        except json.JSONDecodeError:
            return
    
    correcoes = 0

    for usuarioNome in usuarioJson.keys():
        lista_treinos = usuarioJson[usuarioNome]
    
        for treinoDict in lista_treinos:
            for dia, treinoInfo in treinoDict.items():
                exercicios = treinoInfo.get("exercicios", [])

                if isinstance(exercicios, list) and len(exercicios) == 0:
                    treinoInfo["nomeTreino"] = "OFF"
                    correcoes += 1

    if correcoes > 0:
        with open(EXERCICIOS_USER_FILE_PATH, 'w', encoding="UTF-8") as arquivo:
            json.dump(usuarioJson, arquivo, indent=4, ensure_ascii=False)

# ===== Menus =====

def menu_principal():
    while True:
        clear_screen()  # 🔹 limpa antes de mostrar o menu principal
        console.print(Panel("[bold green]🏋️  Sistema de Treino[/bold green]", expand=False))
        console.print("[yellow]1[/yellow] - Novo Usuário")
        console.print("[yellow]2[/yellow] - Carregar Usuário")
        console.print("[yellow]3[/yellow] - Sair")

        opcao = console.input("\n[bold cyan]Escolha uma opção: [/bold cyan]")

        if opcao == "1":
            clear_screen()
            loading("Criando novo usuário")
            criar_usuario()
            console.print("[green]✅ Novo usuário criado com sucesso![/green]")
            time.sleep(2)
        elif opcao == "2":
            clear_screen()
            carregar_usuario()
        elif opcao == "3":
            clear_screen()
            loading("Saindo do sistema")
            console.print("[red]👋 Até logo![/red]")
            break
        else:
            clear_screen()
            console.print("[red]⚠ Opção inválida, tente novamente.[/red]")
            time.sleep(2)


# ===== Acesso ao usuário =====

def carregar_usuario():
    while True:
        clear_screen()
        usuarios = carregar_usuarios()

        if not usuarios:
            console.print("[red]⚠Voltando.[/red]")
            time.sleep(2)
            return  # volta pro menu principal

        console.print("\n[bold blue]👥 Usuários existentes:[/bold blue]")
        for i, u in enumerate(usuarios, start=1):
            console.print(f"[yellow]{i}[/yellow] - {u['Nome']} ([bold blue]{u['Idade']} anos[/bold blue])")

        console.print("\n[yellow]0[/yellow] - Voltar")

        escolha = console.input("\n[bold cyan]Digite o número do usuário que deseja acessar: [/bold cyan]").strip()

        if escolha == "0":
            clear_screen()
            return  # 🔹 volta pro menu principal

        if not escolha.isdigit() or int(escolha) not in range(1, len(usuarios) + 1):
            clear_screen()
            console.print("[red]⚠ Opção inválida.[/red]")
            time.sleep(2)
            continue

        usuario = usuarios[int(escolha) - 1]
        clear_screen()
        console.print(f"\n[bold green]✅ Bem-vindo, {usuario['Nome']}![/bold green]")
        time.sleep(1)
        menu_usuario(usuario)
        break  # sai do loop depois de entrar em um usuário



# ===== Menu principal do usuário =====

def menu_usuario(usuario):
    while True:
        clear_screen()  # 🔹 limpa antes de mostrar menu do usuário
        console.print(Panel(f"[bold green]💪 Menu Principal - {usuario['Nome']}[/bold green]", expand=False))
        console.print("[yellow]1[/yellow] - Treinar")
        console.print("[yellow]2[/yellow] - Perfil")
        console.print("[yellow]3[/yellow] - Meus Treinos")
        console.print("[yellow]4[/yellow] - Sair para o menu inicial")

        opcao = console.input("\n[bold cyan]Escolha uma opção: [/bold cyan]")

        if opcao == "1":
            clear_screen()
            treinar(usuario)
        elif opcao == "2":
            clear_screen()
            mostrar_perfil(usuario)
        elif opcao == "3":
            clear_screen()
            treinos(usuario['Nome'])
        elif opcao == "4":
            clear_screen()
            console.print("[red]⬅ Voltando ao menu inicial...[/red]")
            time.sleep(1.5)
            break
        else:
            clear_screen()
            console.print("[red]⚠ Opção inválida.[/red]")
            time.sleep(2)


# ===== Opções internas =====
def data_hoje():
    hoje = datetime.date.today()
    nmr_dia = hoje.weekday()

    dias = ["Segunda-Feira", "Terça-Feira", "Quarta-Feira", "Quinta-Feira", "Sexta-Feira", "Sábado", "Domingo"]

    return dias[nmr_dia]

def treino_usuario(usuario):
    if os.path.exists(DADOS):
        with open(DADOS, "r", encoding="utf-8") as f:
            dados = json.load(f)
            return dados.get(usuario["Nome"], [])
    return []

def mostrar_detalhes_exercicio(ex):
    clear_screen()
    df = pd.DataFrame([{
        "Divisão": ex.get("nomeDivisao", "N/A"),
        "Séries": ex.get("series", "N/A"),
        "Repetições": ex.get("repeticao", "N/A"),
        "Peso (kg)": ex.get("peso", "N/A"),
    }])

    console.print(Panel(f"🏋️ [bold green]{ex['nome']}[/bold green]", expand=False))

    from rich.table import Table
    table = Table(show_header=True, header_style="bold cyan")
    for col in df.columns:
        table.add_column(col, justify="center")

    for _, row in df.iterrows():
        table.add_row(
            str(row["Divisão"]),
            str(row["Séries"]),
            str(row["Repetições"]),
            str(row["Peso (kg)"]),
        )

    console.print(table)
    console.input("\nPressione [ENTER] para voltar.")

def treinar(usuario):
    DADOS = os.path.join("data", "treinoUsuario.json")

    if not os.path.exists(DADOS):
        console.print("[bold red]⚠ Voltando![/bold red]")
        time.sleep(2)
        return

    with open(DADOS, "r", encoding="utf-8") as f:
        todos_treinos = json.load(f)

    nome_usuario = usuario["Nome"]

    if nome_usuario not in todos_treinos:
        console.print("[bold red]⚠  Voltando![/bold red]")
        time.sleep(2)
        return

    dia = data_hoje()
    treinos_usuario = todos_treinos[nome_usuario]

    treino_do_dia = None
    for bloco in treinos_usuario:
        for dia_json in bloco.keys():
            if dia_json.strip().lower() == dia.strip().lower():
                treino_do_dia = bloco[dia_json]
            break
        if treino_do_dia:
            break


    if not treino_do_dia:
        console.print(f"[yellow]⚠ Nenhum treino cadastrado para {dia}![/yellow]")
        time.sleep(2)
        return

    while True:
        clear_screen()
        console.print(Panel(f"[bold green]{dia}[/bold green]", expand=False))
        console.print(f"\n[bold cyan]Treino de hoje:[/bold cyan] [bold yellow]{treino_do_dia['nomeTreino']}[/bold yellow]\n")

        exercicios = treino_do_dia["exercicios"]

        for i, ex in enumerate(exercicios, start=1):
            console.print(f"[cyan]{i}[/cyan] - {ex['nome']}")

        escolha = console.input("\n[bold cyan]Escolha um exercício para ver detalhes[/bold cyan]([bold red]0[/bold red] para voltar): ").strip()

        if escolha == "0":
            break
        if not escolha.isdigit() or int(escolha) not in range(1, len(exercicios) + 1):
            console.print("[red]⚠ Escolha inválida![/red]")
            time.sleep(1.5)
            continue

        exercicio_escolhido = exercicios[int(escolha) - 1]
        mostrar_detalhes_exercicio(exercicio_escolhido)

#Perfil

def mostrar_perfil(usuario):
    clear_screen()
    console.print(Panel("[bold green]👤 Perfil do Usuário[/bold green]", expand=False))
    
    console.print(f"Nome: [bold]{usuario['Nome']}[/bold]")
    console.print(f"Idade: [bold]{usuario['Idade']}[/bold]")
    console.print(f"Sexo: [bold]{usuario.get('Sexo', 'Não informado')}[/bold]")
    if usuario.get("Responsável"):
        console.print(f"Responsável: [bold]{usuario['Responsável']}[/bold]")
    console.print("\n[yellow]1[/yellow] - Voltar")
    console.print("[red]2[/red] - Deletar perfil")

    opcao = console.input("\n[bold cyan]Escolha uma opção: [/bold cyan]").strip()

    if opcao == "1":
        return
    elif opcao == "2":
        confirmar = console.input("[red]Tem certeza que deseja deletar este perfil? (s/n): [/red]").lower()
        if confirmar == "s":
            deletar_usuario(usuario)
            console.print(f"[green]✅ Usuário {usuario['Nome']} deletado com sucesso![/green]")
            time.sleep(2)
            menu_principal()
            sys.exit()
        else:
            console.print("[yellow]Operação cancelada.[/yellow]")
            time.sleep(1.5)
    else:
        console.print("[red]⚠ Opção inválida![/red]")
        time.sleep(1.5)

def deletar_usuario(usuario):
    usuarios = carregar_usuarios()
    usuarios = [u for u in usuarios if u['Nome'] != usuario['Nome']]

    with open(USUARIO_FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(usuarios, f, indent=4, ensure_ascii=False)


# ===== Execução =====

if __name__ == "__main__":
    menu_principal()
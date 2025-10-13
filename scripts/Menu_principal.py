import time
import sys
import json
import os
from criar_usuario import criar_usuario
from treinos import treinos
from rich.console import Console
from rich.panel import Panel

console = Console()

# =================================================================
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(PROJECT_ROOT, "..", "data")

USUARIO_FILE_PATH = os.path.join(DATA_DIR, "usuario.json")
EXERCICIOS_FILE_PATH = os.path.join(DATA_DIR, "exercicios.json")

# Ajuste o carregamento do arquivo 'exercicios.json'
try:
    with open(EXERCICIOS_FILE_PATH, "r", encoding="utf-8") as f:
        exercicios = json.load(f)
except FileNotFoundError:
    print(f"ERRO: Arquivo de exercícios não encontrado em: {EXERCICIOS_FILE_PATH}")
    exercicios = {} 
    
# ===== Funções base =====

def loading(text="Carregando"):
    for i in range(3):
        console.print(f"[cyan]{text}{'.' * (i+1)}[/cyan]", end="\r")
        time.sleep(0.5)
    print()

def carregar_usuarios():
    if os.path.exists(USUARIO_FILE_PATH):
        with open(USUARIO_FILE_PATH, "r", encoding="utf-8") as f:
            try:
                usuarios = json.load(f)
                if isinstance(usuarios, dict):
                    usuarios = [usuarios]
                elif not isinstance(usuarios, list):
                    usuarios = []
                return usuarios
            except json.JSONDecodeError:
                return []
    return []



# ===== Menus =====

def menu_principal():
    while True:
        console.clear()
        console.print(Panel("[bold green]🏋️  Sistema de Treino[/bold green]", expand=False))
        console.print("[yellow]1[/yellow] - Novo Usuário")
        console.print("[yellow]2[/yellow] - Carregar Usuário")
        console.print("[yellow]3[/yellow] - Sair")

        opcao = console.input("\n[bold cyan]Escolha uma opção: [/bold cyan]")

        if opcao == "1":
            loading("Criando novo usuário")
            criar_usuario()
            console.print("[green]✅ Novo usuário criado com sucesso![/green]")
            time.sleep(2)
        elif opcao == "2":
            carregar_usuario()
        elif opcao == "3":
            loading("Saindo do sistema")
            console.print("[red]👋 Até logo![/red]")
            break
        else:
            console.print("[red]⚠ Opção inválida, tente novamente.[/red]")
            time.sleep(2)

# ===== Acesso ao usuário =====

def carregar_usuario():
    usuarios = carregar_usuarios()

    if not usuarios:
        console.print("[red]⚠ Nenhum usuário cadastrado ainda.[/red]")
        time.sleep(2)
        return

    console.print("\n[bold blue]👥 Usuários existentes:[/bold blue]")
    for i, u in enumerate(usuarios, start=1):
        console.print(f"[yellow]{i}[/yellow] - {u['Nome']} ({u['Idade']} anos)")

    escolha = console.input("\nDigite o número do usuário que deseja acessar: ").strip()
    if not escolha.isdigit() or int(escolha) not in range(1, len(usuarios)+1):
        console.print("[red]⚠ Opção inválida.[/red]")
        time.sleep(2)
        return

    usuario = usuarios[int(escolha) - 1]
    console.print(f"\n[bold green]✅ Bem-vindo, {usuario['Nome']}![/bold green]")
    time.sleep(1)
    menu_usuario(usuario)

# ===== Menu principal do usuário =====

def menu_usuario(usuario):
    while True:
        console.clear()
        console.print(Panel(f"[bold green]💪 Menu Principal - {usuario['Nome']}[/bold green]", expand=False))
        console.print("[yellow]1[/yellow] - Treinar")
        console.print("[yellow]2[/yellow] - Perfil")
        console.print("[yellow]3[/yellow] - Meus Treinos")
        console.print("[yellow]4[/yellow] - Sair para o menu inicial")

        opcao = console.input("\n[bold cyan]Escolha uma opção: [/bold cyan]")

        if opcao == "1":
            treinar(usuario)
        elif opcao == "2":
            mostrar_perfil(usuario)
        elif opcao == "3":
            treinos(usuario['Nome'])
        elif opcao == "4":
            console.print("[red]⬅ Voltando ao menu inicial...[/red]")
            time.sleep(1.5)
            break
        else:
            console.print("[red]⚠ Opção inválida.[/red]")
            time.sleep(2)

# ===== Opções internas =====

def treinar(usuario):
    console.print(Panel("[bold green]🏋️ Iniciando treino...[/bold green]"))
    time.sleep(2)
    console.print("[cyan]Função em desenvolvimento...[/cyan]")
    input("\nPressione Enter para voltar.")

def mostrar_perfil(usuario):
    console.clear()
    console.print(Panel("[bold green]👤 Perfil do Usuário[/bold green]", expand=False))
    console.print(f"Nome: [bold]{usuario['Nome']}[/bold]")
    console.print(f"Idade: [bold]{usuario['Idade']}[/bold]")
    console.print(f"Sexo: [bold]{usuario.get('Sexo', 'Não informado')}[/bold]")
    input("\nPressione Enter para voltar.")

# ===== Execução =====

if __name__ == "__main__":
    menu_principal()

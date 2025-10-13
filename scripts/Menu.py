import time
import sys
import json
import os
from criar_usuario import criar_usuario
from rich.console import Console
from rich.panel import Panel

usuariosJSON = "data/usuario.json"

console = Console()

def loading(text="Carregando"):
    for i in range(3):
        console.print(f"[cyan]{text}{'.' * (i+1)}[/cyan]", end="\r")
        time.sleep(0.6)
    print()

def carregar_usuarios():
    if os.path.exists(usuariosJSON):
        with open(usuariosJSON, "r", encoding="utf-8") as f:
            try:
                usuarios = json.load(f)
                if isinstance(usuarios, dict):  # caso antigo, transforma em lista
                    usuarios = [usuarios]
                elif not isinstance(usuarios, list):
                    usuarios = []
                return usuarios
            except json.JSONDecodeError:
                return []
    return []

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
            loading("Carregando usuário")
            usuarios = carregar_usuarios()

            if not usuarios:
                console.print("[red]⚠ Nenhum usuário cadastrado ainda.[/red]")
                time.sleep(2)
                continue

            while True:
                console.print("\n[bold blue]👥 Usuários existentes:[/bold blue]")
                for i, u in enumerate(usuarios, start=1):
                    console.print(f"[yellow]{i}[/yellow] - {u['Nome']} ({u['Idade']} anos)")
                    ultimo = i
                console.print(f"[yellow]{ultimo + 1}[/yellow] - Voltar 🔙")

                escolha = console.input("\nDigite o número do usuário que deseja acessar: ").strip()
                if escolha == f'{ultimo + 1}':
                    menu_principal()
                if not escolha.isdigit() or int(escolha) not in range(1, len(usuarios)+1):
                    console.print("[red]⚠ Opção inválida.[/red]")
                    time.sleep(2)
                    continue

                usuario = usuarios[int(escolha) - 1]
                console.print(f"\n[bold green]👤 Nome: {usuario['Nome']}[/bold green]")
                console.print(f"[bold green]🎂 Idade: {usuario['Idade']}[/bold green]")

                try:
                    entrar = console.input("\nDeseja entrar no perfil deste usuário? (s/n): ").strip().lower()
                    if entrar == "s":
                        console.print(f"\n[bold green]✅ Bem-vindo, {usuario['Nome']}![/bold green]")
                        time.sleep(2)
                        # menu_principal()
                    elif entrar == "n":
                        continue
                    else:
                        console.print("[red]⚠ Opção inválida.[/red]")
                        time.sleep(2)
                except ValueError:
                        console.print("\nVoltando ao menu principal...")
                        time.sleep(2)
        elif opcao == "3":
            loading("Saindo do sistema")
            console.print("[red]👋 Até logo![/red]")
            break

        else:
            console.print("[red]⚠ Opção inválida, tente novamente.[/red]")
            time.sleep(2)

if __name__ == "__main__":
    menu_principal()

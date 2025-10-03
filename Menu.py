import time
import sys
from rich.console import Console
from rich.panel import Panel

console = Console()

def loading(text="Carregando"):
    for i in range(3):
        console.print(f"[cyan]{text}{'.' * (i+1)}[/cyan]", end="\r")
        time.sleep(0.6)
    print()

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
            console.print("[green]✅ Novo usuário criado com sucesso![/green]")
            time.sleep(2)

        elif opcao == "2":
            loading("Carregando usuário")
            console.print("[blue]👤 Usuário carregado com sucesso![/blue]")
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

import json
import os
from rich.console import Console
from rich.panel import Panel

console = Console()

def criar_usuario():
    nome = input("Digite seu Nome e Sobrenome: ")
    idade = int(console.input("[bold cyan]Digite sua Idade:[/bold cyan] "))
    sexualidade = ""
    console.print("[yellow]1[/yellow] - Masculino")
    console.print("[yellow]2[/yellow] - Feminino")
    console.print("[yellow]3[/yellow] - Indefinido")
    opc_SX = int(input("Digite o Número da Opção Escolhida: "))
    if opc_SX == 1:
        sexualidade = "Masculino"
    elif opc_SX == 2:
        sexualidade = "Feminino"
    elif opc_SX == 3:
        sexualidade = "Indefinido"
    else:
        console.print("[bold red]⚠ Número inválido! Tente novamente.[/bold red]")

    peso = console.input("[bold cyan]Digite seu peso (em kg): [/bold cyan]").strip()

    obj = ""
    console.print(Panel("[bold magenta]Qual das opções abaixo você tem como objetivo principal:[/bold magenta]", expand=False))
    console.print("[yellow]1[/yellow] - Ganhar Massa Muscular (Hipertrofia)")
    console.print("[yellow]2[/yellow] - Perder Peso / Reduzir Gordura Corporal")
    console.print("[yellow]3[/yellow] - Melhorar Saúde e Bem-estar Geral")
    console.print("[yellow]4[/yellow] - Treinos para Performance Esportiva Específica")

    opc_obj = int(console.input("[bold cyan]Digite o Número da Opção Escolhida: [/bold cyan]"))
    if opc_obj == 1:
        obj = "Ganhar Massa Muscular(Hipertrofia)"
    elif opc_obj == 2:
        obj = "Perder Peso / Reduzir Gordura Corporal"
    elif opc_obj == 3:
        obj = "3. Melhorar Saúde e Bem-estar Geral"
    elif opc_obj == 4:
        obj = "Treinos para Performance Esportiva Específica"

    console.print(Panel("[bold magenta]Agora informe se possui alguma lesão que possa impedir alguma atividade:[/bold magenta]", expand=False))
    lesoes_comuns = [
        "Tendinite patelar (joelho de saltador)",
        "Condromalácia patelar",
        "Lombalgia (dor lombar)",
        "Hérnia de disco",
        "Tendinite do manguito rotador",
        "Bursite no ombro",
        "Entorse de tornozelo",
        "Epicondilite (cotovelo de tenista)",
        "Distensão muscular"
    ]

    lesoes_usuario = []
    for lesao in lesoes_comuns:
        resposta = console.input(f"[bold yellow]Você tem ou já teve {lesao}? (s/n): [/bold yellow]").strip().lower()
        if resposta == "s":
            lesoes_usuario.append(lesao)

    if not lesoes_usuario:
        lesoes_usuario.append("Nenhuma lesão relatada")

    novo_usuario = {
        "Nome": nome,
        "Idade": idade,
        "Sexualidade": sexualidade,
        "Peso": peso,
        "Objetivo": obj,
        "Lesões": lesoes_usuario
    }

    if os.path.exists("usuario.json"):
        with open("usuario.json", "r", encoding="utf-8") as arq:
            try:
                usuarios = json.load(arq)
                if isinstance(usuarios, dict): 
                    usuarios = [usuarios]
                elif not isinstance(usuarios, list): 
                    usuarios = []
            except json.JSONDecodeError:
                usuarios = []
    else:
        usuarios = []

    usuarios.append(novo_usuario)
    with open("usuario.json", "w", encoding="utf-8") as arq:
        json.dump(usuarios, arq, ensure_ascii=False, indent=4)

    console.print("[bold green]✅ Usuário adicionado com sucesso![/bold green]")
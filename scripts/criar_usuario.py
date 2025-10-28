import json
import time
import os
import re
from manipulacaoJSON import atualizarTreino
from rich.console import Console
from rich.panel import Panel
from limpeza import clear_screen

console = Console()

def criar_usuario():   
    clear_screen()

    while True:
        nome = console.input("[bold cyan]Digite seu Nome e Sobrenome: [/bold cyan]")

        if len(nome) < 3:
            console.print("[bold red]⚠ O nome deve conter pelo menos 3 caracteres! Tente Novamente!!![/bold red]")
            time.sleep(2)
            clear_screen()
        elif len(nome.split()) < 2:
            console.print("[bold red]⚠ O nome deve conter NOME e SOBRENOME! Tente Novamente!!![/bold red]")
            time.sleep(2)
            clear_screen()
        elif any(char.isdigit() for char in nome):
            console.print("[bold red]⚠ O nome NÃO deve conter números! Tente Novamente!!![/bold red]")
            time.sleep(2)
            clear_screen()
        elif not re.match(r'^[A-Za-zÀ-ÿ\s]+$', nome):
            console.print("[bold red]⚠ O nome NÃO deve conter caracteres especiais! Tente Novamente!!![/bold red]")
            time.sleep(2)
            clear_screen()
        else:
            nome = nome.title()
            break

    clear_screen()

    while True:
        try:
            idade = int(console.input("[bold cyan]Digite sua Idade: [/bold cyan] "))

            if idade < 18:
                console.print("[bold red]⚠ Desculpe, a idade permitida para se matricular é acima de 18 anos! Digite Novamente!!![/bold red]")
                time.sleep(2)  
                clear_screen() 
            elif idade > 150:
                console.print("[bold red]⚠ Idade Inválida! Digite uma idade realista!!![/bold red]")
                time.sleep(2)
                clear_screen()
            else:
                break
        except ValueError:
            console.print("[bold red]⚠ Digite apenas números!!![/bold red]")
            time.sleep(2) 
            clear_screen()

    clear_screen()

    while True:
        try:
            sexo = ""
            console.print("[yellow]1[/yellow] - Masculino")
            console.print("[yellow]2[/yellow] - Feminino")
            console.print("[yellow]3[/yellow] - Indefinido")
            opc_SX = int(console.input("[bold cyan]Digite o número da opção Escolhida a partir do seu sexo: [/bold cyan]"))
            if opc_SX == 1:
                sexo = "Masculino"
                break
            elif opc_SX == 2:
                sexo = "Feminino"
                break
            elif opc_SX == 3:
                sexo = "Indefinido"
                break
            else:
                console.print("[bold red]⚠ Número inválido ! Tente novamente.[/bold red]")
            time.sleep(2)
            clear_screen()
        except ValueError:
            console.print("[bold red]⚠ Dígito inválido! Tente novamente.[/bold red]")
            time.sleep(2)
            clear_screen()

    clear_screen()
    while True:
        
        try:
            peso_str = console.input("[bold cyan]Digite seu peso(em kg): [/bold cyan]").strip()
            peso = int(peso_str)

            if peso <= 0:
                console.print("[bold red]⚠ Peso Inválido! Informe um peso acima de 0!!![/bold red]")
                time.sleep(2)
                clear_screen()
            elif peso > 500:
                console.print("[bold red]⚠ Peso Muito Alto! Informe um valor realista!!![/bold red]")
                time.sleep(2)
                clear_screen()
            else:
                break
        except ValueError:
            console.print("[bold red]⚠ Digite Apenas Números!!![/bold red]")
            time.sleep(2)
            clear_screen()

    clear_screen()
    while True:
        try:
            obj = ""
            console.print(Panel("[bold magenta]Qual das opções abaixo você tem como objetivo principal:[/bold magenta]", expand=False))
            console.print("[yellow]1[/yellow] - Ganhar Massa Muscular (Hipertrofia)")
            console.print("[yellow]2[/yellow] - Perder Peso / Reduzir Gordura Corporal")
            console.print("[yellow]3[/yellow] - Melhorar Saúde e Bem-estar Geral")
            console.print("[yellow]4[/yellow] - Treinos para Performance Esportiva Específica")

            opc_obj = int(console.input("[bold cyan]Digite o Número da Opção Escolhida: [/bold cyan]"))
            if opc_obj == 1:
                obj = "Ganhar Massa Muscular(Hipertrofia)"
                break
            elif opc_obj == 2:
                obj = "Perder Peso / Reduzir Gordura Corporal"
                break
            elif opc_obj == 3:
                obj = "3. Melhorar Saúde e Bem-estar Geral"
                break
            elif opc_obj == 4:
                obj = "Treinos para Performance Esportiva Específica"
                break
            else:
                console.print("[bold red]⚠ Número Inválido! Tente Novamente!!![bold red]")
                time.sleep(2)
                clear_screen()
        except ValueError:
            console.print("[bold red]⚠ Dígito inválido! Tente novamente.[/bold red]")
            time.sleep(2)
            clear_screen()

    clear_screen()

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
        while True:
            resposta = console.input(f"[bold yellow]Você tem ou já teve {lesao}? (s/n): [/bold yellow]").strip().lower()
            if resposta == "s":
                lesoes_usuario.append(lesao)
                clear_screen()
                console.print(Panel("[bold magenta]Agora informe se possui alguma lesão que possa impedir alguma atividade:[/bold magenta]", expand=False))
                break
            elif resposta == "n":
                pass
                clear_screen()
                console.print(Panel("[bold magenta]Agora informe se possui alguma lesão que possa impedir alguma atividade:[/bold magenta]", expand=False))
                break
            else:
                console.print("[bold red]⚠ Dígito Inválido! Digite SOMENTE (s) ou (n)!!![/bold red]")
                time.sleep(2)
                clear_screen()
                console.print(Panel("[bold magenta]Agora informe se possui alguma lesão que possa impedir alguma atividade:[/bold magenta]", expand=False))

    if not lesoes_usuario:
        lesoes_usuario.append("Nenhuma lesão relatada")
    clear_screen()

    novo_usuario = {
        "Nome": nome,
        "Idade": idade,
        "Sexualidade": sexo,
        "Peso": peso,
        "Objetivo": obj,
        "Lesões": lesoes_usuario
    }

    treino_usuario = [
        {
            "DOMINGO": {
            "nomeTreino": "OFF",
            "exercicios": []
            }
        },
        {
            "SEGUNDA-FEIRA": {
            "nomeTreino": "OFF",
            "exercicios": []
            }
        },
        {
            "TER\u00c7A-FEIRA": {
            "nomeTreino": "OFF",
            "exercicios": []
            }
        },
        {
            "QUARTA-FEIRA": {
            "nomeTreino": "OFF",
            "exercicios": []
            }
        },
        {
            "QUINTA-FEIRA": {
            "nomeTreino": "OFF",
            "exercicios": []
            }
        },
        {
            "SEXTA-FEIRA": {
            "nomeTreino": "OFF",
            "exercicios": []
            }
        },
        {
            "S\u00c1BADO": {
            "nomeTreino": "OFF",
            "exercicios": []
            }
        }
    ]

    if os.path.exists("data/usuario.json"):
        with open("data/usuario.json", "r", encoding="utf-8") as arq:
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
    with open("data/usuario.json", "w", encoding="utf-8") as arq:
        json.dump(usuarios, arq, ensure_ascii=False, indent=4)

    atualizarTreino(treino_usuario, nome)

    console.print("[bold green]✅ Usuário adicionado com sucesso![/bold green]")
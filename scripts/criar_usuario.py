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
        if len(nome) < 3 or len(nome.split()) < 2 or any(char.isdigit() for char in nome) or not re.match(r'^[A-Za-zÀ-ÿ\s]+$', nome):
            console.print("[bold red]⚠ Nome inválido! Tente novamente.[/bold red]")
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
                console.print("[bold red]⚠ Idade mínima é 18 anos![/bold red]")
            elif idade > 150:
                console.print("[bold red]⚠ Idade inválida![/bold red]")
            else:
                break
        except ValueError:
            console.print("[bold red]⚠ Digite apenas números![/bold red]")
        time.sleep(2)
        clear_screen()

    clear_screen()

    while True:
        console.print("[yellow]1[/yellow] - Masculino")
        console.print("[yellow]2[/yellow] - Feminino")
        console.print("[yellow]3[/yellow] - Indefinido")
        try:
            opc = int(console.input("[bold cyan]Escolha o número do seu sexo: [/bold cyan]"))
            if opc == 1:
                sexo = "Masculino"
                break
            elif opc == 2:
                sexo = "Feminino"
                break
            elif opc == 3:
                sexo = "Indefinido"
                break
            else:
                raise ValueError
        except ValueError:
            console.print("[bold red]⚠ Opção inválida![/bold red]")
        time.sleep(2)
        clear_screen()

    clear_screen()

    while True:
        try:
            peso = int(console.input("[bold cyan]Digite seu peso (kg): [/bold cyan]").strip())
            if peso <= 0 or peso > 500:
                raise ValueError
            break
        except ValueError:
            console.print("[bold red]⚠ Peso inválido![/bold red]")
            time.sleep(2)
            clear_screen()

    clear_screen()

    objetivos = [
        "Ganhar Massa Muscular (Hipertrofia)",
        "Perder Peso / Reduzir Gordura Corporal",
        "Melhorar Saúde e Bem-estar Geral",
        "Treinos para Performance Esportiva Específica"
    ]
    while True:
        console.print(Panel("[bold magenta]Escolha seu objetivo:[/bold magenta]", expand=False))
        for i, obj_txt in enumerate(objetivos, 1):
            console.print(f"[yellow]{i}[/yellow] - {obj_txt}")
        try:
            opc = int(console.input("[bold cyan]Número da opção: [/bold cyan]"))
            obj = objetivos[opc - 1]
            break
        except (ValueError, IndexError):
            console.print("[bold red]⚠ Opção inválida![/bold red]")
            time.sleep(2)
            clear_screen()

    clear_screen()

    console.print(Panel("[bold magenta]Você possui alguma lesão?[/bold magenta]", expand=False))
    lesoes_comuns = [
        "Tendinite patelar", "Lombalgia", "Hérnia de disco", "Bursite no ombro",
        "Entorse de tornozelo", "Epicondilite", "Distensão muscular"
    ]
    lesoes_usuario = []
    for lesao in lesoes_comuns:
        resp = console.input(f"[yellow]{lesao}? (s/n): [/yellow]").strip().lower()
        if resp == "s":
            lesoes_usuario.append(lesao)
    if not lesoes_usuario:
        lesoes_usuario.append("Nenhuma lesão relatada")

    clear_screen()

    # Criar senha simples
    while True:
        senha = console.input("[bold cyan]Crie uma senha (mínimo 4 caracteres): [/bold cyan]").strip()
        if len(senha) < 4:
            console.print("[red]⚠ Senha muito curta![/red]")
            time.sleep(2)
            clear_screen()
            continue
        confirmar = console.input("[bold cyan]Confirme sua senha: [/bold cyan]").strip()
        if senha != confirmar:
            console.print("[red]⚠ As senhas não coincidem![/red]")
            time.sleep(2)
            clear_screen()
        else:
            break

    clear_screen()

    novo_usuario = {
        "Nome": nome,
        "Idade": idade,
        "Sexo": sexo,
        "Peso": peso,
        "Objetivo": obj,
        "Lesões": lesoes_usuario,
        "Senha": senha  # 👈 agora salva a senha simples
    }

    treino_usuario = [
        {"DOMINGO": {"nomeTreino": "OFF", "exercicios": []}},
        {"SEGUNDA-FEIRA": {"nomeTreino": "OFF", "exercicios": []}},
        {"TERÇA-FEIRA": {"nomeTreino": "OFF", "exercicios": []}},
        {"QUARTA-FEIRA": {"nomeTreino": "OFF", "exercicios": []}},
        {"QUINTA-FEIRA": {"nomeTreino": "OFF", "exercicios": []}},
        {"SEXTA-FEIRA": {"nomeTreino": "OFF", "exercicios": []}},
        {"SÁBADO": {"nomeTreino": "OFF", "exercicios": []}}
    ]

    if os.path.exists("data/usuario.json"):
        with open("data/usuario.json", "r", encoding="utf-8") as arq:
            try:
                usuarios = json.load(arq)
                if not isinstance(usuarios, list):
                    usuarios = []
            except json.JSONDecodeError:
                usuarios = []
    else:
        usuarios = []

    usuarios.append(novo_usuario)
    with open("data/usuario.json", "w", encoding="utf-8") as arq:
        json.dump(usuarios, arq, ensure_ascii=False, indent=4)

    atualizarTreino(treino_usuario, nome)
    console.print("[bold green]✅ Usuário criado com sucesso![/bold green]")
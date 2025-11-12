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
    etapas = ["nome", "idade", "sexo", "peso", "objetivo", "lesoes", "senha"]
    i = 0

    nome = ""
    idade = 0
    sexo = ""
    peso = 0
    obj = ""
    lesoes_usuario = []
    senha = ""

    objetivos = [
        "Ganhar Massa Muscular (Hipertrofia)",
        "Perder Peso / Reduzir Gordura Corporal",
        "Melhorar Saúde e Bem-estar Geral",
        "Treinos para Performance Esportiva Específica"
    ]

    while i < len(etapas):
        etapa = etapas[i]

        # --- Nome ---
        if etapa == "nome":
            nome = console.input("[bold cyan]Digite seu Nome e Sobrenome: [/bold cyan]").strip()
            if nome.lower() == "voltar":
                console.print("[red]⚠ Já está na primeira etapa![/red]")
                time.sleep(1)
                continue
            if len(nome) < 3 or len(nome.split()) < 2 or any(char.isdigit() for char in nome) or not re.match(r'^[A-Za-zÀ-ÿ\s]+$', nome):
                console.print("[bold red]⚠ Nome inválido! Tente novamente.[/bold red]")
                time.sleep(2)
                clear_screen()
            else:
                nome = nome.title()
                i += 1
                clear_screen()

        # --- Idade ---
        elif etapa == "idade":
            idade_input = console.input("[bold cyan]Digite sua Idade ('voltar' para corrigir): [/bold cyan]").strip()
            if idade_input.lower() == "voltar":
                i -= 1
                clear_screen()
                continue
            try:
                idade = int(idade_input)
                if idade < 18:
                    console.print("[bold red]⚠ Idade mínima é 18 anos![/bold red]")
                elif idade > 150:
                    console.print("[bold red]⚠ Idade inválida![/bold red]")
                else:
                    i += 1
                    clear_screen()
            except ValueError:
                console.print("[bold red]⚠ Digite apenas números![/bold red]")
            time.sleep(1)

        # --- Sexo ---
        elif etapa == "sexo":
            console.print("[yellow]1[/yellow] - Masculino")
            console.print("[yellow]2[/yellow] - Feminino")
            console.print("[yellow]3[/yellow] - Indefinido")
            opc = console.input("[bold cyan]Escolha o número do seu sexo ('voltar' para corrigir): [/bold cyan]").strip()
            if opc.lower() == "voltar":
                i -= 1
                clear_screen()
                continue
            try:
                opc = int(opc)
                if opc == 1:
                    sexo = "Masculino"
                elif opc == 2:
                    sexo = "Feminino"
                elif opc == 3:
                    sexo = "Indefinido"
                else:
                    raise ValueError
                i += 1
                clear_screen()
            except ValueError:
                console.print("[bold red]⚠ Opção inválida![/bold red]")
                time.sleep(1)
                clear_screen()

        # --- Peso ---
        elif etapa == "peso":
            peso_input = console.input("[bold cyan]Digite seu peso (kg) ('voltar' para corrigir): [/bold cyan]").strip()
            if peso_input.lower() == "voltar":
                i -= 1
                clear_screen()
                continue
            try:
                peso = float(peso_input)
                if peso <= 0 or peso > 500:
                    raise ValueError
                i += 1
                clear_screen()
            except ValueError:
                console.print("[bold red]⚠ Peso inválido![/bold red]")
                time.sleep(1)
                clear_screen()

        # --- Objetivo ---
        elif etapa == "objetivo":
            console.print(Panel("[bold magenta]Escolha seu objetivo:[/bold magenta]", expand=False))
            for idx, o in enumerate(objetivos, 1):
                console.print(f"[yellow]{idx}[/yellow] - {o}")
            opc = console.input("[bold cyan]Número da opção ('voltar' para corrigir): [/bold cyan]").strip()
            if opc.lower() == "voltar":
                i -= 1
                clear_screen()
                continue
            try:
                obj = objetivos[int(opc) - 1]
                i += 1
                clear_screen()
            except (ValueError, IndexError):
                console.print("[bold red]⚠ Opção inválida![/bold red]")
                time.sleep(1)
                clear_screen()

        # --- Lesões ---
        elif etapa == "lesoes":
            console.print(Panel("[bold magenta]Você possui alguma lesão?[/bold magenta]\n[cyan]Digite 'voltar' para corrigir o objetivo.[/cyan]", expand=False))
            lesoes_comuns = [
                "Tendinite patelar", "Lombalgia", "Hérnia de disco", "Bursite no ombro",
                "Entorse de tornozelo", "Epicondilite", "Distensão muscular"
            ]
            lesoes_usuario = []
            for lesao in lesoes_comuns:
                resp = console.input(f"[yellow]{lesao}? (s/n): [/yellow]").strip().lower()
                if resp == "voltar":
                    i -= 1
                    clear_screen()
                    break
                if resp == "s":
                    lesoes_usuario.append(lesao)
            else:
                if not lesoes_usuario:
                    lesoes_usuario.append("Nenhuma lesão relatada")
                i += 1
                clear_screen()
                continue

        # --- Senha ---
        elif etapa == "senha":
            senha = console.input("[bold cyan]Crie uma senha (mínimo 4 caracteres, 'voltar' para corrigir): [/bold cyan]").strip()
            if senha.lower() == "voltar":
                i -= 1
                clear_screen()
                continue
            if len(senha) < 4:
                console.print("[red]⚠ Senha muito curta![/red]")
                time.sleep(1)
                clear_screen()
                continue

            confirmar = console.input("[bold cyan]Confirme sua senha: [/bold cyan]").strip()
            if confirmar != senha:
                console.print("[red]⚠ As senhas não coincidem![/red]")
                time.sleep(1)
                clear_screen()
            else:
                i += 1
                clear_screen()

    # --- Finalização ---
    novo_usuario = {
        "Nome": nome,
        "Idade": idade,
        "Sexo": sexo,
        "Peso": peso,
        "Objetivo": obj,
        "Lesões": lesoes_usuario,
        "Senha": senha
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
    time.sleep(2)

import json
import time
import os
import re
from manipulacaoJSON import atualizarTreino
from rich.console import Console
from rich.panel import Panel
from limpeza import clear_screen

console = Console()

# Função de carregamento limpa e centralizada
def carregando():
    clear_screen()
    console.print("\n[bold cyan]Carregando[/bold cyan]", end="", justify="center")
    for _ in range(3):
        time.sleep(0.5)
        console.print(".", end="", style="bold cyan", justify="center")
    time.sleep(0.4)
    clear_screen()

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
        clear_screen()

        # --- Nome ---
        if etapa == "nome":
            console.print(Panel("[bold magenta]Etapa 1 de 7[/bold magenta]\nDigite seu [cyan]Nome e Sobrenome[/cyan].\n[grey58](Digite 'voltar' para cancelar)[/grey58]", expand=False))
            nome = console.input("[bold cyan]→ [/bold cyan]").strip()
            if nome.lower() == "voltar":
                console.print("[red]⚠ Já está na primeira etapa![/red]")
                time.sleep(1)
                continue
            if len(nome) < 3 or len(nome.split()) < 2 or any(char.isdigit() for char in nome) or not re.match(r'^[A-Za-zÀ-ÿ\s]+$', nome):
                clear_screen()
                console.print("[bold red]⚠ Nome inválido! Tente novamente.[/bold red]")
                time.sleep(1.5)
            else:
                nome = nome.title()
                carregando()
                i += 1

        # --- Idade ---
        elif etapa == "idade":
            console.print(Panel("[bold magenta]Etapa 2 de 7[/bold magenta]\nDigite sua [cyan]Idade[/cyan].\n[grey58](Digite 'voltar' para voltar à etapa anterior)[/grey58]", expand=False))
            idade_input = console.input("[bold cyan]→ [/bold cyan]").strip()
            if idade_input.lower() == "voltar":
                i -= 1
                carregando()
                continue
            try:
                idade = int(idade_input)
                if idade < 18:
                    clear_screen()
                    console.print("[bold red]⚠ Idade mínima é 18 anos![/bold red]")
                    time.sleep(1.5)
                elif idade > 150:
                    clear_screen()
                    console.print("[bold red]⚠ Idade inválida![/bold red]")
                    time.sleep(1.5)
                else:
                    carregando()
                    i += 1
            except ValueError:
                clear_screen()
                console.print("[bold red]⚠ Digite apenas números![/bold red]")
                time.sleep(1.5)

        # --- Sexo ---
        elif etapa == "sexo":
            console.print(Panel("[bold magenta]Etapa 3 de 7[/bold magenta]\nEscolha seu [cyan]sexo[/cyan]:\n[grey58](Digite 'voltar' para voltar à etapa anterior)[/grey58]", expand=False))
            console.print("[yellow]1[/yellow] - Masculino")
            console.print("[yellow]2[/yellow] - Feminino")
            console.print("[yellow]3[/yellow] - Indefinido")
            opc = console.input("[bold cyan]→ [/bold cyan]").strip()
            if opc.lower() == "voltar":
                i -= 1
                carregando()
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
                carregando()
                i += 1
            except ValueError:
                clear_screen()
                console.print("[bold red]⚠ Opção inválida![/bold red]")
                time.sleep(1.5)

        # --- Peso ---
        elif etapa == "peso":
            console.print(Panel("[bold magenta]Etapa 4 de 7[/bold magenta]\nDigite seu [cyan]peso (kg)[/cyan].\n[grey58](Digite 'voltar' para voltar à etapa anterior)[/grey58]", expand=False))
            peso_input = console.input("[bold cyan]→ [/bold cyan]").strip()
            if peso_input.lower() == "voltar":
                i -= 1
                carregando()
                continue
            try:
                peso = float(peso_input)
                if peso <= 0 or peso > 500:
                    raise ValueError
                carregando()
                i += 1
            except ValueError:
                clear_screen()
                console.print("[bold red]⚠ Peso inválido![/bold red]")
                time.sleep(1.5)

        # --- Objetivo ---
        elif etapa == "objetivo":
            console.print(Panel("[bold magenta]Etapa 5 de 7[/bold magenta]\nEscolha seu [cyan]objetivo[/cyan]:\n[grey58](Digite 'voltar' para voltar à etapa anterior)[/grey58]", expand=False))
            for idx, o in enumerate(objetivos, 1):
                console.print(f"[yellow]{idx}[/yellow] - {o}")
            opc = console.input("[bold cyan]→ [/bold cyan]").strip()
            if opc.lower() == "voltar":
                i -= 1
                carregando()
                continue
            try:
                obj = objetivos[int(opc) - 1]
                carregando()
                i += 1
            except (ValueError, IndexError):
                clear_screen()
                console.print("[bold red]⚠ Opção inválida![/bold red]")
                time.sleep(1.5)

        # --- Lesões ---
        elif etapa == "lesoes":
            console.print(Panel("[bold magenta]Etapa 6 de 7[/bold magenta]\nVocê possui alguma [cyan]lesão[/cyan]?\nDigite 'voltar' para voltar ao objetivo.", expand=False))
            lesoes_comuns = [
                "Tendinite patelar (joelho de saltador)",
                "Lombalgia (dor lombar crônica)",
                "Hérnia de disco (coluna vertebral)",
                "Bursite (ombro)",
                "Entorse (tornozelo)",
                "Epicondilite (cotovelo de tenista)",
                "Distensão muscular (alongamento excessivo)"
            ]
            lesoes_usuario = []
            for lesao in lesoes_comuns:
                resp = console.input(f"[yellow]{lesao}[/yellow]? (s/n): ").strip().lower()
                if resp == "voltar":
                    i -= 1
                    carregando()
                    break
                if resp == "s":
                    lesao_limpa = re.sub(r"\s*\(.*?\)", "", lesao).strip()
                    lesoes_usuario.append(lesao_limpa)
            else:
                if not lesoes_usuario:
                    lesoes_usuario.append("Nenhuma lesão relatada")
                carregando()
                i += 1
                continue

        # --- Senha ---
        elif etapa == "senha":
            console.print(Panel("[bold magenta]Etapa 7 de 7[/bold magenta]\nCrie uma [cyan]senha[/cyan] para sua conta.\n[grey58](Digite 'voltar' para voltar à etapa anterior)[/grey58]", expand=False))
            senha = console.input("[bold cyan]→ [/bold cyan]").strip()
            if senha.lower() == "voltar":
                i -= 1
                carregando()
                continue
            if len(senha) < 4:
                clear_screen()
                console.print("[red]⚠ Senha muito curta![/red]")
                time.sleep(1.5)
                continue
            confirmar = console.input("[bold cyan]Confirme sua senha: [/bold cyan]").strip()
            if confirmar.lower() == "voltar":
                i -= 1
                carregando()
                continue
            if confirmar != senha:
                clear_screen()
                console.print("[red]⚠ As senhas não coincidem![/red]")
                time.sleep(1.5)
                continue
            carregando()
            i += 1

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

    caminho = "data/usuario.json"
    if os.path.exists(caminho):
        with open(caminho, "r", encoding="utf-8") as arq:
            try:
                usuarios = json.load(arq)
                if not isinstance(usuarios, list):
                    usuarios = []
            except json.JSONDecodeError:
                usuarios = []
    else:
        usuarios = []

    usuarios.append(novo_usuario)
    with open(caminho, "w", encoding="utf-8") as arq:
        json.dump(usuarios, arq, ensure_ascii=False, indent=4)

    atualizarTreino(treino_usuario, nome)
    carregando()
    console.print("[bold green]✅ Usuário criado com sucesso![/bold green]")
    time.sleep(2)

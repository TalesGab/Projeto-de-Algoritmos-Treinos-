import pandas as pd
import time
import datetime
import sys
import json
import os
import re
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

        # Se não existir nenhum usuário
        if not usuarios:
            console.print("[red]⚠ Nenhum usuário encontrado. Voltando.[/red]")
            time.sleep(2)
            return  

        console.print("\n[bold blue]👥 Usuários existentes:[/bold blue]")
        for i, u in enumerate(usuarios, start=1):
            console.print(f"[yellow]{i}[/yellow] - {u['Nome']} ([bold blue]{u['Idade']} anos[/bold blue])")

        console.print("\n[yellow]0[/yellow] - Voltar")

        escolha = console.input("\n[bold cyan]Digite o número do usuário que deseja acessar: [/bold cyan]").strip()

        # Voltar
        if escolha == "0":
            clear_screen()
            return  

        # Validação
        if not escolha.isdigit() or int(escolha) not in range(1, len(usuarios) + 1):
            clear_screen()
            console.print("[red]⚠ Opção inválida.[/red]")
            time.sleep(2)
            continue

        usuario = usuarios[int(escolha) - 1]

        # --- PEDIR SENHA AQUI ---
        clear_screen()
        console.print(Panel(
    # Mude [/yellow][/bold] para [/bold yellow]
    f"[bold yellow]🔐 Entre no usuário: [green]{usuario['Nome']}[/green][/bold yellow]", 
    expand=False
))
        senha_digitada = console.input("[cyan]Digite a senha (ou 'voltar'): [/cyan]").strip()

        if senha_digitada.lower() == "voltar":
            clear_screen()
            continue  # volta para lista de usuários

        if senha_digitada != usuario.get("Senha"):
            clear_screen()
            console.print("[bold red]❌ Senha incorreta![/bold red]")
            time.sleep(2)
            continue  # volta para lista de usuários

        # --- Senha correta ---
        clear_screen()
        console.print(f"\n✅ Bem-vindo, {usuario['Nome']}!", style="bold green", justify="center", markup=True)
        time.sleep(1)
        menu_usuario(usuario)
        return  # usuário logado → volta ao menu apenas depois que sair




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
# ===== Carregar usuários (para menu) =====
def carregar_usuarios():
    """Carrega usuários APENAS para escolher e logar."""
    clear_screen()
    caminho = "data/usuario.json"

    if not os.path.exists(caminho):
        console.print("[bold red]⚠ Erro! Arquivo usuario.json não encontrado.[/bold red]")
        time.sleep(2)
        return []

    with open(caminho, "r", encoding="utf-8") as arq:
        usuarios = json.load(arq)

    if not usuarios:
        console.print("[bold red]⚠ Nenhum usuário cadastrado.[/bold red]")
        time.sleep(2)
        return []

    return usuarios


# ===== Carregamento puro (sem menus) =====
def carregar_usuarios_perfil():
    """Carrega a lista de usuários sem exibir menus (uso interno)."""
    if not os.path.exists(USUARIO_FILE_PATH):
        return []

    with open(USUARIO_FILE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


# ===== Deletar usuário =====
def deletar_usuario(usuario):
    usuarios = _puros()

    # Remove o usuário da lista
    usuarios = [u for u in usuarios if u["Nome"] != usuario["Nome"]]

    with open(USUARIO_FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(usuarios, f, indent=4, ensure_ascii=False)


# ===== Menu do usuário =====
def menu_usuario(usuario):
    while True:
        clear_screen()
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
            resultado = mostrar_perfil(usuario)  # <<< RECEBE RESULTADO

            if resultado == "menu":
                return  # volta para o menu principal

        elif opcao == "3":
            clear_screen()
            treinos(usuario['Nome'])

        elif opcao == "4":
            clear_screen()
            console.print("[red]⬅ Voltando ao menu inicial...[/red]")
            time.sleep(1.5)
            return

        else:
            clear_screen()
            console.print("[red]⚠ Opção inválida.[/red]")
            time.sleep(2)


# ===== Perfil =====
def carregar_usuarios_puros():
    try:
        with open(USUARIO_FILE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def salvar_usuarios(usuarios):
    with open(USUARIO_FILE_PATH, "w", encoding="utf-8") as f:
        json.dump(usuarios, f, indent=4, ensure_ascii=False)


# ==========================
#     MOSTRAR PERFIL
# ==========================
def mostrar_perfil(usuario):
    while True:
        console.clear()
        console.print(Panel("[bold green]👤 PERFIL DO USUÁRIO[/bold green]", expand=False))

        table = Table(title="Informações do Usuário", show_header=False, box=None)
        table.add_row("Nome:", f"[bold]{usuario.get('Nome', '---')}[/bold]")
        table.add_row("Idade:", f"[bold]{usuario.get('Idade', '---')}[/bold]")
        table.add_row("Sexo:", f"[bold]{usuario.get('Sexo', '---')}[/bold]")
        table.add_row("Peso:", f"[bold]{usuario.get('Peso', '---')} kg[/bold]")
        table.add_row("Objetivo:", f"[bold]{usuario.get('Objetivo', '---')}[/bold]")

        console.print(table)

        # Lesões em tabela separada
        console.print("\n[bold yellow]Lesões:[/bold yellow]")
        if usuario.get("Lesões"):
            t2 = Table(show_header=True, header_style="bold cyan")
            t2.add_column("Nº")
            t2.add_column("Descrição")

            for i, lesao in enumerate(usuario["Lesões"], start=1):
                t2.add_row(str(i), lesao)

            console.print(t2)
        else:
            console.print("[dim]Nenhuma lesão registrada.[/dim]")

        console.print("\n[yellow]1[/yellow] - Editar perfil")
        console.print("[red]2[/red] - Deletar perfil")
        console.print("[cyan]3[/cyan] - Voltar")

        opc = console.input("\n[bold cyan]Escolha: [/bold cyan]").strip()

        if opc == "1":
            editar_perfil(usuario)
        elif opc == "2":
            deletar_usuario(usuario)
            return
        elif opc == "3":
            return
        else:
            console.print("[red]⚠ Opção inválida![/red]")
            time.sleep(1.2)


# ==========================
#     EDITAR PERFIL
# ==========================
def editar_perfil(usuario):
    while True:
        clear_screen()
        console.print(Panel(f"[bold blue]✏ EDITAR PERFIL – {usuario['Nome']}[/bold blue]", expand=False))

        console.print("""
[cyan]O que deseja editar?[/cyan]

[yellow]1[/yellow] - Nome
[yellow]2[/yellow] - Idade
[yellow]3[/yellow] - Sexo
[yellow]4[/yellow] - Peso
[yellow]5[/yellow] - Objetivo
[yellow]6[/yellow] - Lesões
[red]7[/red] - Voltar
""")

        opc = console.input("[bold cyan]→ [/bold cyan]").strip()

        # ======================================================
        #   EDITAR NOME
        # ======================================================
        if opc == "1":
            while True:
                clear_screen()
                console.print(Panel("[bold magenta]Editar Nome[/bold magenta]\nDigite o novo nome.", expand=False))
                novo_nome = console.input("[cyan]Nome: [/cyan]").strip()

                if novo_nome == "":
                    break

                if len(novo_nome) < 3 or len(novo_nome.split()) < 2:
                    console.print("[red]⚠ Digite nome e sobrenome![/red]")
                    time.sleep(1.3)
                    continue

                if any(n.isdigit() for n in novo_nome):
                    console.print("[red]⚠ Nome não pode conter números![/red]")
                    time.sleep(1.3)
                    continue

                if not re.match(r'^[A-Za-zÀ-ÿ\s]+$', novo_nome):
                    console.print("[red]⚠ Nome contém caracteres inválidos![/red]")
                    time.sleep(1.3)
                    continue

                usuario["Nome"] = novo_nome.title()
                break

        # ======================================================
        #   EDITAR IDADE
        # ======================================================
        elif opc == "2":
            while True:
                clear_screen()
                console.print(Panel(
                    "[bold magenta]Editar Idade[/bold magenta]\n"
                    "Digite sua [cyan]idade[/cyan].\n"
                    "[grey58](Deixe vazio para cancelar)[/grey58]",
                    expand=False
                ))

                idade_input = console.input("[bold cyan]→ [/bold cyan]").strip()

                # Cancelar edição
                if idade_input == "":
                    break

                try:
                    idade = int(idade_input)

                    # Idade mínima
                    if idade < 14:
                        clear_screen()
                        console.print("[bold red]⚠ Idade mínima é 14 anos![/bold red]")
                        time.sleep(1.5)
                        continue

                    # Idade máxima
                    if idade > 150:
                        clear_screen()
                        console.print("[bold red]⚠ Idade inválida![/bold red]")
                        time.sleep(1.5)
                        continue

                    # Menores de idade
                    if idade < 18:
                        console.print("[bold yellow]⚠ Menores de 18 anos só podem treinar acompanhados de responsável.[/bold yellow]")
                        responsavel = console.input("[cyan]Nome do responsável: [/cyan]").strip()
                        usuario["Responsável"] = responsavel

                    # Salvar idade
                    usuario["Idade"] = idade
                    clear_screen()
                    console.print("[bold green]✔ Idade atualizada com sucesso![/bold green]")
                    time.sleep(1.2)
                    break

                except ValueError:
                    clear_screen()
                    console.print("[bold red]⚠ Digite apenas números![/bold red]")
                    time.sleep(1.3)

        # ======================================================
        #   EDITAR SEXO
        # ======================================================
        elif opc == "3":
            while True:
                clear_screen()
                console.print(Panel("[bold magenta]Editar Sexo[/bold magenta]", expand=False))
                console.print("""
[yellow]1[/yellow] Masculino
[yellow]2[/yellow] Feminino
[yellow]3[/yellow] Indefinido
""")

                sx = console.input("[cyan]→ [/cyan]").strip()

                if sx == "":
                    break

                if sx == "1":
                    usuario["Sexo"] = "Masculino"
                elif sx == "2":
                    usuario["Sexo"] = "Feminino"
                elif sx == "3":
                    usuario["Sexo"] = "Indefinido"
                else:
                    console.print("[red]⚠ Opção inválida![/red]")
                    time.sleep(1.3)
                    continue
                break

        # ======================================================
        #   EDITAR PESO
        # ======================================================
        elif opc == "4":
            while True:
                clear_screen()
                console.print(Panel("[bold magenta]Editar Peso[/bold magenta]\nDigite o peso em kg.", expand=False))
                p = console.input("[cyan]Peso: [/cyan]").strip()

                if p == "":
                    break

                try:
                    p = float(p)
                    if p <= 0 or p > 500:
                        console.print("[red]⚠ Peso inválido![/red]")
                        time.sleep(1.2)
                        continue
                    usuario["Peso"] = p
                    break
                except:
                    console.print("[red]⚠ Digite apenas números![/red]")
                    time.sleep(1.2)

        # ======================================================
        #   EDITAR OBJETIVO
        # ======================================================
        elif opc == "5":
            objetivos = [
                "Ganhar Massa Muscular (Hipertrofia)",
                "Perder Peso / Reduzir Gordura Corporal",
                "Melhorar Saúde e Bem-estar Geral",
                "Treinos para Performance Esportiva Específica"
            ]

            while True:
                clear_screen()
                console.print(Panel("[bold magenta]Editar Objetivo[/bold magenta]", expand=False))

                for i, o in enumerate(objetivos, 1):
                    console.print(f"[yellow]{i}[/yellow] - {o}")

                op = console.input("[cyan]→ [/cyan]").strip()

                if op == "":
                    break

                try:
                    usuario["Objetivo"] = objetivos[int(op) - 1]
                    break
                except:
                    console.print("[red]⚠ Opção inválida![/red]")
                    time.sleep(1.2)

        # ======================================================
        #   EDITAR LESÕES
        # ======================================================
        elif opc == "6":
            clear_screen()
            console.print(Panel("[bold magenta]Editar Lesões[/bold magenta]", expand=False))
            console.print("[cyan]Digite cada lesão (ENTER para sair)[/cyan]")

            nova_lista = []
            while True:
                lesao = console.input("- ").strip()
                if lesao == "":
                    break
                nova_lista.append(lesao)

            if nova_lista:
                usuario["Lesões"] = nova_lista

        # ======================================================
        #   VOLTAR
        # ======================================================
        elif opc == "7":
            break

        else:
            console.print("[red]⚠ Opção inválida![/red]")
            time.sleep(1.2)

        # ======================================================
        #   SALVAR ALTERAÇÕES NO JSON
        # ======================================================
        caminho = "data/usuario.json"
        with open(caminho, "r", encoding="utf-8") as arq:
            usuarios = json.load(arq)

        # Atualiza apenas o usuário editado
        for i, u in enumerate(usuarios):
            if u["Nome"] == usuario["Nome"]:
                usuarios[i] = usuario

        with open(caminho, "w", encoding="utf-8") as arq:
            json.dump(usuarios, arq, ensure_ascii=False, indent=4)

        console.print("[green]✔ Perfil atualizado![/green]")
        time.sleep(1.5)

# ===== Execução =====

if __name__ == "__main__":
    menu_principal()
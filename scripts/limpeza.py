from rich.console import Console
import os

console = Console()

# ===== Função universal de limpeza =====
def clear_screen():
    """
    Limpa o terminal completamente (compatível com Windows, Linux e VS Code).
    """
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")
    try:
        console.clear()
    except Exception:
        pass
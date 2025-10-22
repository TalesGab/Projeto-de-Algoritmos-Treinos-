import time
import sys
import json
import os
from rich.console import Console

console = Console()

def loading(text="Carregando"):
    for i in range(3):
        console.print(f"[cyan]{text}{'.' * (i+1)}[/cyan]", end="\r")
        time.sleep(0.5)
    print()

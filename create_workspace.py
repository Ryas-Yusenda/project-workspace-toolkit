from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.tree import Tree

from var import ROOT_PATH

console = Console()

# Folder structure to create
FOLDERS = [
    "Projects/Web",
    "Projects/Mobile",
    "Projects/Desktop",
    "Projects/APIs",
    "Projects/Automation",
    "Projects/AI",
    "Projects/Libraries",
    "Projects/ReverseEngineering",
    "Archives",
    "Templates",
]

console.print(Panel.fit("[bold cyan]Workspace Structure[/bold cyan]", border_style="cyan"))

for folder in FOLDERS:
    (Path(ROOT_PATH) / folder).mkdir(parents=True, exist_ok=True)

root_tree = Tree(f"[bold]{ROOT_PATH}[/bold]")
for folder in FOLDERS:
    root_tree.add(folder)

console.print(root_tree)
console.print("[bold green]Folder structure created successfully.[/bold green]")

console.input("\n[dim]Press Enter to exit...[/dim]")

import os

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm
from rich.table import Table
from send2trash import send2trash

from var import EXCLUDED_PATHS, FOLDERS_TO_DELETE, ROOT_PATH

console = Console()

ROOT_PATH = os.path.join(ROOT_PATH, "Projects")
EXCLUDED_PATHS = {os.path.normpath(os.path.join(ROOT_PATH, path)).lower() for path in EXCLUDED_PATHS}


def is_excluded(project_path: str) -> bool:
    """
    Check whether project should be skipped.
    """
    return os.path.normpath(project_path).lower() in EXCLUDED_PATHS


def get_folder_size(folder_path: str) -> int:
    """
    Calculate folder size.
    """
    total_size = 0

    for root, _, files in os.walk(folder_path):
        for file in files:
            total_size += os.path.getsize(os.path.join(root, file))

    return total_size


def format_size(size_bytes: int) -> str:
    """
    Convert bytes to human-readable format.
    """
    size = float(size_bytes)

    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size < 1024:
            return f"{size:.2f} {unit}"

        size /= 1024

    return f"{size:.2f} PB"


def find_cleanup_targets():
    """
    Scan:
    Projects
      └── Category
          └── Project
              └── dependency folder

    Only checks direct project children.
    """

    targets = []
    skipped = []

    if not os.path.isdir(ROOT_PATH):
        return targets, skipped

    for category in os.listdir(ROOT_PATH):

        category_path = os.path.join(ROOT_PATH, category)

        if not os.path.isdir(category_path):
            continue

        for project in os.listdir(category_path):

            project_path = os.path.join(category_path, project)

            if not os.path.isdir(project_path):
                continue

            if is_excluded(project_path):
                skipped.append(project_path)
                continue

            for dependency in FOLDERS_TO_DELETE:

                dependency_path = os.path.join(project_path, dependency)

                if os.path.isdir(dependency_path):
                    targets.append(dependency_path)

    return targets, skipped


def show_target_table(targets: list[str], total_size: int) -> None:
    table = Table(title="Folders to move", box=box.ROUNDED, header_style="bold cyan")
    table.add_column("Path", style="magenta")
    table.add_column("Size", justify="right", style="green")

    for folder in targets:
        size = get_folder_size(folder)
        table.add_row(folder, format_size(size))

    console.print(table)
    console.print()
    console.print(f"[bold]Folders found:[/] {len(targets)}")
    console.print(f"[bold]Space to free:[/] {format_size(total_size)}")


def main():
    console.print(Panel.fit("[bold cyan]PROJECT DEPENDENCY CLEANER[/bold cyan]", border_style="cyan"))
    console.print(f"[bold]Root:[/] {ROOT_PATH}")
    console.print()

    targets, skipped = find_cleanup_targets()

    if not targets:
        console.print("[yellow]No dependency folders found.[/yellow]")
        if skipped:
            console.print(f"[dim]Skipped {len(skipped)} protected project(s).[/dim]")
        return

    total_size = sum(get_folder_size(folder) for folder in targets)
    show_target_table(targets, total_size)

    if not Confirm.ask("\nMove these folders to the Recycle Bin?", default=False):
        console.print("[yellow]Operation cancelled.[/yellow]")
        return

    moved_size = 0

    console.print("\n[bold green]Moving folders...[/bold green]")

    for folder in targets:
        try:
            size = get_folder_size(folder)
            send2trash(folder)
            moved_size += size
            console.print(f"[green]✓[/green] [bold]{folder}[/bold]")
        except OSError as exc:
            console.print(f"[red]✗[/red] {folder}")
            console.print(f"[red]{exc}[/red]")

    console.print()
    console.print(
        Panel.fit(
            f"[bold green]CLEANUP COMPLETED[/bold green]\nMoved to Recycle Bin: {format_size(moved_size)}",
            border_style="green",
        )
    )


if __name__ == "__main__":
    main()
    console.input("\n[dim]Press Enter to exit...[/dim]")

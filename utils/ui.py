from rich import print
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.progress import Progress, SpinnerColumn, TextColumn
import time

console = Console()

def print_title(title):
    console.print(Panel.fit(f"[bold cyan]{title}[/bold cyan]", border_style="bright_blue"))

def print_subtitle(text):
    console.print(f"\n[bold bright_magenta]{text}[/bold bright_magenta]")

def print_success(message):
    console.print(f"[green]✅ {message}[/green]")

def print_error(message):
    console.print(f"[red]❌ {message}[/red]")

def print_warning(message):
    console.print(f"[yellow]⚠️ {message}[/yellow]")

def ask(prompt_text):
    return Prompt.ask(f"[bold bright_cyan]{prompt_text}[/bold bright_cyan]")

def pause():
    console.print("\n[bold dim]🔸 Press Enter to return to menu...[/bold dim]")
    input() 

def loading(message="Processing..."):
    with Progress(SpinnerColumn(), TextColumn(f"[bold blue]{message}[/bold blue]"), transient=True) as progress:
        task = progress.add_task("loading", total=None)
        time.sleep(1.5)

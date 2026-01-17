import dotenv
import asyncio
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.markdown import Markdown
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from langchain_core.messages import HumanMessage
from src.graph import graph

dotenv.load_dotenv()
console = Console()

def display_welcome():
    console.print(Panel.fit(
        "[bold cyan]Marketing Agency Multi-Agent System[/bold cyan]\n"
        "[dim]Powered by LangGraph & OpenAI[/dim]",
        border_style="cyan"
    ))

def print_agent_output(agent_name: str, content: str):
    color_map = {
        "Supervisor": "magenta",
        "Senior_Researcher": "blue",
        "Content_Strategist": "green",
        "SEO_Optimizer": "yellow",
        "Visual_Designer": "red"
    }
    color = color_map.get(agent_name, "white")

    console.print(f"\n[bold {color}]--- {agent_name} ---[/bold {color}]")
    console.print(Markdown(content))

def main():
    display_welcome()

    thread_id = Prompt.ask("Enter a Thread ID to resume or press Enter for a new session", default="default_thread")
    config = {"configurable": {"thread_id": thread_id}}

    while True:
        console.print("\n")
        user_input = Prompt.ask("[bold]Enter your marketing request[/bold] (or 'quit' to exit)")

        if user_input.lower() in ['quit', 'exit']:
            console.print("[bold red]Goodbye![/bold red]")
            break

        inputs = {"messages": [HumanMessage(content=user_input)]}

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
            console=console
        ) as progress:
            task = progress.add_task("[cyan]Agents are working...", total=None)

            try:
                # Stream the graph execution
                for s in graph.stream(inputs, config=config):
                    if "__end__" not in s:
                        for key, value in s.items():
                            if key == "Supervisor":
                                next_step = value.get("next")
                                progress.console.print(f"[dim]Supervisor routed to: {next_step}[/dim]")
                            elif "messages" in value:
                                last_msg = value["messages"][-1]
                                print_agent_output(key, last_msg.content)
            except Exception as e:
                console.print(f"[bold red]An error occurred:[/bold red] {e}")

        console.print(Panel("[bold green]Task Complete![/bold green]", border_style="green"))

if __name__ == "__main__":
    main()

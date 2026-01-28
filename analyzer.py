from stats import fetch_repos, analyze_stats
from personality import get_personality
from rich import print

def main():
    username = input("Введите GitHub-ник: ").strip()
    repos = fetch_repos(username)

    if not repos:
        print("[red]Пользователь не найден или нет репозиториев.[/red]")
        return

    stats = analyze_stats(repos)
    personality = get_personality(stats)

    print("\n[bold cyan]Отчёт GitHub Personality Analyzer[/bold cyan]")
    print(f"👤 Пользователь: {username}")
    print(f"🧠 Тип разработчика: [bold]{personality['type']}[/bold]")
    print(f"🔥 Уровень активности: {stats['activity_score']}")
    print(f"💬 Описание: {personality['description']}")

if __name__ == "__main__":
    main()

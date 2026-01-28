import requests

def fetch_repos(username):
    url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    return response.json()

def analyze_stats(repos):
    languages = {}
    stars = 0

    for repo in repos:
        lang = repo["language"]
        if lang:
            languages[lang] = languages.get(lang, 0) + 1
        stars += repo["stargazers_count"]

    main_lang = max(languages, key=languages.get) if languages else "Unknown"

    return {
        "repos": len(repos),
        "stars": stars,
        "main_language": main_lang,
        "activity_score": len(repos) * 10 + stars
    }

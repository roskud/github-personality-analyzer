from flask import Flask, render_template, request
from stats import fetch_repos, analyze_stats
from personality import get_personality, ai_description

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None

    if request.method == "POST":
        username = request.form.get("username")
        use_ai = request.form.get("use_ai") == "on"

        repos = fetch_repos(username)
        if not repos:
            error = "Пользователь не найден или нет репозиториев"
        else:
            stats = analyze_stats(repos)
            personality = get_personality(stats)

            result = {
                "username": username,
                "type": personality["type"],
                "score": stats["activity_score"],
                "description": personality["description"],
                "ai": ai_description(stats) if use_ai else None
            }

    return render_template("index.html", result=result, error=error)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)

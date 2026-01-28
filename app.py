from flask import Flask, render_template, request
from stats import fetch_repos, analyze_stats
from personality import get_personality, ai_description

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None
    ai_status = None

    if request.method == "POST":
        username = request.form.get("username")
        use_ai = request.form.get("use_ai") == "on"

        repos = fetch_repos(username)
        if not repos:
            error = "Пользователь не найден или нет репозиториев"
        else:
            stats = analyze_stats(repos)
            personality = get_personality(stats)

            ai_text = None
            if use_ai:
                ai_text = ai_description(stats, username)
                ai_status = "ok" if "недоступен" not in ai_text else "fail"

            result = {
                "username": username,
                "type": personality["type"],
                "score": stats["activity_score"],
                "description": personality["description"],
                "ai": ai_text
            }

    return render_template(
        "index.html",
        result=result,
        error=error,
        ai_status=ai_status
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)

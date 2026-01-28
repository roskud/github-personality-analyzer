from flask import Flask, render_template, request
from stats import fetch_repos, analyze_stats
from personality import get_personality

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        username = request.form["username"]
        repos = fetch_repos(username)
        if repos:
            stats = analyze_stats(repos)
            personality = get_personality(stats)
            result = {
                "username": username,
                "type": personality["type"],
                "score": stats["activity_score"],
                "description": personality["description"]
            }

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

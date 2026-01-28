def get_personality(stats):
    lang = stats["main_language"]
    score = stats["activity_score"]

    if lang in ["Python", "Go", "Java"]:
        dev_type = "Backend Architect"
        desc = "Любит логику, API и чистую архитектуру. Засыпает с открытым терминалом."
    elif lang in ["JavaScript", "TypeScript"]:
        dev_type = "Frontend Magician"
        desc = "Превращает кофе в интерфейсы. CSS не любит, но пользуется."
    elif lang in ["Jupyter Notebook", "R"]:
        dev_type = "Data Alchemist"
        desc = "Видит закономерности там, где другие видят хаос."
    else:
        dev_type = "Fullstack Adventurer"
        desc = "Делает всё. Иногда ломает всё."

    if score > 300:
        desc += " 🚀 GitHub-машина."

    return {
        "type": dev_type,
        "description": desc
    }

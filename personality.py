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


# ---------- AI ЧАСТЬ (GROQ) ----------

from groq import Groq
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ai_description(stats):
    try:
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {
                    "role": "system",
                    "content": "Ты опытный тимлид и кратко, уверенно и с юмором описываешь стиль разработчиков."
                },
                {
                    "role": "user",
                    "content": (
                        f"GitHub разработчик.\n"
                        f"Основной язык: {stats['main_language']}\n"
                        f"Активность: {stats['activity_score']}\n\n"
                        f"Опиши стиль коротко и с лёгким юмором."
                    )
                }
            ],
            temperature=0.8,
            max_tokens=120
        )

        return completion.choices[0].message.content.strip()

    except Exception as e:
        return f"AI временно недоступен (Groq): {str(e)[:100]}"

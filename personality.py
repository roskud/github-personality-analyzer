import json
import os
from datetime import datetime
from groq import Groq

CACHE_FILE = "cache/ai_cache.json"

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


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


# ---------- AI + CACHE ----------

def load_cache():
    if not os.path.exists(CACHE_FILE):
        return {}
    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_cache(cache):
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)


def ai_description(stats, username):
    cache = load_cache()
    key = username.lower()

    # ✅ 1. Возвращаем из кэша
    if key in cache:
        return cache[key]["ai"]

    # ✅ 2. Иначе вызываем AI
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
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

        ai_text = completion.choices[0].message.content.strip()

        # 💾 сохраняем в кэш
        cache[key] = {
            "ai": ai_text,
            "ts": datetime.utcnow().isoformat()
        }
        save_cache(cache)

        return ai_text

    except Exception as e:
        return f"AI временно недоступен (Groq): {str(e)[:100]}"

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


# ---------- AI ЧАСТЬ ----------

from huggingface_hub import InferenceClient
import os

client = InferenceClient(
    model="HuggingFaceH4/zephyr-7b-beta",
    token=os.getenv("HF_TOKEN")
)

def ai_description(stats):
    try:
        messages = [
            {
                "role": "system",
                "content": "Ты опытный разработчик и кратко описываешь стиль других разработчиков."
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
        ]

        response = client.chat_completion(
            messages=messages,
            max_tokens=100,
            temperature=0.8
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"AI временно недоступен (HF): {str(e)[:80]}..."

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
import os
from huggingface_hub import InferenceClient

client = InferenceClient(
    model="bigscience/bloomz-560m",
    token=os.getenv("HF_TOKEN")
)

from huggingface_hub import InferenceClient
import os

client = InferenceClient(
    model="mistralai/Mistral-7B-Instruct-v0.2",
    token=os.getenv("HF_TOKEN")
)

def ai_description(stats):
    try:
        messages = [
            {"role": "system", "content": "Ты опытный тимлид и оцениваешь стиль разработчиков."},
            {"role": "user", "content": f"GitHub разработчик. Основной язык: {stats['main_language']}. Активность: {stats['activity_score']}. Опиши стиль коротко и с юмором."}
        ]
        response = client.chat_completion(
            messages=messages,
            max_tokens=80,
            temperature=0.8
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return "AI временно недоступен, но разработчик всё равно хорош 😎"

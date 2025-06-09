from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from gigachat import GigaChat

# Загрузка переменных окружения
load_dotenv()

app = Flask(__name__)
CORS(app)  # Разрешаем запросы от Vue.js

QUESTIONS = [
    {
        "id": 0,
        "text": "Какой школьный предмет вам нравится больше всего? Почему?",
        "hint": "Например: 'Математика, потому что люблю решать задачи'"
    },
    {
        "id": 1,
        "text": "Опишите ваш идеальный проект или задачу, которой бы хотели заниматься.",
        "hint": "Например: 'Создание мобильного приложения для помощи людям с инвалидностью'"
    },
    {
        "id": 2,
        "text": "Какие навыки вы хотели бы развить в университете?",
        "hint": "Например: 'Программирование, анализ данных, публичные выступления'"
    },
    {
        "id": 3,
        "text": "Где вы видите себя через 5 лет после выпуска?",
        "hint": "Например: 'Работа в IT-компании над искусственным интеллектом'"
    },
    {
        "id": 4,
        "text": "Какие экзамены ты сдал или собираешься сдавать?",
        "hint": "Например: 'Математика, химия, физика'"
    },
    {
        "id": 5,
        "text": "Какие профессии тебя не интересуют?",
        "hint": "Например: 'Профессии, связанные с животными'"
    }
]


@app.route("/api/questions", methods=["GET"])
def get_questions():
    return jsonify(QUESTIONS)


@app.route("/api/analyze", methods=["POST"])
def analyze_answers():
    try:
        answers = request.json.get("answers")

        if not answers or len(answers) != len(QUESTIONS):
            return jsonify({"error": "Неверное количество ответов"}), 400

        prompt = f"""
        Проанализируй ответы абитуриента и порекомендуй подходящие факультеты:
        1. Любимый предмет: {answers[0]}
        2. Идеальный проект: {answers[1]}
        3. Навыки для развития: {answers[2]}
        4. Карьерные цели: {answers[3]}
        5. Сданные экзамены: {answers[4]}
        6. Неинтересные профессии: {answers[5]}

        Дай развернутые рекомендации (3-5 факультетов) с объяснениями, почему они подходят.
        Учитывай ЕГЭ и исключи профессии, которые не интересны абитуриенту.
        """

        # Инициализация GigaChat с авторизацией
        giga = GigaChat(
            credentials=os.getenv("GIGACHAT_CREDENTIALS"),  # Ключ из .env
            verify_ssl_certs=False  # Для тестирования, в продакшене уберите
        )

        # Отправка запроса
        response = giga.chat(prompt)

        return jsonify({
            "recommendations": response.choices[0].message.content
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(port=5000, debug=True)
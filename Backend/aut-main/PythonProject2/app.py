from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from dotenv import load_dotenv
from gigachat import GigaChat
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
CORS(app, supports_credentials=True)  # Включаем CORS

# Конфигурация JWT
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(hours=1)

# Инициализация Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"  # Защита сессии

# Функция для проверки JWT токена
def jwt_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
            
        try:
            data = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
            current_user = User.get(data['user_id'])
        except:
            return jsonify({'error': 'Token is invalid'}), 401
            
        return f(current_user, *args, **kwargs)
    return decorated_function

# Загрузка переменных окружения для GigaChat
load_dotenv()

# Вопросы для анкеты
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

# Инициализация БД
def init_db():
    if not os.path.exists('users.db'):
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE "Users" (
            "Id"	INTEGER NOT NULL UNIQUE,
            "Name"	TEXT NOT NULL,
            "LastName"	TEXT NOT NULL,
            "Patronymic"	TEXT,
            "Email"	TEXT NOT NULL UNIQUE,
            "Password"	TEXT NOT NULL,
            "BirthDate"	TEXT NOT NULL,
            PRIMARY KEY("Id" AUTOINCREMENT)
        );
        ''')
        conn.commit()
        conn.close()

        # Дополнительные настройки для кук
app.config.update(
    SESSION_COOKIE_SAMESITE='Lax',  # или 'None' если нужно
    SESSION_COOKIE_SECURE=False,    # отключаем Secure для локальной разработки
)

# Модель пользователя
class User(UserMixin):
    def __init__(self, id, email, role='user'):
        self.id = id
        self.email = email
        self.role = role

    @staticmethod
    def get(user_id):
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('SELECT Id, Email FROM Users WHERE Id = ?', (user_id,))
        user = cursor.fetchone()
        conn.close()
        if user:
            return User(id=user[0], email=user[1])
        return None

    @staticmethod
    def find_by_email(email):
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('SELECT Id, Name, LastName, Patronymic, Email, Password FROM Users WHERE Email = ?', (email,))
        user = cursor.fetchone()
        conn.close()
        if user:
            return {
                'id': user[0],
                'name': user[1],
                'lastName': user[2],
                'patronymic': user[3],
                'email': user[4],
                'password': user[5]
            }
        return None

@login_manager.user_loader
@login_manager.user_loader
def load_user(user_id):
    user = User.get(user_id)
    if user:
        return user
    return None

# Роуты API для аутентификации
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    lastName = data.get('lastName')
    patronymic = data.get('patronymic')
    email = data.get('email')
    password = data.get('password')
    birthDate = data.get('birthDate')
    
    if not email or not password:
        return jsonify({'error': 'Email and password are required'}), 400

    hashed_password = generate_password_hash(password)
    
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO Users (Name, LastName, Patronymic, Email, Password, BirthDate) VALUES (?, ?, ?, ?, ?, ?)', 
                       (name, lastName, patronymic, email, hashed_password, birthDate))
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        
        # Создаем JWT токен
        token = jwt.encode({
            'user_id': user_id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }, app.config['JWT_SECRET_KEY'], algorithm='HS256')
        
        return jsonify({
            'token': token,
            'user': {
                'id': user_id,
                'email': email
            }
        }), 201
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({'error': 'Email already exists'}), 400

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    user_data = User.find_by_email(email)
    if not user_data or not check_password_hash(user_data['password'], password):
        return jsonify({'error': 'Неверные логин или пароль'}), 401
    
    # Создаем JWT токен
    token = jwt.encode({
        'user_id': user_data['id'],
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, app.config['JWT_SECRET_KEY'], algorithm='HS256')
    
    # Создаем пользователя для Flask-Login
    user = User(user_data['id'], user_data['email'])
    login_user(user)
    
    response = jsonify({
        'token': token,
        'user': {
            'id': user_data['id'],
            'email': user_data['email']
        }
    })
    
    # Устанавливаем куки для сессии
    response.set_cookie(
        'session_token',
        value=token,
        httponly=True,
        secure=True if os.environ.get('FLASK_ENV') == 'production' else False,
        samesite='Lax'
    )
    
    return response

@app.route('/api/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'})

@app.route('/api/me', methods=['GET'])
@jwt_required
def get_current_user(current_user):
    return jsonify({
        'id': current_user.id,
        'email': current_user.email
    })

# Роуты API для анкеты
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
        Проанализируй ответы абитуриента и порекомендуй подходящие профессии:
        1. Любимый предмет: {answers[0]}
        2. Идеальный проект: {answers[1]}
        3. Навыки для развития: {answers[2]}
        4. Карьерные цели: {answers[3]}
        5. Сданные экзамены: {answers[4]}
        6. Неинтересные профессии: {answers[5]}

        Дай развернутые рекомендации (3-5 профессий) с объяснениями, почему они подходят.
        Учитывай ЕГЭ и исключи профессии, которые не интересны абитуриенту.
        """

        # Инициализация GigaChat с авторизацией
        
        giga = GigaChat(credentials="ZjY5MWE1NGItM2MxNy00YzE3LWI1YmEtZmMxNzExNmVhZTlmOjAwYzU0ZjYzLTkyZTEtNDk3Yi1iY2FkLWVlY2E4MTliNmQ4MA==", 
                        verify_ssl_certs=False)
        response = giga.chat(prompt)

        return jsonify({
            "recommendations": response.choices[0].message.content
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=8000)
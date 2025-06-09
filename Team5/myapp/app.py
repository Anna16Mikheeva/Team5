from flask import Flask, request, jsonify, session, make_response, render_template, redirect, url_for
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Критически важные настройки CORS
CORS(app, 
     resources={
         r"/api/*": {
             "origins": "http://localhost:8000",
             "supports_credentials": True,
             "expose_headers": ["Content-Type", "X-CSRFToken"],
             "allow_headers": ["Content-Type", "Authorization"],
             "methods": ["GET", "POST", "PUT", "OPTIONS"]
         }
     },
     supports_credentials=True)

# Дополнительные настройки для кук
app.config.update(
    SESSION_COOKIE_SAMESITE='Lax',  # или 'None' если нужно
    SESSION_COOKIE_SECURE=False,    # отключаем Secure для локальной разработки
)

# Конфигурация подключения к PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:16022001@localhost:5432/Team5'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_SECURE'] = True  # Для HTTPS

db = SQLAlchemy(app)

class Person(db.Model):
    __tablename__ = 'Person'
    Id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(100))
    Email = db.Column(db.String(100), unique=True)
    Password = db.Column(db.String(100))

# Маршрут для отображения welcome страницы
@app.route('/welcome')  # Изменили на '/welcome'
def welcome():
    print("Текущая сессия:", session) 
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('index'))
    user = Person.query.filter_by(Id=user_id).first()
    return render_template('welcome.html', name=user.Name)  # Убедитесь, что файл существует

# Предположим, что у вас есть index.html или другая стартовая страница
@app.route('/')
def index():
    return render_template('index.html')

# API: регистрация
@app.route('/api/register', methods=['POST'])
def api_register():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not all([name, email, password]):
        return jsonify({'error': 'Заполните все поля'}), 400

    existing_user = Person.query.filter_by(Email=email).first()
    if existing_user:
        return jsonify({'error': 'Этот email уже зарегистрирован'}), 400

    new_user = Person(Name=name, Email=email, Password=password)
    db.session.add(new_user)
    db.session.commit()

    # После регистрации сохраняем сессию и редиректим на страницу welcom.html
    session['user_id'] = new_user.Id
    return jsonify({'message': 'Пользователь зарегистрирован', 'user_id': new_user.Id})

# API: вход
@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = Person.query.filter_by(Email=email).first()
    if user and user.Password == password:
        session['user_id'] = user.Id
        # Возвращаем JSON с флагом для редиректа
        return jsonify({
            'message': 'Успешный вход',
            'redirect': '/welcome',  # Добавляем URL для редиректа
            'name': user.Name
        })
    else:
        return jsonify({'error': 'Неверный логин или пароль'}), 401

# API: выход
@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"message": "Вы вышли из системы"}), 200


# API: проверка авторизации и получение приветствия (можно использовать для проверки статуса)
@app.route('/api/welcome', methods=['GET'])
def api_welcome():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Не авторизован'}), 401
    user = Person.query.filter_by(Id=user_id).first()
    if not user:
        return jsonify({'error': 'Пользователь не найден'}), 404
    
    # Можно возвращать сообщение или просто статус
    return jsonify({'message': f'Привет!'})

if __name__ == '__main__':
    app.run(debug=True)
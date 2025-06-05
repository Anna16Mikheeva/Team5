from flask import Flask, request, jsonify, session, make_response
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
    SESSION_COOKIE_SAMESITE='None',
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_DOMAIN='localhost'
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


@app.route('/api/login', methods=['OPTIONS'])
def handle_login_options():
    response = jsonify()
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    return response

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

    return jsonify({'message': 'Пользователь зарегистрирован', 'user_id': new_user.Id})

# API: вход
@app.route('/api/login', methods=['POST', 'OPTIONS'])
def api_login():
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:8000')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return response

    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = Person.query.filter_by(Email=email).first()
    if user and user.Password == password:
        session['user_id'] = user.Id
        response = jsonify({
            'message': 'Успешный вход',
            'user_id': user.Id,
            'name': user.Name
        })
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:8000')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response
    else:
        return jsonify({'error': 'Неверный логин или пароль'}), 401

# API: выход
@app.route('/api/logout', methods=['POST'])
def api_logout():
    session.pop('user_id', None)
    return jsonify({'message': 'Выход выполнен'})

# API: проверка авторизации и получение приветствия
@app.route('/api/welcome', methods=['GET'])
def api_welcome():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Не авторизован'}), 401
    user = Person.query.filter_by(Id=user_id).first()
    if not user:
        return jsonify({'error': 'Пользователь не найден'}), 404
    return jsonify({'message': f'Привет, {user.Name}!'})

if __name__ == '__main__':
    app.run(debug=True)
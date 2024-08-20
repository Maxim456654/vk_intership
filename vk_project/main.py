from flask import Flask, request, jsonify
import tarantool
import jwt
import datetime
from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)
app.config['SECRET_KEY'] = '3fd2f3ef880def0e39954cd160d749f0f70f7457ed1ec6520da5f2b7cf9164d0'

# Подключение к Tarantool
conn = tarantool.connect('tarantool1', 3301)

# Функция для создания JWT-токена
def create_token(username):
    token = jwt.encode({
        'user': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, app.config['SECRET_KEY'], algorithm='HS256')
    return token

# Функция для декодирования JWT-токена
def decode_token(token):
    try:
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return data['user']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

# Добавьте маршрут для корневого URL
@app.route('/')
def home():
    return "Welcome to the Flask API!"

# Маршрут для логина
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    if username:
        token = create_token(username)
        return jsonify({'token': token})
    return jsonify({'message': 'Missing username'}), 400

# Маршрут для записи данных в Tarantool
@app.route('/api/write', methods=['POST'])
def write():
    token = request.headers.get('Authorization')
    if token:
        token = token.replace('Bearer ', '')
        user = decode_token(token)
        if not user:
            return jsonify({'message': 'Unauthorized'}), 401

        data = request.json
        if not isinstance(data, dict):
            return jsonify({'message': 'Data should be a dictionary of key-value pairs'}), 400

        def insert_data(key, value):
            try:
                conn.space('kv_store').insert((key, value))
            except tarantool.DatabaseError as e:
                return str(e)
            return None

        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(insert_data, key, value): key for key, value in data.items()}
            errors = {key: future.result() for future, key in futures.items() if future.result()}

        if errors:
            return jsonify({'message': 'Some errors occurred', 'errors': errors}), 500

        return jsonify({'message': 'Data written successfully'})
    else:
        return jsonify({'message': 'Token is missing'}), 401

# Маршрут для чтения данных из Tarantool
@app.route('/api/read', methods=['POST'])
def read():
    token = request.headers.get('Authorization')
    if token:
        token = token.replace('Bearer ', '')
        user = decode_token(token)
        if not user:
            return jsonify({'message': 'Unauthorized'}), 401

        keys = request.json
        if not isinstance(keys, list):
            return jsonify({'message': 'Keys should be a list'}), 400

        def select_data(key):
            try:
                value = conn.space('kv_store').select(key)
                return key, value[0][1] if value else None
            except tarantool.DatabaseError as e:
                return key, str(e)

        results = {}
        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(select_data, key): key for key in keys}
            for future in futures:
                key, value = future.result()
                results[key] = value

        return jsonify(results)
    else:
        return jsonify({'message': 'Token is missing'}), 401

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


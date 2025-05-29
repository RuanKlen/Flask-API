#pip install pyjwt

import datetime
import jwt
from app.models import Jogador  # import do modelo
from werkzeug.security import check_password_hash
from functools import wraps
from flask import request, jsonify, Blueprint, current_app

# toda a parte de encapsulamento da API, vai ser de responsabilidade do
# Blueprint
auth_bp = Blueprint('auth', __name__)

# criar as rotas de autenticação
@auth_bp.route('/login', methods=['POST'])
def login():
    auth_data = request.get_json()
    username_or_email = auth_data.get('username')  # Pode ser email ou "admin"
    password = auth_data.get('password')

    # Autenticação do ADMIN (fixa)
    if username_or_email == 'admin' and password == 'password':
        token = jwt.encode({
            'user': 'admin',
            'role': 'admin',
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }, current_app.config["SECRET_KEY"], algorithm='HS256')
        return jsonify({'token': token}), 200

    # Autenticação do JOGADOR via banco
    jogador = Jogador.query.filter_by(email=username_or_email).first()
    if jogador and check_password_hash(jogador.senha, password):
        token = jwt.encode({
            'user': jogador.email,
            'role': 'jogador',
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }, current_app.config["SECRET_KEY"], algorithm='HS256')
        return jsonify({'token': token}), 200

    return jsonify({'message': 'Invalid username/email or password'}), 401

# criar marcação de rotas com funções
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-token')

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = data['user']
            current_role = data['role']
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, current_role, *args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    @token_required
    def decorated(current_user, current_role, *args, **kwargs):
        if current_role != 'admin':
            return jsonify({'message': 'Admin access required!'}), 403
        return f(current_user, current_role, *args, **kwargs)
    return decorated

from flask import jsonify, request
from app import db  # Certifique-se de que 'app' é o seu objeto Flask
from app.models import Jogador  # Importe o modelo Jogador
from app.routes import bp  # Certifique-se de que 'bp' é o seu Blueprint
from app.auth import admin_required, token_required  # Importe a função de autenticação
from werkzeug.security import generate_password_hash, check_password_hash

# --- CREATE (POST) ---
@bp.route('/jogadores', methods=['POST'])
def create_jogador():
    """Cria um novo jogador."""
    try:
        data = request.get_json() or {}

        # Validação dos dados de entrada
        if not all(key in data for key in ('nome', 'email', 'senha')):
            return jsonify({'error': 'Nome, email e senha são obrigatórios'}), 400  # Bad Request

        # Verifica se o email já existe
        if Jogador.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email já cadastrado'}), 400  # Bad Request

        # Cria o novo jogador
        novo_jogador = Jogador(
            nome=data['nome'],
            email=data['email'],
            senha=generate_password_hash(data['senha'])  # Aplica hash aqui
        )
  # Use a senha diretamente aqui (e faça o hash na criação)
        db.session.add(novo_jogador)
        db.session.commit()

        return jsonify(novo_jogador.to_dict()), 201  # Created
    except Exception as e:
        db.session.rollback()  # Reverte quaisquer alterações em caso de erro
        return jsonify({'error': str(e)}), 500  # Internal Server Error


# --- READ (GET) ---
@bp.route('/jogadores', methods=['GET'])
@admin_required  # Requer autenticação
def get_jogadores(current_user, current_role):
    """Recupera um jogador específico (por ID) ou todos os jogadores."""
    jogador_id = request.args.get('id')  # Use 'id' para buscar por ID

    try:
        if jogador_id:
            # Recupera um jogador por ID
            jogador = Jogador.query.get_or_404(jogador_id)  # Retorna 404 se não encontrar
            return jsonify(jogador.to_dict()), 200  # OK
        else:
            # Recupera todos os jogadores
            jogadores = Jogador.query.all()
            return jsonify([jogador.to_dict() for jogador in jogadores]), 200  # OK
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Internal Server Error


# --- UPDATE (PUT/PATCH) ---
@bp.route('/jogadores/<int:jogador_id>', methods=['PUT', 'PATCH'])
@admin_required  # Requer autenticação
def update_jogador(current_user, current_role, jogador_id):
    """Atualiza os dados de um jogador existente."""
    try:
        jogador = Jogador.query.get_or_404(jogador_id)  # Retorna 404 se não encontrar
        data = request.get_json() or {}

        # Atualiza os campos fornecidos no corpo da requisição
        for key, value in data.items():
            if key == 'nome':
                jogador.nome = value
            elif key == 'email':
                jogador.email = value
            elif key == 'senha':
                jogador.senha = value  # Lembre-se de fazer o hash da senha!
            elif key == 'pontuacao':
                jogador.pontuacao = value
            elif key == 'ativo':
                jogador.ativo = value

        db.session.commit()
        return jsonify(jogador.to_dict()), 200  # OK
    except Exception as e:
        db.session.rollback()  # Reverte quaisquer alterações em caso de erro
        return jsonify({'error': str(e)}), 500  # Internal Server Error


# --- DELETE (DELETE) ---
@bp.route('/jogadores/<int:jogador_id>', methods=['DELETE'])
@admin_required  # Requer autenticação
def delete_jogador(current_user, current_role, jogador_id):
    """Exclui um jogador."""
    try:
        jogador = Jogador.query.get_or_404(jogador_id)  # Retorna 404 se não encontrar
        db.session.delete(jogador)
        db.session.commit()
        return jsonify({'message': 'Jogador excluído com sucesso'}), 200  # OK
    except Exception as e:
        db.session.rollback()  # Reverte quaisquer alterações em caso de erro
        return jsonify({'error': str(e)}), 500  # Internal Server Error

# Obter jogador por ID
@bp.route('/jogadores/<int:id>', methods=['GET'])
@token_required
def obter_jogador(current_user, current_role, id):
    jogador = Jogador.query.get_or_404(id)
    return jsonify(jogador.to_dict()), 200
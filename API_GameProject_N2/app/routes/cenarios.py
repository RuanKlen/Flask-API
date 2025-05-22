from flask import request, jsonify
from app.routes import bp
from app.db import db
from app.models import Item, Cenario, Rota, Sessao, Desafio
from app.auth import token_required


# ------------------ CENARIOS ------------------
@bp.route('/cenarios', methods=['POST'])
@token_required
def criar_cenario(current_user):
    data = request.get_json()
    cenario = Cenario(nome=data['nome'], dificuldade=data.get('dificuldade'), descricao=data.get('descricao'))
    db.session.add(cenario)
    db.session.commit()
    return jsonify({'id': cenario.id}), 201

@bp.route('/cenarios', methods=['GET'])
@token_required
def listar_cenarios(current_user):
    cenarios = Cenario.query.all()
    return jsonify([{'id': c.id, 'nome': c.nome, 'dificuldade': c.dificuldade, 'descricao': c.descricao} for c in cenarios]), 200

@bp.route('/cenarios/<int:id>', methods=['PUT'])
@token_required
def atualizar_cenario(current_user, id):
    cenario = Cenario.query.get_or_404(id)
    data = request.get_json()

    if 'nome' in data:
        cenario.nome = data['nome']
    if 'dificuldade' in data:
        cenario.dificuldade = data['dificuldade']
    if 'descricao' in data:
        cenario.descricao = data['descricao']

    db.session.commit()
    return jsonify(cenario.to_dict()), 200  # Retorna o cenário atualizado


@bp.route('/cenarios/<int:id>', methods=['DELETE'])
@token_required
def deletar_cenario(current_user, id):
    cenario = Cenario.query.get_or_404(id)
    db.session.delete(cenario)
    db.session.commit()
    return jsonify({'message': 'Cenário deletado'}), 200

@bp.route('/cenarios/<int:id>', methods=['GET'])
@token_required
def obter_cenario(current_user, id):
    cenario = Cenario.query.get_or_404(id)
    return jsonify(cenario.to_dict()), 200
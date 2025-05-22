from flask import request, jsonify
from app.routes import bp
from app.db import db
from app.models import Item, Cenario, Rota, Sessao, Desafio
from app.auth import token_required

# ------------------ ITENS ------------------
@bp.route('/itens', methods=['POST'])
@token_required
def criar_item(current_user):
    data = request.get_json()
    item = Item(nome=data['nome'], descricao=data.get('descricao'), jogador_id=data['jogador_id'])
    db.session.add(item)
    db.session.commit()
    return jsonify({'id': item.id}), 201

@bp.route('/itens', methods=['GET'])
@token_required
def listar_itens(current_user):
    itens = Item.query.all()
    return jsonify([{'id': i.id, 'nome': i.nome, 'descricao': i.descricao, 'jogador_id': i.jogador_id} for i in itens]), 200

@bp.route('/itens/<int:id>', methods=['PUT'])
@token_required
def atualizar_item(current_user, id):
    item = Item.query.get_or_404(id)
    data = request.get_json()

    # Atualiza apenas se os dados existirem no payload
    if 'nome' in data:
        item.nome = data['nome']
    if 'descricao' in data:
        item.descricao = data['descricao']
    if 'jogador_id' in data:
        item.jogador_id = data['jogador_id']

    db.session.commit()
    return jsonify(item.to_dict()), 200  # mostra o item atualizado

@bp.route('/itens/<int:id>', methods=['DELETE'])
@token_required
def deletar_item(current_user, id):
    item = Item.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': f'Item {id} deletado com sucesso'}), 200


# Obter jogador por ID
@bp.route('/itens/<int:id>', methods=['GET'])
@token_required
def obter_itens(current_user, id):
    item = Item.query.get_or_404(id)
    return jsonify(item.to_dict()), 200
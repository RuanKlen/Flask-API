from flask import request, jsonify
from app.routes import bp
from app.db import db
from app.models import Item
from app.auth import admin_required, token_required

# ------------------ ITENS ------------------
@bp.route('/itens', methods=['POST'])
@admin_required
def criar_item(current_user, current_role):
    data = request.get_json()

    # Validação dos dados recebidos
    if not data:
        return jsonify({'erro': 'Nenhum dado fornecido'}), 400

    # Campos obrigatórios
    campos_obrigatorios = ['nome', 'tipo', 'raridade']

    # Verifica campos faltando
    campos_faltando = [campo for campo in campos_obrigatorios if not data.get(campo)]
    if campos_faltando:
        return jsonify({
            'erro': 'Campos obrigatórios ausentes',
            'campos_faltando': campos_faltando
        }), 400

    # Criação do item sem exigir jogador_id
    item = Item(
        nome=data['nome'],
        tipo=data['tipo'],
        raridade=data['raridade'],
        descricao=data.get('descricao'),  # opcional
        jogador_id=data.get('jogador_id')  # opcional
    )

    db.session.add(item)
    db.session.commit()

    return jsonify({'id': item.id, 'mensagem': 'Item criado com sucesso'}), 201

@bp.route('/itens', methods=['GET'])
@token_required
def listar_itens(current_user, current_role):
    itens = Item.query.all()
    return jsonify([{'id': i.id, 'nome': i.nome, 'tipo': i.tipo, 'raridade': i.raridade, 'descricao': i.descricao, 'jogador_id': i.jogador_id} for i in itens]), 200

@bp.route('/itens/<int:id>', methods=['PUT'])
@admin_required
def atualizar_item(current_user, current_role, id):
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
@admin_required
def deletar_item(current_user, current_role, id):
    item = Item.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': f'Item {id} deletado com sucesso'}), 200


# Obter jogador por ID
@bp.route('/itens/<int:id>', methods=['GET'])
@token_required
def obter_itens(current_user, current_role, id):
    item = Item.query.get_or_404(id)
    return jsonify(item.to_dict()), 200
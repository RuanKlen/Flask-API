from flask import request, jsonify
from app.routes import bp
from app.db import db
from app.models import Item, Cenario, Rota, Sessao, Desafio
from app.auth import token_required

# ------------------ ROTAS ------------------
@bp.route('/rotas', methods=['POST'])
@token_required
def criar_rota(current_user):
    data = request.get_json()
    rota = Rota(tipo=data['tipo'], descricao=data.get('descricao'))
    db.session.add(rota)
    db.session.commit()
    return jsonify({'id': rota.id}), 201

@bp.route('/rotas', methods=['GET'])
@token_required
def listar_rotas(current_user):
    rotas = Rota.query.all()
    return jsonify([{'id': r.id, 'tipo': r.tipo, 'descricao': r.descricao} for r in rotas]), 200

@bp.route('/rotas/<int:id>', methods=['PUT'])
@token_required
def atualizar_rota_por_id(current_user, id):
    rota = Rota.query.get_or_404(id)
    data = request.get_json()

    if 'tipo' in data:
        rota.tipo = data['tipo']
    if 'descricao' in data:
        rota.descricao = data['descricao']

    db.session.commit()
    return jsonify(rota.to_dict()), 200


@bp.route('/rotas/<int:id>', methods=['DELETE'])
@token_required
def deletar_rota(current_user, id):
    rota = Rota.query.get_or_404(id)
    db.session.delete(rota)
    db.session.commit()
    return jsonify({'message': 'Rota deletada'}), 200

@bp.route('/rotas/<int:id>', methods=['GET'])
@token_required
def obter_rota(current_user, id):
    rota = Rota.query.get_or_404(id)
    return jsonify(rota.to_dict()), 200
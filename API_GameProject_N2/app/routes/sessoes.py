from flask import request, jsonify
from app.routes import bp
from app.db import db
from app.models import Item, Cenario, Rota, Sessao, Desafio
from app.auth import token_required

# ------------------ SESSOES ------------------
@bp.route('/sessoes', methods=['POST'])
@token_required
def criar_sessao(current_user):
    data = request.get_json()
    sessao = Sessao(jogador_id=data['jogador_id'], cenario_id=data['cenario_id'], tempo_total=data.get('tempo_total'), modo_jogo=data.get('modo_jogo'), coop=data.get('coop', False))
    db.session.add(sessao)
    db.session.commit()
    return jsonify({'id': sessao.id}), 201

@bp.route('/sessoes', methods=['GET'])
@token_required
def listar_sessoes(current_user):
    sessoes = Sessao.query.all()
    return jsonify([{'id': s.id, 'jogador_id': s.jogador_id, 'cenario_id': s.cenario_id, 'tempo_total': s.tempo_total, 'modo_jogo': s.modo_jogo, 'coop': s.coop} for s in sessoes]), 200

@bp.route('/sessoes/<int:id>', methods=['PUT'])
@token_required
def atualizar_sessao_por_id(current_user, id):
    sessao = Sessao.query.get_or_404(id)
    data = request.get_json()

    if 'jogador_id' in data:
        sessao.jogador_id = data['jogador_id']
    if 'cenario_id' in data:
        sessao.cenario_id = data['cenario_id']
    if 'tempo_total' in data:
        sessao.tempo_total = data['tempo_total']
    if 'modo_jogo' in data:
        sessao.modo_jogo = data['modo_jogo']
    if 'coop' in data:
        sessao.coop = data['coop']

    db.session.commit()
    return jsonify(sessao.to_dict()), 200


@bp.route('/sessoes/<int:id>', methods=['DELETE'])
@token_required
def deletar_sessao(current_user, id):
    sessao = Sessao.query.get_or_404(id)
    db.session.delete(sessao)
    db.session.commit()
    return jsonify({'message': 'Sessão deletada'}), 200

@bp.route('/sessoes/<int:id>', methods=['GET'])
@token_required
def obter_sessao(current_user, id):
    sessao = Sessao.query.get_or_404(id)
    return jsonify(sessao.to_dict()), 200
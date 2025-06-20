from flask import request, jsonify
from app.routes import bp
from app.db import db
from app.models import Sessao
from app.auth import admin_required, token_required

# ------------------ SESSOES ------------------
@bp.route('/sessoes', methods=['POST'])
@admin_required
def criar_sessao(current_user, current_role):
    data = request.get_json()

    sessao = Sessao(
        jogador_id=data['jogador_id'],
        cenario_id=data['cenario_id'],
        desafio_id=data['desafio_id'],
        rota_id=data.get('rota_id'),  
        tempo_total=data.get('tempo_total'),
        modo_jogo=data.get('modo_jogo'),
        coop=data.get('coop', False)
    )
    #Verifica se o jogador existe
    if 'jogador_id' in data:
        from app.models import Jogador
        if not Jogador.query.get(data['jogador_id']):
            return jsonify({'error': 'O jogador com esse ID não existe'}), 400
        sessao.jogador_id = data['jogador_id']
    #Verifica se a rota existe
    rota_id = data.get('rota_id')
    if rota_id is not None:
        from app.models import Rota
        if not Rota.query.get(rota_id):
            return jsonify({'error': 'Rota com esse ID não existe'}), 400
    #Verifica se o cenario existe
    if 'cenario_id' in data:
        from app.models import Cenario
        if not Cenario.query.get(data['cenario_id']):
            return jsonify({'error': 'O cenário com esse ID não existe'}), 400
        sessao.cenario_id = data['cenario_id']
    if 'desafio_id' in data:
        from app.models import Desafio
        if not Desafio.query.get(data['desafio_id']):
            return jsonify({'error': 'O desafio com esse ID não existe'}), 400
        sessao.cenario_id = data['desafio_id']

    db.session.add(sessao)
    db.session.commit()
    return jsonify({'id': sessao.id}), 201

@bp.route('/sessoes', methods=['GET'])
@token_required
def listar_sessoes(current_user, current_role):
    sessoes = Sessao.query.all()
    return jsonify([{'id': s.id, 'jogador_id': s.jogador_id, 'cenario_id': s.cenario_id, 'desafio_id': s.desafio_id, 'tempo_total': s.tempo_total, 'modo_jogo': s.modo_jogo, 'coop': s.coop, 'rota_id': s.rota_id} for s in sessoes]), 200

@bp.route('/sessoes/<int:id>', methods=['PUT'])
@admin_required
def atualizar_sessao_por_id(current_user, current_role, id):
    sessao = Sessao.query.get_or_404(id)
    data = request.get_json()

    if 'jogador_id' in data:
        from app.models import Jogador
        if not Jogador.query.get(data['jogador_id']):
            return jsonify({'error': 'O jogador com esse ID não existe'}), 400
        sessao.jogador_id = data['jogador_id']
    
    if 'cenario_id' in data:
        from app.models import Cenario
        if not Cenario.query.get(data['cenario_id']):
            return jsonify({'error': 'O cenário com esse ID não existe'}), 400
        sessao.cenario_id = data['cenario_id']
    
    if 'desafio_id' in data:
        from app.models import Desafio
        if not Desafio.query.get(data['desafio_id']):
            return jsonify({'error': 'O desafio com esse ID não existe'}), 400
        sessao.cenario_id = data['desafio_id']

    if 'rota_id' in data:
        from app.models import Rota
        if not Rota.query.get(data['rota_id']):
            return jsonify({'error': 'Rota com esse ID não existe'}), 400
        sessao.rota_id = data['rota_id']
    
    if 'tempo_total' in data:
        sessao.tempo_total = data['tempo_total']
    if 'modo_jogo' in data:
        sessao.modo_jogo = data['modo_jogo']
    if 'coop' in data:
        sessao.coop = data['coop']

    db.session.commit()
    return jsonify(sessao.to_dict()), 200


@bp.route('/sessoes/<int:id>', methods=['DELETE'])
@admin_required
def deletar_sessao(current_user, current_role, id):
    sessao = Sessao.query.get_or_404(id)
    db.session.delete(sessao)
    db.session.commit()
    return jsonify({'message': 'Sessão deletada'}), 200

@bp.route('/sessoes/<int:id>', methods=['GET'])
@token_required
def obter_sessao(current_user, current_role, id):
    sessao = Sessao.query.get_or_404(id)
    return jsonify(sessao.to_dict()), 200
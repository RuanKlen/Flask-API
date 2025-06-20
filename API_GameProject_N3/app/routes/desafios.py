from flask import request, jsonify
from app.routes import bp
from app.db import db
from app.models import Desafio, Jogador
from app.auth import admin_required, token_required

# ------------------ DESAFIOS ------------------
@bp.route('/desafios', methods=['POST'])
@admin_required
def criar_desafio(current_user, current_role):
    data = request.get_json()
    
    desafio = Desafio(
        jogador_id=data['jogador_id'], 
        nome=data['nome'], 
        tentativas=data.get('tentativas', 1), 
        tempo=data.get('tempo'), 
        pontos=data.get('pontos'), 
        coop=data.get('coop', False)
        )
    
    db.session.add(desafio)
    
    jogador = Jogador.query.get(desafio.jogador_id)
    if jogador:
        jogador.pontuacao += desafio.pontos or 0  # Garante que pontos nulos não causem erro

    db.session.commit()
    
    return jsonify({'id': desafio.id}), 201

@bp.route('/desafios', methods=['GET'])
@token_required
def listar_desafios(current_user, current_role):
    desafios = Desafio.query.all()
    return jsonify([{'id': d.id, 'jogador_id': d.jogador_id, 'nome': d.nome, 'tentativas': d.tentativas, 'tempo': d.tempo, 'pontos': d.pontos, 'coop': d.coop} for d in desafios]), 200

@bp.route('/desafios/<int:id>', methods=['PUT'])
@admin_required
def atualizar_desafio_por_id(current_user, current_role, id):
    desafio = Desafio.query.get_or_404(id)
    data = request.get_json()

    if 'jogador_id' in data:
        desafio.jogador_id = data['jogador_id']
    if 'nome' in data:
        desafio.nome = data['nome']
    if 'tentativas' in data:
        desafio.tentativas = data['tentativas']
    if 'tempo' in data:
        desafio.tempo = data['tempo']
    if 'pontos' in data:
        desafio.pontos = data['pontos']
    if 'coop' in data:
        desafio.coop = data['coop']

    jogador = Jogador.query.get(desafio.jogador_id)
    if jogador:
        jogador.pontuacao += desafio.pontos or 0  # Garante que pontos nulos não causem erro
        
    db.session.commit()
    return jsonify(desafio.to_dict()), 200

@bp.route('/desafios/<int:id>', methods=['DELETE'])
@admin_required
def deletar_desafio(current_user, current_role, id):
    desafio = Desafio.query.get_or_404(id)
    db.session.delete(desafio)
    db.session.commit()
    return jsonify({'message': 'Desafio deletado'}), 200

@bp.route('/desafios/<int:id>', methods=['GET'])
@token_required
def obter_desafio(current_user, current_role, id):
    desafio = Desafio.query.get_or_404(id)
    return jsonify(desafio.to_dict()), 200

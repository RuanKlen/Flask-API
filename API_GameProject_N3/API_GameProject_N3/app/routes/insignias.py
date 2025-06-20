from flask import jsonify, request
from app.routes import bp
from app.db import db
from app.models import Jogador, Insignia, Sessao, Desafio, Cenario, Rota
from app.auth import token_required

# Função auxiliar para criar as insígnias no banco de dados pela primeira vez
def inicializar_insignias():
    if Insignia.query.count() == 0:
        insignias_data = [
            {'nome': 'Explorador Novato', 'descricao': 'Concluiu seu primeiro cenário.'},
            {'nome': 'Guerreiro Tenaz', 'descricao': 'Venceu seu primeiro desafio.'},
            {'nome': 'Mestre dos Cenários', 'descricao': 'Concluiu todos os cenários disponíveis.'},
            {'nome': 'Caçador de Segredos', 'descricao': 'Encontrou uma rota secreta.'},
            {'nome': 'Herói Cooperativo', 'descricao': 'Completou 10 sessões ou desafios em modo cooperativo.'},
            {'nome': 'Veterano de Guerra', 'descricao': 'Acumulou mais de 10.000 pontos.'},
            {'nome': 'Maratonista', 'descricao': 'Jogou por mais de 24 horas no total.'}
        ]
        for data in insignias_data:
            db.session.add(Insignia(**data))
        db.session.commit()

# Função que centraliza a lógica de verificação
def verificar_e_atribuir_insignias(jogador):
    inicializar_insignias() # Garante que as insígnias existem

    # 1. Explorador Novato
    if Sessao.query.filter_by(jogador_id=jogador.id).count() >= 1:
        insignia = Insignia.query.filter_by(nome='Explorador Novato').first()
        if insignia not in jogador.insignias:
            jogador.insignias.append(insignia)
            
    # 2. Guerreiro Tenaz
    if Desafio.query.filter_by(jogador_id=jogador.id).count() >= 1:
        insignia = Insignia.query.filter_by(nome='Guerreiro Tenaz').first()
        if insignia not in jogador.insignias:
            jogador.insignias.append(insignia)

    # 3. Mestre dos Cenários
    total_cenarios = Cenario.query.count()
    cenarios_completos = db.session.query(Sessao.cenario_id).filter_by(jogador_id=jogador.id).distinct().count()
    if total_cenarios > 0 and cenarios_completos >= total_cenarios:
        insignia = Insignia.query.filter_by(nome='Mestre dos Cenários').first()
        if insignia not in jogador.insignias:
            jogador.insignias.append(insignia)
            
    # 4. Caçador de Segredos
    rota_secreta_id = db.session.query(Rota.id).filter_by(tipo='secreta').first()
    if rota_secreta_id and Sessao.query.filter_by(jogador_id=jogador.id, rota_id=rota_secreta_id[0]).first():
        insignia = Insignia.query.filter_by(nome='Caçador de Segredos').first()
        if insignia not in jogador.insignias:
            jogador.insignias.append(insignia)

    # 5. Herói Cooperativo
    sessoes_coop = Sessao.query.filter_by(jogador_id=jogador.id, coop=True).count()
    desafios_coop = Desafio.query.filter_by(jogador_id=jogador.id, coop=True).count()
    if (sessoes_coop + desafios_coop) >= 10:
        insignia = Insignia.query.filter_by(nome='Herói Cooperativo').first()
        if insignia not in jogador.insignias:
            jogador.insignias.append(insignia)
            
    # 6. Veterano de Guerra
    if jogador.pontuacao > 10000:
        insignia = Insignia.query.filter_by(nome='Veterano de Guerra').first()
        if insignia not in jogador.insignias:
            jogador.insignias.append(insignia)

    # 7. Maratonista
    tempo_total_jogado = db.session.query(db.func.sum(Sessao.tempo_total)).filter_by(jogador_id=jogador.id).scalar() or 0
    if tempo_total_jogado > 86400: # 24 horas em segundos
        insignia = Insignia.query.filter_by(nome='Maratonista').first()
        if insignia not in jogador.insignias:
            jogador.insignias.append(insignia)
            
    db.session.commit()

@bp.route('/jogadores/<int:id>/insignias', methods=['GET'])
@token_required
def get_jogador_insignias(current_user, current_role, id):
    """Recupera todas as insígnias de um jogador específico."""
    jogador = Jogador.query.get_or_404(id)
    
    db.session.refresh(jogador)

    # Executa a verificação e atribuição (lógica on-demand)
    verificar_e_atribuir_insignias(jogador)
    
    # Retorna as insígnias que o jogador possui
    insignias = jogador.insignias
    return jsonify([insignia.to_dict() for insignia in insignias]), 200

# Adicione este código ao final de app/recompensas.py

@bp.route('/ranking', methods=['GET'])
@token_required
def get_ranking(current_user, current_role):
    """Recupera o ranking geral de jogadores com base na pontuação."""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Usamos .paginate() para performance e escalabilidade
    jogadores_paginados = Jogador.query.order_by(Jogador.pontuacao.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    jogadores = jogadores_paginados.items
    
    response = {
        'ranking': [jogador.to_dict() for jogador in jogadores],
        'total_jogadores': jogadores_paginados.total,
        'pagina_atual': jogadores_paginados.page,
        'total_paginas': jogadores_paginados.pages
    }
    
    return jsonify(response), 200



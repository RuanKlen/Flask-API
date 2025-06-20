from flask import Blueprint

bp = Blueprint('main', __name__)

from app.routes import jogadores, itens, cenarios, rotas, sessoes, desafios, insignias

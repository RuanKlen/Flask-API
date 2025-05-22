from flask import Blueprint

bp = Blueprint('main', __name__)

from app.routes import jogadores
from app.routes import itens, cenarios, rotas, sessoes, desafios

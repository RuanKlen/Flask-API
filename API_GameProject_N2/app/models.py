from app.db import db

class Jogador(db.Model):  # cria o modelo de objeto para o banco de dados
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)  # Nome do jogador (obrigatório)
    email = db.Column(db.String(100), unique=True, nullable=False)  # Email do jogador (único e obrigatório)
    senha = db.Column(db.String(255), nullable=False)  # Senha do jogador (armazenada de forma segura)
    data_cadastro = db.Column(db.DateTime, default=db.func.current_timestamp())  # Data de cadastro (automática)
    pontuacao = db.Column(db.Integer, default=0)  # Pontuação do jogador (inicia em 0)
    ativo = db.Column(db.Boolean, default=True)  # Indica se o jogador está ativo (padrão: True)

    # converte o objeto para um dicionário
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'data_cadastro': self.data_cadastro.isoformat(),  # Formata a data para JSON
            'pontuacao': self.pontuacao,
            'ativo': self.ativo
        }

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(255))
    jogador_id = db.Column(db.Integer, db.ForeignKey('jogador.id'), nullable=False)
    

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao,
            'jogador_id': self.jogador_id
        }


class Cenario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    dificuldade = db.Column(db.String(50))
    descricao = db.Column(db.Text)

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'dificuldade': self.dificuldade,
            'descricao': self.descricao
        }

class Rota(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50))  # principal, secundária, secreta
    descricao = db.Column(db.Text)


    def to_dict(self):
        return {
            'id': self.id,
            'tipo': self.tipo,
            'descricao': self.descricao,
        }
    
class Sessao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jogador_id = db.Column(db.Integer, db.ForeignKey('jogador.id'), nullable=False)
    cenario_id = db.Column(db.Integer, db.ForeignKey('cenario.id'), nullable=False)
    tempo_total = db.Column(db.Integer)
    modo_jogo = db.Column(db.String(20))  # fácil, médio, difícil
    coop = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            'id': self.id,
            'jogador_id': self.jogador_id,
            'cenario_id': self.cenario_id,
            'tempo_total': self.tempo_total,
            'modo_jogo': self.modo_jogo,
            'coop': self.coop, 
        }


class Desafio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jogador_id = db.Column(db.Integer, db.ForeignKey('jogador.id'), nullable=False)
    nome = db.Column(db.String(100))  # nome do desafio ou chefe
    tentativas = db.Column(db.Integer, default=1)
    tempo = db.Column(db.Integer)  # segundos
    pontos = db.Column(db.Integer)
    coop = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            'id': self.id,
            'jogador_id': self.jogador_id,
            'nome': self.nome,
            'tentativas': self.tentativas,
            'tempo': self.tempo,
            'pontos': self.pontos,
            'coop': self.coop,
        }
import os

# caminho relativo para a aplicação
#ALGO COMO: C:\Users\andrei.carniel\PycharmProjects\API_project_v1
# ou C:\Users\Joao\Downloads\API_project_v1

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # buscar um arquivo na estrutura de arquivos contendo a chave secreta
    # utilizamos o you-will-never-guess para ambiente de desenvolvimento
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    # endereço do banco de dados
    # Resultando em: C:\Users\andrei.carniel\PycharmProjects\API_project_v1\app.db
    # OU C:\Users\Joao\Downloads\API_project_v1\app.db
    # /opt/API_project_v1/app.db (linux)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    # se quiser fazer log de todas as modificações
    SQLALCHEMY_TRACK_MODIFICATIONS = False
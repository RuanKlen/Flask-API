# 📚 API_GameProject_N2

Este repositório contém a **API back-end** desenvolvida como parte da avaliação da disciplina **Server-Side** da Universidade Católica de Santa Catarina (CatólicaSC). O projeto está integrado ao componente **PAC Extensionista**, onde o foco é o desenvolvimento de um **jogo educacional de matemática** voltado para alunos do 7º ano do Ensino Fundamental que necessitam de reforço escolar.

## 🎯 Objetivo do Projeto

Criar uma API robusta para gerenciar jogadores, progresso, níveis, conquistas e itens, que será utilizada por um jogo educacional com a temática **matemática**, desenvolvido em equipe. A API serve como o sistema central de dados e autenticação para o jogo.

---

## 🗂 Estrutura do Repositório
📁 API_GameProject_N2/ # Pasta principal do projeto com os arquivos da API
📦 API_GameProject_N2.rar # Versão compactada do projeto
🧪 Insomnia.yaml # Arquivo de testes de rotas (Insomnia)
🧪 Insomnia_N2_Andrei... # (Insomnia)

---

## 🚀 Tecnologias Utilizadas

- **Python 3.11**
- **Flask** (framework web)
- **Flask-JWT-Extended** (autenticação via token JWT)
- **Flask-Migrate + SQLAlchemy** (ORM e controle de migrações)
- **SQLite** (banco de dados local simples)
- **Insomnia** (para testar e validar endpoints da API)

---

## 📌 Funcionalidades da API

- ✅ Cadastro e autenticação de jogadores e admins via JWT
- ✅ Controle de acesso por tipo de usuário (player/admin)
- ✅ Rotas protegidas para:
  - 📄 Listar jogadores
  - 🧩 Controlar progresso do jogador
  - 🧠 Gerenciar níveis e conquistas
  - 🎒 Atribuir e listar itens
- ✅ Testes de rotas prontos via arquivos `.yaml` para Insomnia

---

## 🛠 Como executar o projeto

### 1. Crie um ambiente virtual e ative
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

### 2. Instale as dependências
pip install -r requirements.txt

### 3. Execute as migrações e rode o servidor
flask db init
flask db migrate
flask db upgrade
flask run

---

## 🔐 Autenticação
A API utiliza JWT para proteger rotas. É necessário:

1.Fazer login via /login para obter o token

2.Enviar o token no header Authorization: Bearer <token> nas demais requisições protegidas

---

## 🧪 Testes com Insomnia
Dois arquivos .yaml estão disponíveis para testar todos os endpoints com o Insomnia:

Insomnia.yaml — inclui todas as rotas

---

## 👨‍🏫 Sobre o Projeto Educacional
Este projeto faz parte do PAC Extensionista da CatólicaSC e tem como missão desenvolver um jogo de reforço escolar em matemática para alunos do 7º ano do Ensino Fundamental. A API aqui desenvolvida é um protótipo e ao final, fornecerá todo o suporte de dados necessário ao jogo, permitindo o rastreamento de progresso, desafios, recompensas e mais.

---

## 👥 Desenvolvedores
Ruan Klen (responsável pelo repositório)
Gustavo Voltolini
Vitor Mayer
Luiz Côrrea

---

## 🏫 Universidade
Universidade Católica de Santa Catarina
Curso: Engenharia de Software
Disciplina: Server-Side (N2)
Ano: 2025
Professor: Andrei Carniel

---

## 📄 Licença
Este projeto é de uso educacional e não possui fins lucrativos. Consulte seu professor para reutilização em outros projetos.

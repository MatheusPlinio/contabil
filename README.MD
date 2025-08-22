# 📄 Desafio Técnico – Desenvolvedor Python (Automação com Selenium)

Este projeto foi desenvolvido como parte do **Desafio Técnico – Conthabil**, com foco em automação, manipulação de arquivos e desenvolvimento de API em Python.

---

## 🚀 Objetivo
Automatizar a coleta do Diário Oficial da Prefeitura de Natal, realizar upload dos arquivos em um serviço externo e disponibilizar os resultados por meio de uma API com banco de dados PostgreSQL.

---

## 📌 Funcionalidades
1. **Coleta de Publicações**
   - Acessa o [Diário Oficial de Natal](https://www.natal.rn.gov.br/dom) via Selenium.
   - Filtra publicações do **mês anterior**.
   - Faz download dos arquivos PDF localmente.

2. **Upload dos Arquivos**
   - Realiza upload dos PDFs para o serviço [0x0.st](https://0x0.st).
   - Retorna URLs públicas para acesso aos arquivos.
   - Exibe as URLs no console.

3. **Banco de Dados (PostgreSQL)**
   - Armazena as URLs públicas com informações de data de publicação.
   - Cria uma API em Python (FastAPI/Flask) para gerenciar os dados.

4. **API Pública**
   - Rota para **listar todos os arquivos** armazenados.
   - Rota para **filtrar arquivos por competência** (mês/ano da publicação).

5. **Extras**
   - **Docker Compose** para orquestrar API + PostgreSQL.
   - Possibilidade de deploy em serviços como **Railway, Render ou AWS**.

---

## 🛠️ Tecnologias Utilizadas
- **Python 3.10+**
- **Selenium** (automação do navegador)
- **Requests** (upload de arquivos)
- **FastAPI** ou **Flask** (API REST)
- **PostgreSQL**
- **SQLAlchemy** (ORM)
- **Docker & Docker Compose**

---

## 📂 Estrutura do Projeto
```bash
├── app/
│   ├── main.py          # Arquivo principal da API
│   ├── database.py      # Conexão e modelos do banco
│   ├── routes.py        # Definição das rotas da API
│   ├── scraper.py       # Automação com Selenium
│   └── uploader.py      # Upload dos arquivos para 0x0.st
├── requirements.txt     # Dependências do projeto
├── Dockerfile           # Dockerfile da API
├── docker-compose.yml   # Orquestração API + PostgreSQL
└── README.md            # Documentação
```

⚙️ Como Executar o Projeto
1. Clonar o Repositório
```bash
git clone https://github.com/seu-usuario/desafio-conthabil.git
```

2. Configurar Variáveis de Ambiente

Crie um arquivo .env na raiz do projeto:

```bash
DATABASE_URL=postgresql://user:password@db:5432/desafio
```

3. Construir a Imagem Docker
```bash
docker build -t desafio-conthabil .
```

4. Executar o Container
```bash
docker run -p 8000:8000 desafio-conthabil
```

# Strava Stats

Aplicação web em Django para autenticar com Strava via OAuth2 e visualizar estatísticas de atividades com filtros, paginação e comparativos.

## Pré-requisitos

- Python 3.14+ para execução local (ou Docker)
- Docker e Docker Compose (opcional)
- Conta no Strava com uma aplicação criada

## Configuração no Strava

1. Acesse https://www.strava.com/settings/api
2. Crie uma aplicação
3. Configure `Authorization Callback Domain` como `localhost` (desenvolvimento local)
4. Garanta que o callback usado pela aplicação seja:
   `http://localhost:8000/strava-stats/auth/callback/`

## Variáveis de ambiente

A forma mais simples é gerar o `.env` com:

```bash
make env STRAVA_CLIENT_ID=seu_client_id STRAVA_CLIENT_SECRET=seu_client_secret
```

Isso cria:

- `STRAVA_CLIENT_ID`
- `STRAVA_CLIENT_SECRET`
- `DJANGO_SECRET_KEY`

Variáveis opcionais úteis:

- `DEBUG` (padrão: `True`)
- `ALLOWED_HOSTS` (padrão: `localhost,127.0.0.1`)
- `STRAVA_REDIRECT_URI` (padrão: `http://localhost:8000/strava-stats/auth/callback/`)

## Execução local (sem Docker)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements/development.txt
make migrate
make runserver
```

Acesse:

- http://localhost:8000/strava-stats/

## Execução com Docker

```bash
make build
make run
```

Acesse:

- http://localhost:8000/strava-stats/

## Comandos disponíveis

| Comando | Descrição |
|---------|-----------|
| `make help` | Lista os comandos |
| `make migrate` | Executa migrações (local) |
| `make runserver` | Inicia servidor Django (local) |
| `make build` | Build das imagens Docker |
| `make run` | Sobe os serviços Docker |
| `make execute` | Sobe Docker e executa `runserver` no container |
| `make sh` | Shell `sh` no container |
| `make bash` | Shell `bash` no container |
| `make logs` | Exibe logs do container |
| `make restart` | Reinicia os serviços Docker |
| `make stop` | Para e remove os serviços Docker |
| `make ruff` | Lint + formatação com Ruff (no container) |
| `make audit` | Auditoria de dependências com `pip-audit` |
| `make env STRAVA_CLIENT_ID=... STRAVA_CLIENT_SECRET=...` | Cria `.env` |

## Funcionalidades

- Autenticação OAuth2 com Strava
- Dashboard com resumo geral de atividades
- Cards principais com comparativo `filtrado / total`:
  atividades, tempo, distância e elevação
- Filtros por esporte, semana, mês e busca textual
- Filtro de semana resiliente no backend (`1` e `Semana 1`)
- Listas de semanas e meses sem períodos futuros
- Estatísticas por tipo de atividade, semana e mês
- Tabela de atividades com paginação

## Estrutura do projeto

```text
strava-stats/
├── manage.py
├── activities/
│   ├── services/
│   │   ├── strava_auth.py
│   │   ├── strava_api.py
│   │   ├── statistics.py
│   │   └── cache_service.py
│   ├── constants.py
│   ├── exceptions.py
│   ├── urls.py
│   └── views.py
├── strava_stats/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── templates/
├── static/
├── requirements/
├── Dockerfile
├── docker-compose.yaml
└── Makefile
```

## Stack

- Python 3
- Django 5
- Pandas 3
- TailwindCSS
- Docker / Docker Compose

## Licença

MIT

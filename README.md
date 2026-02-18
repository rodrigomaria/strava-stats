# Strava Stats

Aplicação web Django para visualizar estatísticas de atividades do Strava.

## Pré-requisitos

- Python 3.12+ (ou Docker)
- Conta no Strava com uma aplicação criada

## Configuração

### 1. Criar aplicação no Strava

1. Acesse https://www.strava.com/settings/api
2. Crie uma nova aplicação
3. Configure o **Authorization Callback Domain** como `localhost`

### 2. Configurar credenciais

```bash
make env STRAVA_CLIENT_ID=seu_client_id STRAVA_CLIENT_SECRET=seu_client_secret
```

### 3. Executar localmente

```bash
make install    # Instalar dependências
make migrate    # Executar migrações
make runserver  # Iniciar servidor
```

Acesse http://localhost:8000

### 4. Executar com Docker

```bash
make build   # Construir imagem
make run     # Iniciar container
```

## Comandos Disponíveis

| Comando | Descrição |
|---------|-----------|
| `make install` | Instalar dependências |
| `make migrate` | Executar migrações Django |
| `make runserver` | Iniciar servidor de desenvolvimento |
| `make build` | Construir container Docker |
| `make run` | Iniciar container Docker |
| `make execute` | Executar Django no Docker |
| `make stop` | Parar containers |
| `make ruff` | Executar linter |
| `make audit` | Auditoria de segurança |
| `make help` | Mostrar ajuda |

## Estrutura do Projeto

```
strava-stats/
├── manage.py
├── strava_stats/           # Configuração Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── activities/             # App principal
│   ├── services/           # Serviços modularizados
│   │   ├── strava_auth.py  # Autenticação OAuth2
│   │   ├── strava_api.py   # Cliente API Strava
│   │   └── statistics.py   # Processamento de estatísticas
│   ├── constants.py
│   ├── views.py
│   └── urls.py
├── templates/
└── static/
```

## Funcionalidades

- **Autenticação OAuth2**: Login automático com Strava
- **Dashboard**: Visualização completa das estatísticas
- **Estatísticas por Tipo**: Análise por esporte
- **Estatísticas Mensais/Semanais**: Acompanhamento temporal
- **Detalhes de Atividades**: Modal interativo

## Tecnologias

- Python 3.12
- Django 5.1
- Pandas
- TailwindCSS

## Licença

MIT
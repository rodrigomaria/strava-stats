# Strava Statistics

## Descrição
Este projeto contém um notebook Jupyter para interagir com a API do Strava, permitindo a análise de atividades esportivas.

## Requisitos
- Docker
- Docker Compose

## Configuração

### Variáveis de ambiente
Configure as seguintes variáveis de ambiente antes de executar o container:

- `STRAVA_CLIENT_ID`: Seu ID de cliente Strava
- `STRAVA_CLIENT_SECRET`: Seu segredo de cliente Strava

Você pode configurá-las diretamente no arquivo `.env` na raiz do projeto.

Para gerar essas variáveis, é necessário a criação de uma [app no Strava](https://developers.strava.com/docs/getting-started/#account).

## Uso
### Comandos Disponíveis

| Comando | Descrição |
|---------|-----------|
| `make build` | Constrói o container Docker |
| `make run` | Inicia o container em modo detached |
| `make jupyter` | Executa o servidor Jupyter Notebook |
| `make sh` | Acessa o container usando shell sh |
| `make bash` | Acessa o container usando bash |
| `make logs` | Mostra os logs do container |
| `make stop` | Para e remove o container |
| `make restart` | Reinicia o container |
| `make black` | Executa o formatador Black no código |
| `make help` | Mostra a ajuda com todos os comandos |

### Acessar o Jupyter Notebook
1. Execute o comando `make jupyter` para iniciar o servidor Jupyter Notebook
2. Abra seu navegador e acesse `http://localhost:8888`
3. Use o token de acesso mostrado no terminal para fazer login
4. Abra o notebook `strava_statistics.ipynb`

### Autenticação com Strava
1. Execute as células do notebook para obter o link de autorização
2. Abra o link no navegador e autorize o acesso
3. Copie a URL de redirecionamento e cole-a no notebook quando solicitado

## Notas
- Os dados e análises ficam salvos no volume montado.
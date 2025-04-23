# Strava Statistics

*[Português](#português) | [English](#english)*

<a id="português"></a>
## Português

### Descrição
Este projeto contém um notebook Jupyter para interagir com a API do Strava, permitindo a análise de atividades esportivas.

### Requisitos
- Docker
- Docker Compose

### Configuração

#### Variáveis de ambiente
Configure as seguintes variáveis de ambiente antes de executar o container:

- `STRAVA_CLIENT_ID`: Seu ID de cliente Strava
- `STRAVA_CLIENT_SECRET`: Seu segredo de cliente Strava

Você pode configurá-las diretamente no arquivo `.env` na raiz do projeto.

Para gerar essas variáveis, é necessário a criação de uma [app no Strava](https://developers.strava.com/docs/getting-started/#account).

### Uso
#### Comandos Disponíveis

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

#### Acessar o Jupyter Notebook
1. Execute o comando `make jupyter` para iniciar o servidor Jupyter Notebook
2. Abra seu navegador e acesse `http://localhost:8888`
3. Use o token de acesso mostrado no terminal para fazer login
4. Abra o notebook `strava_statistics.ipynb`

#### Autenticação com Strava
1. Execute as células do notebook para obter o link de autorização
2. Clique no link e autorize o acesso ao Strava
3. Copie a URL de redirecionamento e cole-a no notebook quando solicitado

### Notas
- Os dados e análises ficam salvos no volume montado.

---

<a id="english"></a>
## English

### Description
This project contains a Jupyter notebook to interact with the Strava API, allowing the analysis of sports activities.

### Requirements
- Docker
- Docker Compose

### Configuration

#### Environment Variables
Configure the following environment variables before running the container:

- `STRAVA_CLIENT_ID`: Your Strava client ID
- `STRAVA_CLIENT_SECRET`: Your Strava client secret

You can configure them directly in the `.env` file at the root of the project.

To generate these variables, you need to create a [Strava app](https://developers.strava.com/docs/getting-started/#account).

### Usage
#### Available Commands

| Command | Description |
|---------|-------------|
| `make build` | Build the Docker container |
| `make run` | Start the container in detached mode |
| `make jupyter` | Run the Jupyter Notebook server |
| `make sh` | Access the container using sh shell |
| `make bash` | Access the container using bash |
| `make logs` | Show container logs |
| `make stop` | Stop and remove the container |
| `make restart` | Restart the container |
| `make black` | Run the Black formatter on the code |
| `make help` | Show help with all commands |

#### Accessing the Jupyter Notebook
1. Run the `make jupyter` command to start the Jupyter Notebook server
2. Open your browser and go to `http://localhost:8888`
3. Use the access token shown in the terminal to log in
4. Open the `strava_statistics.ipynb` notebook

#### Strava Authentication
1. Run the notebook cells to get the authorization link
2. Click on the link and authorize access to Strava
3. Copy the redirect URL and paste it into the notebook when prompted

### Notes
- Data and analyses are saved in the mounted volume.
### Instalar Depenências do Projeto

```bash
pip install -r requirements.txt
```

### Workspace do Postman com todas as requisições do backend, aceite o link de convite:

[Clique aqui para acessar o Workspace do Postman](https://app.getpostman.com/join-team?invite_code=7c67035b20e8719cc58c75e883e81455dce36048e0e30c1900a0d9fb58e5a477)

### Rodar a Aplicação em Docker ou usando banco de dados Local

Para rodar a aplicação rodando com Docker vá ao .env e adicione True para essa variável:

```bash
USE_DOCKER=True
```

Caso contrário se deseja rodar a aplicação localmente use:

```bash
USE_DOCKER=False
```

### Criar o Banco spacex_bd2

- Requisitos
  - Python 3.10 ou superior
  - Docker

OBS: Caso você queira testar com um banco de dados local, só será preciso alterar as variáveis de ambiente no arquivo `.env` localizado na raiz do projeto.

1. Encontre a pasta `dba` dentro do diretório do projeto.

```bash
cd dba
```

2. Execute o comando para criar o banco de dados `spacex_bd2`:

```bash
python create_db.py
```

### Carga de Dados da API

1. Certifique-se de que o banco de dados `spacex_bd2` foi criado com sucesso.

```bash
cd dba
```

2. Execute o comando para carregar os dados da API SpaceX no banco de dados:

```bash
python load_database.py
```

#### Gerar as Classes Modelos com sqlacodegen

Para gerar as classes modelos do SQLAlchemy a partir de um banco de dados existente, você pode usar o `sqlacodegen`. Siga os passos abaixo:

1. Na raiz do projeto rode o comando para subir a instância do banco com posgtres:

```bash
docker compose up -d
```

2. Acesse o diretório onde está localizado o script `generate_models.sh`:

```bash
cd backend/scripts
```

3. Gere o executável do `generate_models.sh`:

```bash
chmod +x generate_models.sh
```

4. Execute o script `generate_models.sh`:

```bash
./generate_models.sh
```

3. O script irá gerar os arquivos de modelos no diretório `backend/app/models/`. Você pode verificar os arquivos gerados para garantir que as classes estão corretas.

### Gerar o novo backup do banco de dados

Para gerar um novo backup do banco de dados `spacex_bd2`, você pode seguir os passos abaixo:

1. Certifique-se de que o banco de dados `spacex_bd2` está rodando.

```bash
cd backend/scripts
```

2. Execute o comando para gerar o backup:

```bash
chmod +x generate_backup.sh

```

```bash
./generate_backup

```

### Iniciando servidor Backend e Frontend

Para iniciar o servidor backend e frontend, você pode seguir os passos abaixo:

1. Certifique-se de que o banco de dados está rodando e que as dependências do projeto foram instaladas.

```bash
cd backend && python main.py
```

2. Abra um novo terminal e navegue até o diretório do frontend:

```bash
cd frontend && npm install && npm run dev
```

### Instalar Depenências do Projeto

```bash
pip install -r requirements.txt
```

### Criar o Banco spacex_bd2

- Requisitos
  - Python 3.10 ou superior
  - Docker

OBS: Caso você queira testar com um banco de dados local, só será preciso alterar as variáveis de ambiente no arquivo `.env` localizado na raiz do projeto.

1. Encontre a pasta `dba` dentro do diretório do projeto. (certifique-se que o docker esteja rodando)

```bash
cd dba
```

2. Execute o comando para criar o banco de dados `spacex_bd2`:

```bash
python create_db.py
```

### Carga de Dados da API

1. Certifique-se de que o banco de dados `spacex_bd2` foi criado com sucesso e que o Docker está rodando.

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

from sqlalchemy import select, Table, MetaData, and_
from sqlalchemy.exc import NoSuchTableError
from app.daos.base_dao import BaseDAO
from app.exceptions.exceptions import DaoError
from datetime import date
from collections import defaultdict


class RelatorioDao(BaseDAO):

    def tratar_valor(self, coluna_nome: str, valor):
        if isinstance(valor, list) and len(valor) == 2:
            if 'date' in coluna_nome or 'time' in coluna_nome:
                try:
                    return [date.fromisoformat(valor[0]), date.fromisoformat(valor[1])]
                except Exception:
                    pass
        elif isinstance(valor, str):
            if 'date' in coluna_nome or 'time' in coluna_nome:
                try:
                    return date.fromisoformat(valor)
                except Exception:
                    pass
        return valor
    def extrair_relacoes(self, tables):
        # Cria um dicionário onde cada chave (tabela) aponta para uma lista de relacionamentos (joins possíveis)
        relacoes = defaultdict(list)

        # Cria um dicionário que associa o nome da tabela ao objeto Table do SQLAlchemy
        nome_para_tabela = {t.name: t for t in tables}

        # Percorre cada tabela para identificar suas chaves estrangeiras
        for tabela in tables:
            for fk in tabela.foreign_keys:
                # Nome da tabela de origem (onde está a FK)
                origem = tabela.name

                # Nome da tabela de destino (a tabela referenciada pela FK)
                destino = fk.column.table.name

                # Condição de join: coluna da origem == coluna da FK na tabela destino
                condicao = fk.parent == fk.column

                # Armazena a relação no grafo (unidirecional)
                relacoes[origem].append((destino, condicao))

                # Também armazena o inverso (bidirecional) — necessário para montar os joins de qualquer lado
                relacoes[destino].append((origem, condicao))

        # Retorna:
        # - o dicionário de relacionamentos (grafo)
        # - o mapa de nome → tabela (para uso posterior nos joins)
        return relacoes, nome_para_tabela

    
    #  uso um especie de BFS para percorrer as tabelas 
    def montar_joins(self, query, tabelas_usadas, relacoes, nome_para_tabela):
        # Conjunto para rastrear quais tabelas já foram incluídas na query (com join ou como base)
        tabelas_joined = set()

        # Conjunto das tabelas que ainda precisam ser conectadas
        tabelas_restantes = set(tabelas_usadas)

        # Define a primeira tabela como a base da consulta (FROM)
        primeira = tabelas_usadas[0]
        query = query.select_from(nome_para_tabela[primeira])
        tabelas_joined.add(primeira)
        tabelas_restantes.remove(primeira)

        # Enquanto ainda houver tabelas que precisam ser conectadas
        while tabelas_restantes:
            # Para cada tabela já conectada
            for base in list(tabelas_joined):
                # Procura nos relacionamentos dessa tabela
                for destino, condicao in relacoes[base]:
                    # Se encontrar uma tabela de destino que ainda não foi conectada
                    if destino in tabelas_restantes:
                        # Faz o join com a tabela de destino usando a condição extraída da FK
                        query = query.join(nome_para_tabela[destino], condicao)

                        # Marca essa tabela como já conectada
                        tabelas_joined.add(destino)
                        tabelas_restantes.remove(destino)

                        # Interrompe o loop interno para recomeçar com a nova tabela conectada
                        break
                else:
                    # Se não encontrou nenhum destino conectável para essa base, continua para a próxima
                    continue

                # Se conseguiu fazer um join neste passo, quebra o loop externo para reiniciar
                break
            else:
                # Se depois de tentar todas as tabelas conectadas, nenhuma tabela restante pôde ser conectada,
                # então o conjunto de tabelas solicitado não está todo interligado — gera erro
                raise DaoError("Não foi possível conectar todas as tabelas solicitadas.")

        # Retorna a query com todos os joins necessários montados
        return query


    def buscar_dados(self, tabelas: list[str], colunas: list[str], filtros: list[dict]) -> list[dict]:
        metadata = MetaData()
        try:
            with self.get_session() as session:
                # Carrega as tabelas dinamicamente
                tables = [Table(t, metadata, autoload_with=session.bind) for t in tabelas]
                nome_para_tabela = {t.name: t for t in tables}

                # Monta colunas selecionadas
                cols = []
                for col in colunas:
                    tabela_nome, coluna_nome = col.split('.', 1)
                    tabela_obj = nome_para_tabela[tabela_nome]
                    cols.append(tabela_obj.c[coluna_nome])

                query = select(*cols)

                # Condições dos filtros
                condicoes = []
                for f in filtros:
                    tabela_nome, coluna_nome = f['coluna'].split('.', 1)
                    tabela_obj = nome_para_tabela[tabela_nome]
                    coluna_obj = tabela_obj.c[coluna_nome]
                    valor = self.tratar_valor(coluna_nome, f['valor'])

                    op = f['operador']
                    val = valor
                    if op == 'igual a':
                        condicoes.append(coluna_obj == val)
                    elif op == 'maior que':
                        condicoes.append(coluna_obj > val)
                    elif op == 'menor que':
                        condicoes.append(coluna_obj < val)
                    elif op == 'maior ou igual a':
                        condicoes.append(coluna_obj >= val)
                    elif op == 'menor ou igual a':
                        condicoes.append(coluna_obj <= val)
                    elif op == 'diferente de':
                        condicoes.append(coluna_obj != val)
                    elif op == 'parecido com':
                        condicoes.append(coluna_obj.like('%' + val + '%'))
                    elif op == 'entre' and isinstance(val, (list, tuple)) and len(val) == 2:
                        condicoes.append(coluna_obj.between(val[0], val[1]))
                    else:
                        raise DaoError(f"Operador desconhecido ou inválido: {op}")

                # Extrai relações e aplica joins dinâmicos
                relacoes, nome_para_tabela = self.extrair_relacoes(tables)

                query = self.montar_joins(query, tabelas, relacoes, nome_para_tabela)

                if condicoes:
                    query = query.where(and_(*condicoes))

                resultado = session.execute(query)
                rows = resultado.fetchall()
                keys = resultado.keys()

                dados = [dict(zip(keys, row)) for row in rows]
                return dados

        except Exception as e:
            raise DaoError(f"Erro ao buscar dados do relatório: {e}")

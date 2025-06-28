from sqlalchemy import select, Table, MetaData, and_, func
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

    def buscar_dados(self, tabelas: list[str], colunas: list[str], filtros: list[dict], agregacoes: list[dict] = []) -> list[dict]:
        metadata = MetaData()
        try:
            with self.get_session() as session:
                tables = [Table(t, metadata, autoload_with=session.bind) for t in tabelas]
                nome_para_tabela = {t.name: t for t in tables}

                cols, group_by_cols, having_conditions = self.construir_colunas(colunas, agregacoes, nome_para_tabela)

                query = select(*cols)

                condicoes = self.construir_filtros(filtros, nome_para_tabela)

                relacoes, nome_para_tabela = self.extrair_relacoes(tables)
                query = self.montar_joins(query, tabelas, relacoes, nome_para_tabela)

                if condicoes:
                    query = query.where(and_(*condicoes))

                if agregacoes and group_by_cols:
                    query = query.group_by(*group_by_cols)

                if having_conditions:
                    query = query.having(and_(*having_conditions))

                print(query)

                resultado = session.execute(query)
                rows = resultado.fetchall()
                keys = resultado.keys()

                return [dict(zip(keys, row)) for row in rows]

        except Exception as e:
            raise DaoError(f"Erro ao buscar dados do relatório: {e}")

    def construir_colunas(self, colunas, agregacoes, nome_para_tabela):
        from sqlalchemy import func

        cols = []
        group_by_cols = []
        having_conditions = []

        for col in colunas:
            tabela_nome, coluna_nome = col.split('.', 1)
            tabela_obj = nome_para_tabela[tabela_nome]
            coluna_obj = tabela_obj.c[coluna_nome]
            cols.append(coluna_obj)
            group_by_cols.append(coluna_obj)

        for agg in agregacoes:
            tabela_nome, coluna_nome = agg['coluna'].split('.', 1)
            tabela_obj = nome_para_tabela[tabela_nome]
            coluna_obj = tabela_obj.c[coluna_nome]

            funcao = agg['funcao'].upper()
            alias = agg.get('alias', f'{funcao}_{coluna_nome}')

            expr = self.criar_agregacao(funcao, coluna_obj).label(alias)
            cols.append(expr)

            if 'having' in agg:
                having_expr = self.criar_agregacao(funcao, coluna_obj)
                op = agg['having']['operador']
                val = agg['having']['valor']
                cond = self.operador_para_expressao(having_expr, op, val)
                having_conditions.append(cond)

        return cols, group_by_cols, having_conditions

    def criar_agregacao(self, funcao, coluna_obj):
        from sqlalchemy import func
        match funcao:
            case 'COUNT': return func.count(coluna_obj)
            case 'SUM': return func.sum(coluna_obj)
            case 'AVG': return func.avg(coluna_obj)
            case 'MAX': return func.max(coluna_obj)
            case 'MIN': return func.min(coluna_obj)
            case _: raise DaoError(f"Função de agregação desconhecida: {funcao}")

    def operador_para_expressao(self, coluna_expr, operador, valor):
        match operador:
            case '>': return coluna_expr > valor
            case '>=': return coluna_expr >= valor
            case '<': return coluna_expr < valor
            case '<=': return coluna_expr <= valor
            case '=' | '==': return coluna_expr == valor
            case '!=': return coluna_expr != valor
            case _: raise DaoError(f"Operador HAVING inválido: {operador}")

    def construir_filtros(self, filtros, nome_para_tabela):
        condicoes = []
        for f in filtros:
            tabela_nome, coluna_nome = f['coluna'].split('.', 1)
            tabela_obj = nome_para_tabela[tabela_nome]
            coluna_obj = tabela_obj.c[coluna_nome]
            valor = self.tratar_valor(coluna_nome, f['valor'])

            op = f['operador']
            match op:
                case 'igual a': condicoes.append(coluna_obj == valor)
                case 'maior que': condicoes.append(coluna_obj > valor)
                case 'menor que': condicoes.append(coluna_obj < valor)
                case 'maior ou igual a': condicoes.append(coluna_obj >= valor)
                case 'menor ou igual a': condicoes.append(coluna_obj <= valor)
                case 'diferente de': condicoes.append(coluna_obj != valor)
                case 'parecido com': condicoes.append(coluna_obj.like(f"%{valor}%"))
                case 'entre' if isinstance(valor, (list, tuple)) and len(valor) == 2:
                    condicoes.append(coluna_obj.between(valor[0], valor[1]))
                case _: raise DaoError(f"Operador inválido ou mal formatado: {op}")

        return condicoes

    # def buscar_dados(self, tabelas: list[str], colunas: list[str], filtros: list[dict], agregacoes: list[dict] = []) -> list[dict]:
    #     metadata = MetaData()
    #     try:
    #         with self.get_session() as session:
    #             tables = [Table(t, metadata, autoload_with=session.bind) for t in tabelas]
    #             nome_para_tabela = {t.name: t for t in tables}

    #             # Monta colunas normais e guarda objetos para possível GROUP BY
    #             from sqlalchemy import func
    #             cols = []
    #             group_by_cols = []

    #             for col in colunas:
    #                 tabela_nome, coluna_nome = col.split('.', 1)
    #                 tabela_obj = nome_para_tabela[tabela_nome]
    #                 coluna_obj = tabela_obj.c[coluna_nome]
    #                 cols.append(coluna_obj)
    #                 group_by_cols.append(coluna_obj)

    #             # Adiciona colunas agregadas
    #             having_conditions = []

    #             for agg in agregacoes:
    #                 tabela_nome, coluna_nome = agg['coluna'].split('.', 1)
    #                 tabela_obj = nome_para_tabela[tabela_nome]
    #                 coluna_obj = tabela_obj.c[coluna_nome]

    #                 funcao = agg['funcao'].upper()
    #                 alias = agg.get('alias', f'{funcao}_{coluna_nome}')

    #                 # Cria a função agregada com alias
    #                 if funcao == 'COUNT':
    #                     expr = func.count(coluna_obj).label(alias)
    #                 elif funcao == 'SUM':
    #                     expr = func.sum(coluna_obj).label(alias)
    #                 elif funcao == 'AVG':
    #                     expr = func.avg(coluna_obj).label(alias)
    #                 elif funcao == 'MAX':
    #                     expr = func.max(coluna_obj).label(alias)
    #                 elif funcao == 'MIN':
    #                     expr = func.min(coluna_obj).label(alias)
    #                 else:
    #                     raise DaoError(f"Função de agregação desconhecida: {funcao}")

    #                 cols.append(expr)

    #                 # Se tiver cláusula HAVING
    #                 if 'having' in agg:
    #                     op = agg['having']['operador']
    #                     val = agg['having']['valor']
    #                     raw_expr = expr._proxy_key  # recupera o alias criado

    #                     # Expressão HAVING precisa usar a função agregada diretamente
    #                     if funcao == 'COUNT':
    #                         having_expr = func.count(coluna_obj)
    #                     elif funcao == 'SUM':
    #                         having_expr = func.sum(coluna_obj)
    #                     elif funcao == 'AVG':
    #                         having_expr = func.avg(coluna_obj)
    #                     elif funcao == 'MAX':
    #                         having_expr = func.max(coluna_obj)
    #                     elif funcao == 'MIN':
    #                         having_expr = func.min(coluna_obj)

    #                     # Mapeia operadores
    #                     if op == '>':
    #                         having_conditions.append(having_expr > val)
    #                     elif op == '>=':
    #                         having_conditions.append(having_expr >= val)
    #                     elif op == '<':
    #                         having_conditions.append(having_expr < val)
    #                     elif op == '<=':
    #                         having_conditions.append(having_expr <= val)
    #                     elif op == '=' or op == '==':
    #                         having_conditions.append(having_expr == val)
    #                     elif op == '!=':
    #                         having_conditions.append(having_expr != val)
    #                     else:
    #                         raise DaoError(f"Operador HAVING inválido: {op}")

    #             query = select(*cols)

    #             # Aplica filtros
    #             condicoes = []
    #             for f in filtros:
    #                 tabela_nome, coluna_nome = f['coluna'].split('.', 1)
    #                 tabela_obj = nome_para_tabela[tabela_nome]
    #                 coluna_obj = tabela_obj.c[coluna_nome]
    #                 valor = self.tratar_valor(coluna_nome, f['valor'])

    #                 op = f['operador']
    #                 if op == 'igual a':
    #                     condicoes.append(coluna_obj == valor)
    #                 elif op == 'maior que':
    #                     condicoes.append(coluna_obj > valor)
    #                 elif op == 'menor que':
    #                     condicoes.append(coluna_obj < valor)
    #                 elif op == 'maior ou igual a':
    #                     condicoes.append(coluna_obj >= valor)
    #                 elif op == 'menor ou igual a':
    #                     condicoes.append(coluna_obj <= valor)
    #                 elif op == 'diferente de':
    #                     condicoes.append(coluna_obj != valor)
    #                 elif op == 'parecido com':
    #                     condicoes.append(coluna_obj.like(f'%{valor}%'))
    #                 elif op == 'entre' and isinstance(valor, (list, tuple)) and len(valor) == 2:
    #                     condicoes.append(coluna_obj.between(valor[0], valor[1]))
    #                 else:
    #                     raise DaoError(f"Operador inválido ou mal formatado: {op}")

    #             # Joins dinâmicos
    #             relacoes, nome_para_tabela = self.extrair_relacoes(tables)
    #             query = self.montar_joins(query, tabelas, relacoes, nome_para_tabela)

    #             if condicoes:
    #                 query = query.where(and_(*condicoes))

    #             # Aplica GROUP BY se tiver colunas não agregadas
    #             if agregacoes and group_by_cols:
    #                 query = query.group_by(*group_by_cols)
                
    #             if having_conditions:
    #                 query = query.having(and_(*having_conditions))

    #             resultado = session.execute(query)
    #             rows = resultado.fetchall()
    #             keys = resultado.keys()

    #             return [dict(zip(keys, row)) for row in rows]

    #     except Exception as e:
    #         raise DaoError(f"Erro ao buscar dados do relatório: {e}")


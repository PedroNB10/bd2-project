from sqlalchemy import select, Table, MetaData, and_, func
from sqlalchemy.exc import NoSuchTableError
from app.daos.base_dao import BaseDAO
from app.exceptions.exceptions import DaoError
from datetime import date
from collections import defaultdict


class RelatorioDao(BaseDAO):

    # Função usada para tratar valores de data
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
    
    # Função usada para mapear o grafo de relações entre as tabelas usadas na consulta
    # tabelas: tabelas usadas na consulta
    # Retorna:
    # - o dicionário de relacionamentos (grafo)
    # - o mapa de nome -> tabela (para uso posterior nos joins)
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

                # Também armazena o inverso (bidirecional) - necessário para montar os joins de qualquer lado
                relacoes[destino].append((origem, condicao))

        return relacoes, nome_para_tabela
    
    # Função encarregada da gerência os Joins entre as tabelas, modelando as 
    # tabelas em forma de grafo e usando uma DFS para identificar com quais 
    # tabelas cada tabela selecionada se relaciona
    # query: consulta que vai ser retornada
    # tabelas_usadas: tabelas que estão sendo usadas na query
    # relacoes: tabelas com as quais as tabelas usadas podem se relacionar
    # nome_para_tabela: informações das tabelas utilizadas
    # Retorna a query com todos os joins necessários montados
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

        return query

    # Função principal usada para montar a consulta 
    # tabelas: tabelas que foram selecionadas pelo usuario
    # colunas: colunas a serem usadas no Select
    # filtros: Informações para a cláusula where
    # agregacoes: informações para ser usada se o usuario solicitar algum recurso de agregação 
    # Retorna: O resultado da query passada pelo usuario
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
        
    # Constroi a coluna criada pela operação de agregação
    # Colunas: colunas que vão ser exibidas sem ser a coluna de agregação
    # Agregacao: Informações(coluna, função e nome da tabela gerada) das agregações solicitadas
    # Nome_para_tabela: Informações da tabela escolhida
    def construir_colunas(self, colunas, agregacoes, nome_para_tabela):
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
    
    # Função para filtrar quais agregações foram solicitadas
    # função: função escolhida
    #coluna_obj: a coluna em que vou aplicar a função escolhida
    def criar_agregacao(self, funcao, coluna_obj):
        from sqlalchemy import func
        match funcao:
            case 'COUNT': return func.count(coluna_obj)
            case 'SUM': return func.sum(coluna_obj)
            case 'AVG': return func.avg(coluna_obj)
            case 'MAX': return func.max(coluna_obj)
            case 'MIN': return func.min(coluna_obj)
            case _: raise DaoError(f"Função de agregação desconhecida: {funcao}")

    # Função para lidar com os operadores tanto dos  having da agregação 
    # coluna_expr: coluna considerada no filtro
    # operador: operador escolhido pelo usuario
    # valor: valor a ser comparado com o valor de cada tupla da coluna expr 
    def operador_para_expressao(self, coluna_expr, operador, valor):
        match operador:
            case '>': return coluna_expr > valor
            case '>=': return coluna_expr >= valor
            case '<': return coluna_expr < valor
            case '<=': return coluna_expr <= valor
            case '=' | '==': return coluna_expr == valor
            case '!=': return coluna_expr != valor
            case _: raise DaoError(f"Operador HAVING inválido: {operador}")
        
    # Função para lidar também com filtro mas relacionado a clausula where da consulta
    # filtros: escolhido pelo usuario 
    # nome_para_tabela:  estrutura da tabela que sera aplicada o filtro
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
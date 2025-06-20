from sqlalchemy import select, Table, MetaData, and_, or_, text
from sqlalchemy.sql import operators
from app.daos.base_dao import BaseDAO
from app.exceptions.exceptions import DaoError
from datetime import datetime, date

class RelatorioDao(BaseDAO):
    
    def tratar_valor(self, coluna_nome: str, valor):
        if isinstance(valor, list) and len(valor) == 2:
            # Para filtros tipo "entre" com datas
            if 'date' in coluna_nome or 'time' in coluna_nome:
                try:
                    return [date.fromisoformat(valor[0]), date.fromisoformat(valor[1])]
                except Exception:
                    pass
        elif isinstance(valor, str):
            # Para operadores simples com uma única data
            if 'date' in coluna_nome or 'time' in coluna_nome:
                try:
                    return date.fromisoformat(valor)
                except Exception:
                    pass
        return valor
    
    def buscar_dados(self, tabelas: list[str], colunas: list[str], filtros: list[dict]) -> list[dict]:
        metadata = MetaData()
        try:
            with self.get_session() as session:
                # Refere às tabelas dinamicamente
                tables = [Table(t, metadata, autoload_with=session.bind) for t in tabelas]

                # Monta colunas selecionadas - colunas são strings 'tabela.coluna'
                cols = []
                for col in colunas:
                    tabela_nome, coluna_nome = col.split('.', 1)
                    tabela_obj = next(t for t in tables if t.name == tabela_nome)
                    cols.append(tabela_obj.c[coluna_nome])

                query = select(*cols)


                # Monta as condições (filtros)
                condicoes = []
                for f in filtros:
                    tabela_nome, coluna_nome = f['coluna'].split('.', 1)
                    tabela_obj = next(t for t in tables if t.name == tabela_nome)
                    coluna_obj = tabela_obj.c[coluna_nome]
                    
                    print('coluna: ', coluna_nome)
                    print('valor: ', f['valor'])
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
                        print(val)
                        print(coluna_obj)
                        print(coluna_nome)
                        condicoes.append(coluna_obj.between(val[0], val[1]))
                    else:
                        raise DaoError(f"Operador desconhecido ou inválido: {op}")

                if condicoes:
                    query = query.where(and_(*condicoes))

                resultado = session.execute(query)
                rows = resultado.fetchall()
                keys = resultado.keys()

                dados = [dict(zip(keys, row)) for row in rows]
                return dados

        except Exception as e:
            raise DaoError(f"Erro ao buscar dados do relatório: {e}")

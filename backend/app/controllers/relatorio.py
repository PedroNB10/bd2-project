from flask import jsonify
from app.daos.relatorio_dao import RelatorioDao

class RelatorioController:
    def __init__(self) -> None:
        self.relatorio = RelatorioDao()

    def relatorio_dados(self, payload):  # <-- adiciona o self aqui
        try:
            if not payload or 'tabelas' not in payload or 'colunas' not in payload:
                return jsonify({"erro": "Parâmetros inválidos, tabelas e colunas são obrigatórios"}), 400

            tabelas = payload['tabelas']
            colunas = payload['colunas']
            filtros = payload.get('filtros', [])

            dados = self.relatorio.buscar_dados(tabelas, colunas, filtros)

            return jsonify(dados)

        except Exception as e:
            print("Erro no controller:", e)
            return jsonify({"erro": "Erro ao buscar dados do relatório"}), 500


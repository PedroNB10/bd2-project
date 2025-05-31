class NoDataFound(Exception):
    """Exceção para quando não houver dados encontrados"""

    pass


class DatabaseError(Exception):
    """Exceção para encapsular erros gerais de banco de dados."""

    pass


class InvalidRequestArguments(Exception):
    """Exceção para argumentos inválidos em uma requisição"""

    pass


class DaoError(Exception):
    """Exceção erro dentro da execução da classe DAO"""

    pass

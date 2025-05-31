from sqlalchemy.inspection import inspect


def serialize(obj: object) -> dict:
    """
    Convert the SQLAlchemy model instance into a dictionary.
    Only includes columns mapped to the database, excluding internal state.
    """

    return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}

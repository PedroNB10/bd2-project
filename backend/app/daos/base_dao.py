import logging
from contextlib import contextmanager
from db import SessionLocal  # Adjust the import path as needed

logger = logging.getLogger(__name__)


class BaseDAO:
    @contextmanager
    def get_session(self):
        """
        Obtains a session to perform operations on the database.
        Ensures that the transaction is committed if everything goes well,
        or rolled back in case of an error.
        """
        session = SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error("Error during session execution", exc_info=True)
            raise
        finally:
            session.close()

    def get_all(self) -> list:
        """
        Returns a list of all records.
        Should be implemented by the subclass.
        """
        pass

    def get_by_id(self, id: int) -> object | None:
        """
        Returns a record with the specified ID, or None if not found.
        Should be implemented by the subclass.
        """
        pass

    def create(self, obj: object) -> int:
        """
        Creates a new record and returns the generated ID.
        Should be implemented by the subclass.
        """
        pass

    def update(self, obj: object) -> None:
        """
        Updates an existing record.
        Should be implemented by the subclass.
        """
        pass

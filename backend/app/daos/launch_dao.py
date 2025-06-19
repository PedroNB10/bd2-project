import logging
from app.daos.base_dao import BaseDAO
from app.models.models import Launches
from app.exceptions.exceptions import DaoError

logger = logging.getLogger(__name__)


class LaunchDao(BaseDAO):

    def get_all(self) -> list[Launches]:

        try:

            with self.get_session() as session:
                launches = session.query(Launches).all()
                session.expunge_all()

                return launches

        except Exception as e:
            logger.error("Error fetching all launches: %s", e, exc_info=True)

            raise DaoError("Error fetching all launches")

    def get_by_id(self, rocket_id: str) -> Launches | None:
        pass

    def create(self, rocket: Launches) -> int:
        pass

    def update(self, order: Launches):
        pass

    def get_columns(self):

        with self.get_session() as session:
                core = session.query(Launches).first()
                columns = core.__table__.columns
                session.expunge_all()

                # return columns.keys()
                return [(col.name, str(col.type)) for col in columns]
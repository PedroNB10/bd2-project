import logging
from app.daos.base_dao import BaseDAO
from app.models.models import LaunchCores
from app.exceptions.exceptions import DaoError

logger = logging.getLogger(__name__)


class LaunchCoreDao(BaseDAO):

    def get_all(self) -> list[LaunchCores]:

        try:

            with self.get_session() as session:
                launchcores = session.query(LaunchCores).all()
                session.expunge_all()

                return launchcores

        except Exception as e:
            logger.error("Error fetching all launchcores: %s", e, exc_info=True)

            raise DaoError("Error fetching all launchcores")

    def get_by_id(self, rocket_id: str) -> LaunchCores | None:
        pass

    def create(self, rocket: LaunchCores) -> int:
        pass

    def update(self, order: LaunchCores):
        pass

    def get_columns(self):
        with self.get_session() as session:
                core = session.query(LaunchCores).first()
                columns = core.__table__.columns
                session.expunge_all()

                return [(col.name, str(col.type)) for col in columns]
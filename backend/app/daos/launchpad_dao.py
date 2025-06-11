import logging
from app.daos.base_dao import BaseDAO
from app.models.models import Launchpads
from app.exceptions.exceptions import DaoError

logger = logging.getLogger(__name__)


class LaunchpadDao(BaseDAO):

    def get_all(self) -> list[Launchpads]:

        try:

            with self.get_session() as session:
                launchpads = session.query(Launchpads).all()
                session.expunge_all()

                return launchpads

        except Exception as e:
            logger.error("Error fetching all launchpads: %s", e, exc_info=True)

            raise DaoError("Error fetching all launchpads")

    def get_by_id(self, rocket_id: str) -> Launchpads | None:
        pass

    def create(self, rocket: Launchpads) -> int:
        pass

    def update(self, order: Launchpads):
        pass

    def get_columns(self):

        with self.get_session() as session:
                core = session.query(Launchpads).first()
                columns = core.__table__.columns
                session.expunge_all()

                return columns.keys()
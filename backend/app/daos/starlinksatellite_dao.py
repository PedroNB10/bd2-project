import logging
from app.daos.base_dao import BaseDAO
from app.models.models import StarlinkSatellites
from app.exceptions.exceptions import DaoError

logger = logging.getLogger(__name__)


class StarlinkSatelliteDao(BaseDAO):

    def get_all(self) -> list[StarlinkSatellites]:

        try:

            with self.get_session() as session:
                starlinksatellites = session.query(StarlinkSatellites).all()
                session.expunge_all()

                return starlinksatellites

        except Exception as e:
            logger.error("Error fetching all starlinksatellites: %s", e, exc_info=True)

            raise DaoError("Error fetching all starlinksatellites")

    def get_by_id(self, rocket_id: str) -> StarlinkSatellites | None:
        pass

    def create(self, rocket: StarlinkSatellites) -> int:
        pass

    def update(self, order: StarlinkSatellites):
        pass

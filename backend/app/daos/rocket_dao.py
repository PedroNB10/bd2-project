import logging
from app.daos.base_dao import BaseDAO
from app.models.models import Rockets
from app.exceptions.exceptions import DaoError

logger = logging.getLogger(__name__)


class RocketDao(BaseDAO):

    def get_all(self) -> list[Rockets]:

        try:

            with self.get_session() as session:
                rockets = session.query(Rockets).all()
                session.expunge_all()

                return rockets

        except Exception as e:
            logger.error("Error fetching all rockets: %s", e, exc_info=True)

            raise DaoError("Error fetching all rockets")

    def get_by_id(self, rocket_id: str) -> Rockets | None:
        pass

    def create(self, rocket: Rockets) -> int:
        pass

    def update(self, order: Rockets):
        pass

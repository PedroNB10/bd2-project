import logging
from app.daos.base_dao import BaseDAO
from app.models.models import OrbitalParameters
from app.exceptions.exceptions import DaoError

logger = logging.getLogger(__name__)


class OrbitalDao(BaseDAO):

    def get_all(self) -> list[OrbitalParameters]:

        try:

            with self.get_session() as session:
                orbital = session.query(OrbitalParameters).all()
                session.expunge_all()

                return orbital

        except Exception as e:
            logger.error("Error fetching all orbital_parameters: %s", e, exc_info=True)

            raise DaoError("Error fetching all orbital_parameters")

    def get_by_id(self, rocket_id: str) -> OrbitalParameters | None:
        pass

    def create(self, rocket: OrbitalParameters) -> int:
        pass

    def update(self, order: OrbitalParameters):
        pass

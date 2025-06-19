import logging
from app.daos.base_dao import BaseDAO
from app.models.models import Crew
from app.exceptions.exceptions import DaoError

logger = logging.getLogger(__name__)


class CrewDao(BaseDAO):

    def get_all(self) -> list[Crew]:

        try:

            with self.get_session() as session:
                crews = session.query(Crew).all()
                session.expunge_all()

                return crews

        except Exception as e:
            logger.error("Error fetching all crews: %s", e, exc_info=True)

            raise DaoError("Error fetching all crews")

    def get_by_id(self, rocket_id: str) -> Crew | None:
        pass

    def create(self, rocket: Crew) -> int:
        pass

    def update(self, order: Crew):
        pass

    def get_columns(self):

        with self.get_session() as session:
                core = session.query(Crew).first()
                columns = core.__table__.columns
                session.expunge_all()

                # return columns.keys()
                return [(col.name, str(col.type)) for col in columns]
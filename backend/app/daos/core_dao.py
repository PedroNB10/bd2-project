import logging
from app.daos.base_dao import BaseDAO
from app.models.models import Cores
from app.exceptions.exceptions import DaoError

logger = logging.getLogger(__name__)


class CoreDao(BaseDAO):

    def get_all(self) -> list[Cores]:

        try:

            with self.get_session() as session:
                cores = session.query(Cores).all()
                session.expunge_all()

                return cores

        except Exception as e:
            logger.error("Error fetching all cores: %s", e, exc_info=True)

            raise DaoError("Error fetching all cores")

    def get_by_id(self, rocket_id: str) -> Cores | None:
        pass

    def create(self, rocket: Cores) -> int:
        pass

    def update(self, order: Cores):
        pass

    def get_columns(self):

        with self.get_session() as session:
                core = session.query(Cores).first()
                columns = core.__table__.columns
                session.expunge_all()

                # return columns.keys()
                return [(col.name, str(col.type)) for col in columns]
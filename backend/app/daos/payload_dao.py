import logging
from app.daos.base_dao import BaseDAO
from app.models.models import Payloads
from app.exceptions.exceptions import DaoError

logger = logging.getLogger(__name__)


class PayloadDao(BaseDAO):

    def get_all(self) -> list[Payloads]:

        try:

            with self.get_session() as session:
                payloads = session.query(Payloads).all()
                session.expunge_all()

                return payloads

        except Exception as e:
            logger.error("Error fetching all payloads: %s", e, exc_info=True)

            raise DaoError("Error fetching all payloads")

    def get_by_id(self, rocket_id: str) -> Payloads | None:
        pass

    def create(self, rocket: Payloads) -> int:
        pass

    def update(self, order: Payloads):
        pass

    def get_columns(self):

        with self.get_session() as session:
                core = session.query(Payloads).first()
                columns = core.__table__.columns
                session.expunge_all()

                return columns.keys()
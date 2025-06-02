from app.daos.payload_dao import PayloadDao
from app.utils.serialize import serialize
from app.exceptions.exceptions import DaoError, NoDataFound


class PayloadsController:

    def __init__(self) -> None:
        self.payloads_dao = PayloadDao()

    def get_all_payloads(self) -> dict:
        try:
            payloads = self.payloads_dao.get_all()
            if not payloads:
                raise AttributeError("No payloads found")

            payloads_dict = [serialize(payload) for payload in payloads]
            return payloads_dict

        except NoDataFound as e:
            raise

        except DaoError as e:
            raise

        except Exception as e:
            print(f"Error fetching all payloads: {e}")
            raise

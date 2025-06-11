from app.daos.rocket_dao import RocketDao
from app.utils.serialize import serialize
from app.exceptions.exceptions import DaoError, NoDataFound


class RocketsController:

    def __init__(self) -> None:
        self.rockets_dao = RocketDao()

    def get_all_rockets(self) -> dict:
        try:
            rockets = self.rockets_dao.get_all()
            if not rockets:
                raise AttributeError("No rockets found")

            rockets_dict = [serialize(rocket) for rocket in rockets]
            return rockets_dict

        except NoDataFound as e:
            raise

        except DaoError as e:
            raise

        except Exception as e:
            print(f"Error fetching all orders: {e}")
            raise

    def get_columns(self):
        try:
            keys = self.rockets_dao.get_columns()
            if not keys:
                raise AttributeError("No rockets found")

            return keys

        except NoDataFound as e:
            raise

        except DaoError as e:
            raise

        except Exception as e:
            print(f"Error fetching column names for table rockets: {e}")
            raise

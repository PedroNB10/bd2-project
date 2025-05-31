from app.daos.rocket_dao import RocketDao
from app.utils.serialize import serialize
from app.exeptions.exeptions import DaoError, NoDataFound


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

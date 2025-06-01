from app.daos.launch_dao import LaunchDao
from app.utils.serialize import serialize
from app.exceptions.exceptions import DaoError, NoDataFound


class LaunchesController:

    def __init__(self) -> None:
        self.launches_dao = LaunchDao()

    def get_all_launches(self) -> dict:
        try:
            launches = self.launches_dao.get_all()
            if not launches:
                raise AttributeError("No launches found")

            launches_dict = [serialize(launches) for launches in launches]
            return launches_dict

        except NoDataFound as e:
            raise

        except DaoError as e:
            raise

        except Exception as e:
            print(f"Error fetching all launches: {e}")
            raise

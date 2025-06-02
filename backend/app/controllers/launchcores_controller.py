from app.daos.launchcore_dao import LaunchCoreDao
from app.utils.serialize import serialize
from app.exceptions.exceptions import DaoError, NoDataFound


class LaunchCoresController:

    def __init__(self) -> None:
        self.launchcores_dao = LaunchCoreDao()

    def get_all_launchcores(self) -> dict:
        try:
            launchcores = self.launchcores_dao.get_all()
            if not launchcores:
                raise AttributeError("No launchcores found")

            launchcores_dict = [serialize(launchcore) for launchcore in launchcores]
            return launchcores_dict

        except NoDataFound as e:
            raise

        except DaoError as e:
            raise

        except Exception as e:
            print(f"Error fetching all launchcores: {e}")
            raise

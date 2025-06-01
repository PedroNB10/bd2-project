from app.daos.launchpad_dao import LaunchpadDao
from app.utils.serialize import serialize
from app.exceptions.exceptions import DaoError, NoDataFound


class LaunchpadsController:

    def __init__(self) -> None:
        self.launchpads_dao = LaunchpadDao()

    def get_all_launchpads(self) -> dict:
        try:
            launchpads = self.launchpads_dao.get_all()
            if not launchpads:
                raise AttributeError("No launchpads found")

            launchpads_dict = [serialize(launchpad) for launchpad in launchpads]
            return launchpads_dict

        except NoDataFound as e:
            raise

        except DaoError as e:
            raise

        except Exception as e:
            print(f"Error fetching all launchpads: {e}")
            raise

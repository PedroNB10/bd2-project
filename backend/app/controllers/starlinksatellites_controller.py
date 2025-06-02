from app.daos.starlinksatellite_dao import StarlinkSatelliteDao
from app.utils.serialize import serialize
from app.exceptions.exceptions import DaoError, NoDataFound


class StarlinkSatellitesController:

    def __init__(self) -> None:
        self.starlinksatellites_dao = StarlinkSatelliteDao()

    def get_all_starlinksatellites(self) -> dict:
        try:
            starlinksatellites = self.starlinksatellites_dao.get_all()
            if not starlinksatellites:
                raise AttributeError("No starlinksatellites found")

            starlinksatellites_dict = [serialize(starlinksatellite) for starlinksatellite in starlinksatellites]
            return starlinksatellites_dict

        except NoDataFound as e:
            raise

        except DaoError as e:
            raise

        except Exception as e:
            print(f"Error fetching all starlinksatellites: {e}")
            raise

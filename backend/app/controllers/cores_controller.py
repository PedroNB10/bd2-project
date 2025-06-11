from app.daos.core_dao import CoreDao
from app.utils.serialize import serialize
from app.exceptions.exceptions import DaoError, NoDataFound


class CoresController:

    def __init__(self) -> None:
        self.cores_dao = CoreDao()

    def get_all_cores(self) -> dict:
        try:
            cores = self.cores_dao.get_all()
            if not cores:
                raise AttributeError("No cores found")

            cores_dict = [serialize(core) for core in cores]
            return cores_dict

        except NoDataFound as e:
            raise

        except DaoError as e:
            raise

        except Exception as e:
            print(f"Error fetching all cores: {e}")
            raise

    def get_columns(self):
        try:
            keys = self.cores_dao.get_columns()
            if not keys:
                raise AttributeError("No cores found")

            return keys

        except NoDataFound as e:
            raise

        except DaoError as e:
            raise

        except Exception as e:
            print(f"Error fetching column names for table Cores: {e}")
            raise

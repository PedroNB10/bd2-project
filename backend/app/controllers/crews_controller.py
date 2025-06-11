from app.daos.crew_dao import CrewDao
from app.utils.serialize import serialize
from app.exceptions.exceptions import DaoError, NoDataFound


class CrewsController:

    def __init__(self) -> None:
        self.crews_dao = CrewDao()

    def get_all_crews(self) -> dict:
        try:
            crews = self.crews_dao.get_all()
            if not crews:
                raise AttributeError("No crews found")

            crews_dict = [serialize(crew) for crew in crews]
            return crews_dict

        except NoDataFound as e:
            raise

        except DaoError as e:
            raise

        except Exception as e:
            print(f"Error fetching all crews: {e}")
            raise

    def get_columns(self):
        try:
            keys = self.crews_dao.get_columns()
            if not keys:
                raise AttributeError("No crews found")

            return keys

        except NoDataFound as e:
            raise

        except DaoError as e:
            raise

        except Exception as e:
            print(f"Error fetching column names for table Crews: {e}")
            raise

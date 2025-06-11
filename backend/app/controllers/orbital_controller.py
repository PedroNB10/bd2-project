from app.daos.orbital_dao import OrbitalDao
from app.utils.serialize import serialize
from app.exceptions.exceptions import DaoError, NoDataFound


class OrbitalsController:

    def __init__(self) -> None:
        self.orbitals_dao = OrbitalDao()

    def get_all_orbitals(self) -> dict:
        try:
            orbitals = self.orbitals_dao.get_all()
            if not orbitals:
                raise AttributeError("No orbitals found")

            orbitals_dict = [serialize(orbital) for orbital in orbitals]
            return orbitals_dict

        except NoDataFound as e:
            raise

        except DaoError as e:
            raise

        except Exception as e:
            print(f"Error fetching all orders: {e}")
            raise

    def get_columns(self):
        try:
            keys = self.orbitals_dao.get_columns()
            if not keys:
                raise AttributeError("No orbitals found")

            return keys

        except NoDataFound as e:
            raise

        except DaoError as e:
            raise

        except Exception as e:
            print(f"Error fetching column names for table orbitals: {e}")
            raise
